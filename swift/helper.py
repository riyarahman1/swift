from django.db.models import Prefetch, Subquery
from django.db.models import Q
from django.shortcuts import render
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from swift.constantvariables import APPFOLDERNAME, PAGINATION_PERPAGE, FROM_EMAIL, UAE_TIMEZONE
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from datetime import timedelta
import json
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.template import loader
from swift.models import *
import pytz
from datetime import datetime
from .constantvariables import FROM_EMAIL
from django.utils.encoding import force_bytes
import os
from django.core.files import File
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
#from dateutil.relativedelta import relativedelta
from .models import EmailTemplate

try:
    import zoneinfo
except ImportError:
    from backports import zoneinfo


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def flush_cache(text):
    cache.clear()


def renderfile(request, foldername=None, pagename=None, variableobj=None, innerfolder=None):
    if innerfolder and foldername:
        if innerfolder:
            return render(request, APPFOLDERNAME + '/' + foldername + '/' + pagename + '/' + variableobj + '.html', innerfolder)
    elif foldername:
        if variableobj:
            return render(request, APPFOLDERNAME + '/' + foldername + '/' + pagename + '.html', variableobj)
        else:
            return render(request, APPFOLDERNAME + '/' + foldername + '/' + pagename + '.html', {})
    else:
        if variableobj:
            return render(request, APPFOLDERNAME + '/' + pagename + '.html', variableobj)
        else:
            return render(request, APPFOLDERNAME + '/' + pagename + '.html', {})


def paginationhelper(paginationrecord=None, page=None):
    paginator = Paginator(paginationrecord, PAGINATION_PERPAGE)

    try:
        paginationrecord = paginator.page(page)
    except PageNotAnInteger:
        paginationrecord = paginator.page(1)
    except EmptyPage:
        paginationrecord = paginator.page(paginator.num_pages)
    return paginationrecord


def date_range(start, end):
    delta = end - start  # as timedelta
    days = [start + timedelta(days=i) for i in range(delta.days + 1)]
    return days



def emailhelper(request, subject=None, template_id=None, contentreplace=None, to_email=None, action=None):
    if template_id:
        mail_subject = subject
        email_content_template = EmailTemplate.objects.get(pk=template_id)
        # print(email_content_template.content,'@emailtempalte')
        templatecontent = email_content_template.content
        for k, v in contentreplace.items():
            templatecontent = templatecontent.replace(k, v)
        html = templatecontent
        # print(html,'@emailtempalte')
        c_template = loader.get_template(
            'hisensehr/email-layout/common_email_layout.html')
        html_c_template = c_template.render({
            'content': html, }, request)
        html = html_c_template
        to_email = to_email
        if action == 'forget-password':
            from_mail = FROM_EMAIL
        else:
            from_mail = FROM_EMAIL
        if send_mail(mail_subject, '', from_mail, [to_email], fail_silently=False, html_message=html):
            return True
        else:
            return False
    else:
        return False



def convert_timestamp_in_datetime_utc(timestamp_received):
    dt_naive_utc = datetime.utcfromtimestamp(timestamp_received)
    return dt_naive_utc.replace(tzinfo=pytz.utc)


def media_url(request):
    scheme = request.is_secure() and "https" or "http"
    return '{0}://{1}/media/'.format(scheme, request.get_host())


def timezone(date):
    try:
        local_timezone = zoneinfo.ZoneInfo(UAE_TIMEZONE)
        date_time = date.astimezone(local_timezone)
        return date_time.strftime("%d %B %Y")
    except Exception as e:
        return None


def timezone_requstesdate(date):
    try:
        local_timezone = zoneinfo.ZoneInfo(UAE_TIMEZONE)
        date_time = date.astimezone(local_timezone)
        return date_time.strftime("%d %b %Y")
    except Exception as e:
        return None


def encrypt_me(value):
    encrypted = urlsafe_base64_encode(
        force_bytes("{0}***{1}".format(value, 'jesus')))
    return str(encrypted)


def decrypt_me(value):
    uid = urlsafe_base64_decode(value).decode()
    uid_split = uid.split("***")
    decrypted = None
    if uid_split[0]:
        decrypted = uid_split[0]
    return str(decrypted)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'



def LogUserActivity(request, data):
    actor = request.user if request.user.is_authenticated else None
    if actor:
        scheme = request.is_secure() and "https://" or "http://"
        current_site = get_current_site(request)
        domainlink = scheme + current_site.domain
        status = data['status']
        action_type = data['action_type']
        module_name = data['module_name']
        log_message = data['log_message']
        model_object = data['model_object']
        db_data = data['db_data']
        app_visibility = data['app_visibility'] if data['app_visibility'] else False
        web_visibility = data['web_visibility'] if data['web_visibility'] else False
        activity_mode = data['activity_mode'] if 'activity_mode' in data and data['activity_mode'] else 'Web'
        error_msg = data['error_msg']
        fwd_link = domainlink + data['fwd_link']
        data = {
            "actor": actor,
            "status": status,
            "action_type": action_type,
            "module_name": module_name,
            "web_visibility": web_visibility,
            "app_visibility": app_visibility,
            "path_info": {'path': request.path, 'path_name': request.resolver_match.url_name},
            "fwd_link": fwd_link,
            "activity_mode": activity_mode,
        }
        if log_message:
            data["remarks"] = log_message
        else:
            f"User: {request.user} -- Action Type: {action_type} -- Path: {request.path} -- Path Name: {request.resolver_match.url_name}"

        try:
            if model_object:
                data["content_type"] = ContentType.objects.get_for_model(
                    model_object
                )
                data["content_object"] = model_object
            else:
                data["content_type"] = None
                data["content_object"] = None
        except:
            data["content_type"] = None
            data["content_object"] = None

        if db_data:
            data["data"] = db_data

        if status == 'Failed':
            data["error_msg"] = error_msg

        # print("----logdata---",data)
        ActivityLog.objects.create(**data)

"""


def LogUserActivity(request, data):
    actor = request.user if request.user.is_authenticated else None
    # print("---actor---",actor)
    if actor:
        scheme = request.is_secure() and "https://" or "http://"
        current_site = get_current_site(request)
        domainlink = scheme + current_site.domain
        status = data['status']
        action_type = data['action_type']
        module_name = data['module_name']
        log_message = data['log_message']
        model_object = data['model_object']
        db_data = data['db_data']
        app_visibility = data['app_visibility'] if data['app_visibility'] else False
        web_visibility = data['web_visibility'] if data['web_visibility'] else False
        activity_mode = data['activity_mode'] if 'activity_mode' in data and data['activity_mode'] else 'Web'
        error_msg = data['error_msg']
        fwd_link = domainlink + data['fwd_link']
        data = {
            "actor": actor,
            "status": status,
            "action_type": action_type,
            "module_name": module_name,
            "web_visibility": web_visibility,
            "app_visibility": app_visibility,
            "path_info": {'path': request.path, 'path_name': request.resolver_match.url_name},
            "fwd_link": fwd_link,
            "activity_mode": activity_mode,
        }
        if log_message:
            data["remarks"] = log_message
        else:
            f"User: {request.user} -- Action Type: {action_type} -- Path: {request.path} -- Path Name: {request.resolver_match.url_name}"

        try:
            if model_object:
                data["content_type"] = ContentType.objects.get_for_model(
                    model_object
                )
                data["content_object"] = model_object
            else:
                data["content_type"] = None
                data["content_object"] = None
        except:
            data["content_type"] = None
            data["content_object"] = None

        if db_data:
            data["data"] = db_data

        if status == 'Failed':
            data["error_msg"] = error_msg

        # print("----logdata---",data)
        ActivityLog.objects.create(**data)

"""
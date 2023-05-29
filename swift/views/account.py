import datetime
from django.views.generic import CreateView,View
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from swift.helper import renderfile
import pdb
import json
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template import loader
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.cache import cache
from django.utils.http import url_has_allowed_host_and_scheme
from swift.forms.account import SignInForm
from django.db.models import Value as V
from swiftteacher.settings import ACTIVITY_PASSWORD, ALLOWED_IP
from django.core.paginator import *
import calendar
from swift.models import User
from swift.helper import emailhelper


class SignIn(CreateView):
    template_name = "swift/account/index.html"
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect( reverse('appswift:home' ) )
        
        cache.set('next', request.GET.get('next', None))
        datas = { 'form' : SignInForm() }
        return render(request, self.template_name, datas)

    def post(self, request, *args, **kwargs):
        datas = {}
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
            if user is not None and user.is_active:
                login(self.request, user)
                next_url = cache.get('next')
                if next_url:
                    cache.delete('next')
                    if not url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
                        return HttpResponseRedirect(reverse('appswift:home'))
                    else:
                        return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse('appswift:home'))
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect( reverse('appswift:signin') )
        else:
            email = request.POST.get('email')
            if User.objects.filter(email=email, is_active=False).exists():
                messages.error(request,"Your account is not active")
            else:
                if not request.POST.get('email'):
                    messages.error(request,"Email is required")
                elif not request.POST.get('password'):
                    messages.error(request,"Password is required")
                else:
                    messages.error(request,"Invalid Login Details")
        datas['form'] = form
        return render(request, self.template_name, datas)


class Home(LoginRequiredMixin, CreateView):
    template_name = "swift/account/home.html"
    def get(self, request, *args, **kwargs):
        # if self.request.user.is_authenticated:
        #     return HttpResponseRedirect( reverse('appswift:home' ) )
        cache.set('next', request.GET.get('next', None))
        datas = { 'form' : SignInForm() }
        return render(request, self.template_name, datas)
    

class SignOut(CreateView):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        request.session.flush()
        return HttpResponseRedirect( reverse('appswift:signin') )


class ForgotPassword(View):
    def get(self, request, *args, **kwargs):
        return renderfile(request,'account','forgot_password')
    
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            scheme = request.is_secure() and "https://" or "http://"
            current_site = get_current_site(request)
            domainlink = scheme + current_site.domain
            mail_subject = 'Swift - Forgot Password'
            template = loader.get_template(
                'hisensehr/email-layout/acc_active_email.html')
            html_temp = template.render({
                'domain': domainlink,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)}, request)

            content_replace = {"NAME": str(user.first_name).capitalize() + " " + str(user.last_name).capitalize(), "LINK": html_temp}
            if emailhelper(request, mail_subject, 3, content_replace, email,action="forget-password"):
                messages.success(request, 'Reset Password Link Was Sent To Your Email!')
                return HttpResponseRedirect( reverse('appswift:signin') )
            else:
                messages.error(request, "Something went wrong")
                return HttpResponseRedirect( reverse('appswift:forgot_password') )
        except User.DoesNotExist:
            email = request.POST.get('email')
            if not email:
                messages.error(request, "Email is required")
            else:
                messages.error(request, "User not found with this email")
            return renderfile(request, 'account', 'forgot_password')

"""def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        
        if user:
            return renderfile(request, 'account', 'reset_password', {'user': user.id})
        else:
            return renderfile(request, '', '404', {})
    else:
        return renderfile(request, '', '404', {})

def change_password(request):
    userid = request.POST.get('user')
    pwd = request.POST.get('password1')
    cpwd = request.POST.get('password2')
    try:
        user = User.objects.get(pk=userid)
    except User.DoesNotExist:
        user = None
    if not pwd:
        messages.error(request, "Password cannot be empty")
        return renderfile(request, 'account', 'reset_password', {'user': user.id})
    if pwd == cpwd:
        if len(pwd)>=6:
            with transaction.atomic():
                if user:
                    user.set_password(pwd)
                    user.save()
                    # Profile.objects.filter(user=user).update(password_str=pwd)
                    messages.success(request, "Password Changed Successfully")
                    return HttpResponseRedirect( reverse('appswift:signin') )
                else:
                    messages.error(request, "Something went wrong")
                    return renderfile(request, 'account', 'reset_password', {'user': user.id})
        else:
            messages.error(request, "Password must be atleast 8 characters")
            return renderfile(request, 'account', 'reset_password', {'user': user.id})
    else:
        messages.error(request, "New password and confirm password should be same")
        return renderfile(request, 'account', 'reset_password', {'user': user.id})


    
class ActivityLogView(View):
    def get(self, request, *args, **kwargs):
        return renderfile(request,'utils','activity_log')
    
    def post(self, request, *args, **kwargs):
        context = {}
        context['permission_granted'] = False
        #print("--------",ACTIVITY_PASSWORD)
        if ACTIVITY_PASSWORD:
            user_password = request.POST.get('activity_password')
            try:
                #print(ACTIVITY_PASSWORD,"----", user_password)
                if user_password == ACTIVITY_PASSWORD:
                    context['permission_granted'] = True
                    context['action_types'] = ACTION_TYPES
                    context['action_statuses'] = ACTION_STATUS
                    context['employees'] =  User.objects.only('id','first_name','last_name').exclude(is_superuser=True).order_by('first_name')
                else:
                    messages.error(request, "No permission to do the action")
            except Exception as e:
                messages.error(request, "No permission to do the action")
        else:
            messages.error(request, "No permission to do the action")
        return renderfile(request,'utils','activity_log', context)
    
class FetchActivityLogView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        data = {}
        conditions = {}
        page = request.GET.get('page', 1)
        employee = request.GET.get('employee')
        action = request.GET.get('action')
        status = request.GET.get('status')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        activity_mode = request.GET.get('mode')
        if employee:
            conditions['actor_id'] = employee
        if action:
            conditions['action_type'] = action
        if status:
            conditions['status'] = status
        if activity_mode: 
            conditions['activity_mode'] = activity_mode
        if from_date and to_date:
            conditions['action_time__date__range'] = (from_date,to_date)
        #print("-------",conditions)
        activities = ActivityLog.objects.select_related('actor','actor__profile').filter(**conditions).\
                    only('id','remarks','action_type','status','action_time','data','actor__first_name','actor__last_name','actor__profile__employee_id').\
                    order_by('-id')
    
        paginator = Paginator(activities, 50)
        try:
            activities = paginator.page(page)
        except PageNotAnInteger:
            activities = paginator.page(1)
        except EmptyPage:
            activities = paginator.page(paginator.num_pages)
        if type(page) != int:
            page = int(page)

        context['activities'], data['status'], context['current_page']  = activities, True, page
        
        data['status'] = True
        data['pagination'] = render_to_string("hisensehr/utils/log_data_pagination.html",context=context, request=request)
        data['template'] = render_to_string('hisensehr/utils/log_data_ajax.html', context=context, request=request)
        return JsonResponse(data)


class SupportActivityLogView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['permission_granted'] = True
        context['action_types'] = ACTION_TYPES
        context['action_statuses'] = ACTION_STATUS
        context['employees'] =  User.objects.only('id','first_name','last_name').exclude(is_superuser=True).order_by('first_name')
        return renderfile(request,'support','activity_log',context)
    
    
    
class SupportFetchActivityLogView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        data = {}
        conditions = {}
        page = request.GET.get('page', 1)
        employee = request.GET.get('employee')
        action = request.GET.get('action')
        status = request.GET.get('status')
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        activity_mode = request.GET.get('mode')
        if employee:
            conditions['actor_id'] = employee
        if action:
            conditions['action_type'] = action
        if status:
            conditions['status'] = status
        if activity_mode: 
            conditions['activity_mode'] = activity_mode
        if from_date and to_date:
            conditions['action_time__date__range'] = (from_date,to_date)
        #print("-------",conditions)
        activities = ActivityLog.objects.select_related('actor','actor__profile').filter(**conditions).\
                    only('id','remarks','action_type','status','action_time','data','activity_mode','actor__first_name','actor__last_name','actor__profile__employee_id').\
                    order_by('-id')
    
        paginator = Paginator(activities, 50)
        try:
            activities = paginator.page(page)
        except PageNotAnInteger:
            activities = paginator.page(1)
        except EmptyPage:
            activities = paginator.page(paginator.num_pages)
        if type(page) != int:
            page = int(page)

        context['activities'], data['status'], context['current_page']  = activities, True, page
        
        data['status'] = True
        data['pagination'] = render_to_string("hisensehr/support/log_data_pagination.html",context=context, request=request)
        data['template'] = render_to_string('hisensehr/support/log_data_ajax.html', context=context, request=request)
        return JsonResponse(data)
    """

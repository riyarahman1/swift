from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from swift.forms.topics import TopicForm
from django.core.paginator import *
from swift.constantvariables import PAGINATION_PERPAGE
from swift.models import Topic, Course, Subject
from swift.helper import renderfile, is_ajax, LogUserActivity
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db import transaction
from swift.models import CREATE, UPDATE, SUCCESS, FAILED, DELETE
from django.shortcuts import get_object_or_404, render


class TopicView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("search")
        subjects = request.GET.get("subject") 
        courses = request.GET.get("course") 
        condition = {"is_active": True}
        if query:
            condition["name__icontains"] = query
        if subjects:
            condition["subject_id"] = subjects
        if courses:
            condition["subject__course__id"] = courses
        topics = Topic.objects.select_related("subject").filter(**condition).order_by("-id")

        subject_list = Subject.objects.all()  
        course_list =  Course.objects.all()  
        if courses:
            subject_list = subject_list.filter(course_id=courses)
        
        context = {}
        context["subjects"] = subject_list
        context["courses"] = course_list

        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            page = 1

        paginator = Paginator(topics, PAGINATION_PERPAGE)
        try:
            topics = paginator.page(page)
        except PageNotAnInteger:
            topics = paginator.page(1)
        except EmptyPage:
            topics = paginator.page(paginator.num_pages)

        context["topics"], context["current_page"] = topics, page

        if is_ajax(request=request):
            response = {
                "status": True,
                "pagination": render_to_string(
                    "swift/topic/pagination.html", context=context, request=request
                ),
                "template": render_to_string(
                    "swift/topic/topic_list.html", context=context, request=request
                ),
            }
            return JsonResponse(response)

        course_id = request.GET.get("course_id")
        course = get_object_or_404(Course, id=course_id) if course_id else None

        form = TopicForm(
            initial={"course": course}
        )  


        context["form"] = form
        return renderfile(request, "topic", "index", context)



class TopicCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = TopicForm()

        context = {"form": form, "id": 0}
        data["status"] = True
        data["title"] = "Add Topic"
        data["template"] = render_to_string(
            "swift/topic/topic_form.html", context, request=request
        )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        response = {}
        form = TopicForm(request.POST or None)
        if form.is_valid():
            try:
                # with transaction.atomic():
                name = request.POST.get("name", None)
                subject = request.POST.get("subject", None)
                # CHECK THE DATA EXISTS
                if not Topic.objects.filter(name=name).exists():
                    obj = Topic.objects.create(
                         name=name, subject_id=subject
                     )

                    # log entry
                    log_data = {}
                    log_data["module_name"] = "Topic"
                    log_data["action_type"] = CREATE
                    log_data["log_message"] = "Topic Created"
                    log_data["status"] = SUCCESS
                    log_data["model_object"] = obj
                    log_data["db_data"] = {"name": name}
                    log_data["app_visibility"] = True
                    log_data["web_visibility"] = True
                    log_data["error_msg"] = ""
                    log_data["fwd_link"] = "/topic/"
                    LogUserActivity(request, log_data)

                    response["status"] = True
                    response["message"] = "Added successfully"
                else:
                    response["status"] = False
                    response["message"] = "Topic Already exists"

            except Exception as error:
                log_data = {}
                log_data["module_name"] = "Topic"
                log_data["action_type"] = CREATE
                log_data["log_message"] = "Topic updation failed"
                log_data["status"] = FAILED
                log_data["model_object"] = None
                log_data["db_data"] = {}
                log_data["app_visibility"] = False
                log_data["web_visibility"] = False
                log_data["error_msg"] = error
                log_data["fwd_link"] = "/topic/"
                LogUserActivity(request, log_data)

                response["status"] = False
                response["message"] = "Something went wrong"
        else:
            response["status"] = False
            context = {"form": form}
            response["title"] = "Add Topic"
            response["valid_form"] = False
            response["template"] = render_to_string(
                "swift/topic/topic_form.html", context, request=request
            )
        return JsonResponse(response)

class TopicUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)
        data = {}
        obj = get_object_or_404(Topic, id=id)
        form = TopicForm(instance=obj)
        context = {"form": form, "id": id, "course_id": obj.subject.course_id}
        data["status"] = True
        data["title"] = "Edit Topic"
        data["template"] = render_to_string(
            "swift/topic/topic_form.html", context, request=request
        )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data, response = {}, {}
        id = kwargs.get("pk", None)
        obj = get_object_or_404(Topic, id=id)
        previous_name = obj.name
        form = TopicForm(request.POST or None, instance=obj)

        if form.is_valid():
            try:
                with transaction.atomic():
                    if (
                        Topic.objects.filter(name__icontains=request.POST.get("name"))
                        .exclude(id=id)
                        .exists()
                    ):
                        response["status"] = False
                        response["message"] = "Name already exists"
                        return JsonResponse(response)
                    obj.name = request.POST.get("name" or None)
                    obj.description = request.POST.get("description" or None)
                    obj.save()

                    # log entry
                    log_data = {}
                    log_data["module_name"] = "Topic"
                    log_data["action_type"] = UPDATE
                    log_data["log_message"] = "Topic Updated"
                    log_data["status"] = SUCCESS
                    log_data["model_object"] = obj
                    log_data["db_data"] = {
                        "previous_name": previous_name,
                        "updated_name": obj.name,
                    }
                    log_data["app_visibility"] = True
                    log_data["web_visibility"] = True
                    log_data["error_msg"] = ""
                    log_data["fwd_link"] = "/topic/"
                    LogUserActivity(request, log_data)

                    response["status"] = True
                    response["message"] = "Topic updated successfully"
                    return JsonResponse(response)

            except Exception as dberror:
                log_data = {}
                log_data["module_name"] = "Topic"
                log_data["action_type"] = UPDATE
                log_data["log_message"] = "Topic updation failed"
                log_data["status"] = FAILED
                log_data["model_object"] = None
                log_data["db_data"] = {}
                log_data["app_visibility"] = False
                log_data["web_visibility"] = False
                log_data["error_msg"] = dberror
                log_data["fwd_link"] = "/topic/"
                LogUserActivity(request, log_data)

                response["message"] = "Something went wrong"
                response["status"] = True
        else:
            response["status"] = False
            context = {"form": form, "course_id": obj.subject.course_id}
            response["title"] = "Edit Topic"
            response["valid_form"] = False
            response["template"] = render_to_string(
                "swift/topic/topic_form.html", context, request=request
            )
            return JsonResponse(response)


class TopicDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)
        response = {}
        obj = get_object_or_404(Topic, id=id)
        obj.is_active = False
        obj.save()

        # log entry
        log_data = {}
        log_data["module_name"] = "Topic"
        log_data["action_type"] = DELETE
        log_data["log_message"] = f"Deleted Topic {obj.name}"
        log_data["status"] = SUCCESS
        log_data["model_object"] = None
        log_data["db_data"] = {"name": obj.name}
        log_data["app_visibility"] = True
        log_data["web_visibility"] = True
        log_data["error_msg"] = ""
        log_data["fwd_link"] = "/Topic/"
        LogUserActivity(request, log_data)

        response["status"] = True
        response["message"] = "Topic deleted successfully"
        return JsonResponse(response)



class FilteredSubjectsView(View):
    def get(self, request):
        course_id = request.GET.get('course_id')
        subjects = Subject.objects.filter(course_id=course_id)
        subject_list = [{'id': subject.id, 'name': subject.name} for subject in subjects]
        return JsonResponse({'subjects': subject_list})
    


class GetSubjectsView(View):
    def get(self, request, *args, **kwargs):
        course_id = request.GET.get("course_id")
        subjects = Subject.objects.filter(course_id=course_id).values("id", "name")
        return JsonResponse({"subjects": list(subjects)})    
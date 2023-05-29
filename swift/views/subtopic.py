from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from swift.forms.subtopic import SubTopicForm
from django.core.paginator import *
from swift.constantvariables import PAGINATION_PERPAGE
from swift.models import Topic, Course, Subject, SubTopic
from swift.helper import renderfile, is_ajax, LogUserActivity
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db import transaction
from swift.models import CREATE, UPDATE, SUCCESS, FAILED, DELETE
from django.shortcuts import get_object_or_404, render


class SubtopicView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("search")  # search
        subjects = request.GET.get("subject")  # subject
        topics = request.GET.get("topic")  # topic
        condition = {"is_active": True}
        if query:  # search
            condition["name__icontains"] = query
        if topics:  # topic
            condition["topic_id"] = topics
        if subjects:  # subject
            condition["topic__subject__id"] = subjects
        subtopics = (
            SubTopic.objects.select_related("topic").filter(**condition).order_by("-id")
        )

        topic_list = Topic.objects.all()
        subject_list = Subject.objects.all()

        context = {}
        context["subjects"] = subject_list
        context["topics"] = topic_list

        try:
            page = int(request.GET.get("page", 1))
        except ValueError:
            page = 1

        paginator = Paginator(subtopics, PAGINATION_PERPAGE)
        try:
            subtopics = paginator.page(page)
        except PageNotAnInteger:
            subtopics = paginator.page(1)
        except EmptyPage:
            subtopics = paginator.page(paginator.num_pages)

        context["subtopics"], context["current_page"] = subtopics, page

        if is_ajax(request=request):
            response = {
                "status": True,
                "pagination": render_to_string(
                    "swift/subtopic/pagination.html", context=context, request=request
                ),
                "template": render_to_string(
                    "swift/subtopic/subtopic_list.html",
                    context=context,
                    request=request,
                ),
            }
            return JsonResponse(response)

        topic_id = request.GET.get("topic_id")
        topic = get_object_or_404(Topic, id=topic_id) if topic_id else None

        form = SubTopicForm(initial={"topic": topic})

        context["form"] = form
        return renderfile(request, "subtopic", "index", context)


class SubtopicCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = SubTopicForm()
        context = {"form": form, "id": 0}
        data = {
            "status": True,
            "title": "Add Subtopic",
            "template": render_to_string(
                "swift/subtopic/subtopic_form.html", context, request=request
            ),
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        form = SubTopicForm(request.POST)
        response = {}

        if form.is_valid():
            try:
                name = request.POST.get("name", None)
                topic = request.POST.get("topic", None)
                lessons = request.POST.get("lessons", None)
                objectives = request.POST.get("objectives", None)

                # CHECK THE DATA EXISTS
                if not Topic.objects.filter(name=name).exists():
                    obj = Topic.objects.create(
                        name=name,
                        topic_id=topic,
                        lessons=lessons,
                        objectives=objectives,
                    )

                    # log entry
                    log_data = {}
                    log_data["module_name"] = " Subtopic"
                    log_data["action_type"] = CREATE
                    log_data["log_message"] = "Subtopic Created"
                    log_data["status"] = SUCCESS
                    log_data["model_object"] = obj
                    log_data["db_data"] = {"name": name}
                    # log_data['db_data'] = {'course':course}

                    log_data["app_visibility"] = True
                    log_data["web_visibility"] = True
                    log_data["error_msg"] = ""
                    log_data["fwd_link"] = "/subtopic/"
                    LogUserActivity(request, log_data)

                    response["status"] = True
                    response["message"] = "Added successfully"
                else:
                    response["status"] = False
                    response["message"] = "Subtopic Already exists"

            except Exception as error:
                log_data = {}
                log_data["module_name"] = "Subtopic"
                log_data["action_type"] = CREATE
                log_data["log_message"] = "Subtopic updation failed"
                log_data["status"] = FAILED
                log_data["model_object"] = None
                log_data["db_data"] = {}
                log_data["app_visibility"] = False
                log_data["web_visibility"] = False
                log_data["error_msg"] = error
                log_data["fwd_link"] = "/subtopic/"
                LogUserActivity(request, log_data)

                response["status"] = False
                response["message"] = "Something went wrong"
        else:
            response["status"] = False
            context = {"form": form}
            response["title"] = "Add Subtopic"
            response["valid_form"] = False
            response["template"] = render_to_string(
                "swift/subtopic/subtopic_form.html", context, request=request
            )
        return JsonResponse(response)


class SubtopicUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)
        data = {}
        obj = get_object_or_404(SubTopic, id=id)
        form = SubTopicForm(instance=obj)
        context = {"form": form, "id": id, "course_id": obj.subject.course_id}
        data["status"] = True
        data["title"] = "Edit SubTopic"
        data["template"] = render_to_string(
            "swift/subtopic/subtopic_form.html", context, request=request
        )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data, response = {}, {}
        id = kwargs.get("pk", None)
        obj = get_object_or_404(SubTopic, id=id)
        previous_name = obj.name
        form = SubTopicForm(request.POST or None, instance=obj)

        if form.is_valid():
            try:
                with transaction.atomic():
                    if (
                        SubTopic.objects.filter(
                            name__icontains=request.POST.get("name")
                        )
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


class SubtopicDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)
        response = {}
        obj = get_object_or_404(SubTopic, id=id)
        obj.is_active = False
        obj.save()

        # log entry
        log_data = {}
        log_data["module_name"] = "Topic"
        log_data["action_type"] = DELETE
        log_data["log_message"] = f"Deleted SubTopic {obj.name}"
        log_data["status"] = SUCCESS
        log_data["model_object"] = None
        log_data["db_data"] = {"name": obj.name}
        log_data["app_visibility"] = True
        log_data["web_visibility"] = True
        log_data["error_msg"] = ""
        log_data["fwd_link"] = "/SubTopic/"
        LogUserActivity(request, log_data)

        response["status"] = True
        response["message"] = "SubTopic deleted successfully"
        return JsonResponse(response)


class FilteredTopicView(View):
    def get(self, request):
        course_id = request.GET.get("course_id")
        subjects = Subject.objects.filter(course_id=course_id)
        subject_list = [
            {"id": subject.id, "name": subject.name} for subject in subjects
        ]
        return JsonResponse({"subjects": subject_list})

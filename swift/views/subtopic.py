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
        query = request.GET.get("search")
        subjects = request.GET.get("subject")
        topics = request.GET.get("topic")
        condition = {"is_active": True}

        if query:
            condition["name__icontains"] = query
        if topics:
            condition["topic_id"] = topics
        if subjects:
            condition["topic__subject__id"] = subjects

        subtopics = (
            SubTopic.objects.select_related("topic").filter(**condition).order_by("-id")
        )

        topic_list = Topic.objects.all()
        subject_list = Subject.objects.all()

        if subjects:
            topic_list = topic_list.filter(subject_id=subjects)

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

        subject_id = request.GET.get("subject_id")
        subject = get_object_or_404(Subject, id=subject_id) if subject_id else None

        form = SubTopicForm(initial={"subject": subject})


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
        response = {}
        form = SubTopicForm(request.POST or None)
        if form.is_valid():
            try:
                # with transaction.atomic():
                name = request.POST.get("name", None)
                topic = request.POST.get("topic", None)
                lessons = request.POST.get("lessons", None)
                objectives = request.POST.get("objectives", None)
                
                # CHECK THE DATA EXISTS
                if not SubTopic.objects.filter(name=name).exists():
                    obj = SubTopic.objects.create(
                         name=name, topic_id=topic,lessons_id=lessons,objectives_id=objectives
                     )

                    # log entry
                    log_data = {}
                    log_data["module_name"] = "SubTopic"
                    log_data["action_type"] = CREATE
                    log_data["log_message"] = "SubTopic Created"
                    log_data["status"] = SUCCESS
                    log_data["model_object"] = obj
                    log_data["db_data"] = {"name": name}
                    log_data["app_visibility"] = True
                    log_data["web_visibility"] = True
                    log_data["error_msg"] = ""
                    log_data["fwd_link"] = "/subtopic/"
                    LogUserActivity(request, log_data)

                    response["status"] = True
                    response["message"] = "Added successfully"
                else:
                    response["status"] = False
                    response["message"] = "Topic Already exists"

            except Exception as error:
                log_data = {}
                log_data["module_name"] = "SubTopic"
                log_data["action_type"] = CREATE
                log_data["log_message"] = "SubTopic updation failed"
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
            response["title"] = "Add SubTopic"
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
        context = {"form": form, "id": id}
        data["status"] = True
        data["title"] = "Edit SubTopic"
        data["template"] = render_to_string(
            "swift/subtopic/subtopic_form.html", context, request=request
        )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
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
                        data["status"] = False
                        data["message"] = "Name already exists"
                        return JsonResponse(data)

                    obj = form.save()

                    # log entry
                    log_data = {
                        "module_name": "SubTopic",
                        "action_type": "UPDATE",
                        "log_message": "SubTopic Updated",
                        "status": "SUCCESS",
                        "model_object": obj,
                        "db_data": {
                            "previous_name": previous_name,
                            "updated_name": obj.name,
                        },
                        "app_visibility": True,
                        "web_visibility": True,
                        "error_msg": "",
                        "fwd_link": "/topic/",
                    }
                    LogUserActivity(request, log_data)

                    data["status"] = True
                    data["message"] = "SubTopic updated successfully"
                    return JsonResponse(data)
            except Exception as dberror:
                log_data = {
                    "module_name": "SubTopic",
                    "action_type": "UPDATE",
                    "log_message": "SubTopic updation failed",
                    "status": "FAILED",
                    "model_object": None,
                    "db_data": {},
                    "app_visibility": False,
                    "web_visibility": False,
                    "error_msg": str(dberror),
                    "fwd_link": "/topic/",
                }
                LogUserActivity(request, log_data)

                data["message"] = "Something went wrong"
                data["status"] = True
        else:
            data["status"] = False
            context = {"form": form, "id": id}
            data["title"] = "Edit SubTopic"
            data["valid_form"] = False
            data["template"] = render_to_string(
                "swift/subtopic/subtopic_form.html", context, request=request
            )
            return JsonResponse(data)



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

# add filter
class FilteredSubtopicView(View):
    def get(self, request):
        course_id = request.GET.get("course_id")
        subject_id = request.GET.get("subject_id")

        if course_id and subject_id:
            subtopics = SubTopic.objects.filter(
                topic__subject__course_id=course_id,
                topic__subject_id=subject_id
            )
        else:
            subtopics = SubTopic.objects.none()

        subtopic_list = [
            {"id": subtopic.id, "name": subtopic.name} for subtopic in subtopics
        ]
        return JsonResponse({"subtopics": subtopic_list})

# searchfilter
class FilteredTopicsView(View):
    def get(self, request):
        subject_id = request.GET.get("subject_id")
        subject = get_object_or_404(Subject, id=subject_id) if subject_id else None
        course_id = subject.course_id
        topics = Topic.objects.filter(subject_id=subject_id, subject__course_id=course_id)
        topic_list = [{'id': topic.id, 'name': topic.name} for topic in topics]
        return JsonResponse({'topics': topic_list})
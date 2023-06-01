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
        courses = request.GET.get("course")
        subjects = request.GET.get("subject")
        topics = request.GET.get("topic")
        condition = {"is_active": True}

        if query:
            condition["name__icontains"] = query
        if topics:
            condition["topic_id"] = topics
        if subjects:
            condition["topic__subject__id"] = subjects
        if courses:
            condition["topic__subject__course__id"] = courses    
            

        subtopics = (
            SubTopic.objects.select_related("topic").filter(**condition).order_by("-id")
        )

        topic_list = Topic.objects.all()
        subject_list = Subject.objects.all()
        course_list = Course.objects.all()
        

        if subjects:
            topic_list = topic_list.filter(subject_id=subjects)
        if courses:
            subject_list = subject_list.filter(course_id=courses)
            
        context = {}
        context["subjects"] = subject_list
        context["topics"] = topic_list
        context["courses"] = course_list
        

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
            "template": render_to_string("swift/subtopic/subtopic_form.html", context, request=request),
        }
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        response = {}
        form = SubTopicForm(request.POST or None)
        if form.is_valid():
            try:
                subtopic = form.save()
                # log entry
                log_data = {
                    "module_name": "SubTopic",
                    "action_type": "CREATE",
                    "log_message": "SubTopic Created",
                    "status": "SUCCESS",
                    "model_object": str(subtopic),
                    "db_data": {"name": subtopic.name},
                    "app_visibility": True,
                    "web_visibility": True,
                    "error_msg": "",
                    "fwd_link": "/subtopic/",
                }
                LogUserActivity(request, log_data)

                response["status"] = True
                response["message"] = "Added successfully"
            except Exception as error:
                log_data = {
                    "module_name": "SubTopic",
                    "action_type": "CREATE",
                    "log_message": "SubTopic creation failed",
                    "status": "FAILED",
                    "model_object": None,
                    "db_data": {},
                    "app_visibility": False,
                    "web_visibility": False,
                    "error_msg": str(error),
                    "fwd_link": "/subtopic/",
                }
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

class SubtopicUpdate(View):
    def get(self, request, *args, **kwargs):
        data = {}
        id = kwargs.get("pk")
        obj = get_object_or_404(SubTopic, id=id)
        form = SubTopicForm(instance=obj)
        subject_id = obj.topic.subject_id if obj.topic and obj.topic.subject_id else None
        topic_id = obj.topic_id if obj.topic else None
        context = {"form": form, "id": id, "subject_id": subject_id, "topic_id": topic_id}
        data["status"] = True
        data["title"] = "Edit SubTopic"
        data["course_id"] = obj.topic.subject.course_id if obj.topic and obj.topic.subject else None
        data["subject_id"] = subject_id
        data["topic_id"] = topic_id
        data["template"] = render_to_string("swift/subtopic/subtopic_form.html", context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data, response = {}, {}
        id = kwargs.get("pk")
        obj = get_object_or_404(SubTopic, id=id)
        previous_name = obj.name
        previous_lessons = obj.lessons
        previous_objectives = obj.objectives
        form = SubTopicForm(request.POST, instance=obj)

        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                topic_id = request.POST.get("topic", None)
                topic = get_object_or_404(Topic, id=topic_id)
                lessons = form.cleaned_data['lessons']
                objectives = form.cleaned_data['objectives']

                if not SubTopic.objects.filter(name=name, topic=topic).exclude(id=id).exists():
                    obj.name = name
                    obj.topic = topic
                    obj.lessons = lessons
                    obj.objectives = objectives
                    obj.save()

                    # log entry
                    log_data = {
                        "module_name": "SubTopic",
                        "action_type": "UPDATE",
                        "log_message": "SubTopic Updated",
                        "status": "SUCCESS",
                        "model_object": str(obj),
                        "db_data": {
                            "previous_name": previous_name,
                            "previous_lessons": previous_lessons,
                            "previous_objectives": previous_objectives,
                            "updated_name": name,
                            "updated_lessons": lessons,
                            "updated_objectives": objectives,
                        },
                        "app_visibility": True,
                        "web_visibility": True,
                        "error_msg": "",
                        "fwd_link": "/subtopic/",
                    }
                    LogUserActivity(request, log_data)

                    response["status"] = True
                    response["message"] = "Subtopic updated successfully"
                else:
                    response["status"] = False
                    response["message"] = "Subtopic already exists"

            except Exception as error:
                print(f"Error: {str(error)}")
                log_data = {
                    "module_name": "SubTopic",
                    "action_type": "UPDATE",
                    "log_message": "SubTopic updation failed",
                    "status": "FAILED",
                    "model_object": None,
                    "db_data": {},
                    "app_visibility": False,
                    "web_visibility": False,
                    "error_msg": str(error),
                    "fwd_link": "/subtopic/",
                }
                LogUserActivity(request, log_data)

                response["status"] = False
                response["message"] = "Something went wrong"
        else:
            response["status"] = False
            context = {"form": form, "id": id}
            response["title"] = "Edit Subtopic"
            response["valid_form"] = False
            response["template"] = render_to_string("swift/subtopic/subtopic_form.html", context, request=request)

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




class FilterSubjectsView(View):
    def get(self, request, *args, **kwargs):
        topic_id = request.GET.get("topic")
        course_id = request.GET.get("course")

        if topic_id:
            subjects = Subject.objects.filter(topic_id=topic_id).values("id", "name")
        elif course_id:
            subjects = Subject.objects.filter(course_id=course_id).values("id", "name")
        else:
            subjects = []

        data = {"subjects": list(subjects)}
        return JsonResponse(data)


class FilterTopicsView(View):
    def get(self, request, *args, **kwargs):
        subject_id = request.GET.get("subject")
        course_id = request.GET.get("course")

        if subject_id:
            topics = Topic.objects.filter(subject_id=subject_id).values("id", "name")
        elif course_id:
            topics = Topic.objects.filter(subject__course_id=course_id).values("id", "name")
        else:
            topics = []

        data = {"topics": list(topics)}
        return JsonResponse(data)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# ----------------------------------------------searchfilter---------------------------------------------------
class FiltersearchSubjectsView(View):
    def get(self, request):
        course_id = request.GET.get("course")

        if course_id:
            subjects = Subject.objects.filter(course_id=course_id).values("id", "name")
        else:
            subjects = Subject.objects.all().values("id", "name")

        subject_list = list(subjects)

        return JsonResponse({"subjects": subject_list})

class FiltersearchCoursesView(View):
    def get(self, request):
        courses = Course.objects.all().values("id", "name")
        course_list = list(courses)
        return JsonResponse({"courses": course_list})
    
class FiltersearchTopicsView(View):
    def get(self, request):
        subject_id = request.GET.get("subject")
        course_id = request.GET.get("course")

        if subject_id:
            topics = Topic.objects.filter(subject_id=subject_id).values("id", "name")
        elif course_id:
            topics = Topic.objects.filter(subject__course_id=course_id).values("id", "name")
        else:
            topics = Topic.objects.all().values("id", "name")

        topic_list = list(topics)

        return JsonResponse({"topics": topic_list})

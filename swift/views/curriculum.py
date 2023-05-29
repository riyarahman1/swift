from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from swift.forms.curriculum import CurriculumForm
from swift.helper import renderfile, is_ajax, LogUserActivity
from swift.models import Curriculum
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import *
from swift.constantvariables import PAGINATION_PERPAGE
from django.shortcuts import get_object_or_404
from swift.models import CREATE, UPDATE, SUCCESS, FAILED, DELETE, READ
from django.db import transaction


class CurriculumView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context, response = {}, {}
        page = int(request.GET.get("page", 1))
        curriculums = Curriculum.objects.filter(is_active=True).order_by("-id")

        paginator = Paginator(curriculums, PAGINATION_PERPAGE)
        try:
            curriculums = paginator.page(page)
        except PageNotAnInteger:
            curriculums = paginator.page(1)
        except EmptyPage:
            curriculums = paginator.page(paginator.num_pages)

        context["curriculums"], context["current_page"] = curriculums, page
        if is_ajax(request=request):
            response["status"] = True
            response["pagination"] = render_to_string(
                "swift/curriculum/pagination.html", context=context, request=request
            )
            response["template"] = render_to_string(
                "swift/curriculum/curriculum_list.html", context, request=request
            )
            return JsonResponse(response)
        context["form"] = CurriculumForm()
        return renderfile(request, "curriculum", "index", context)


class CurriculumCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = CurriculumForm()
        context = {"form": form, "id": 0}
        data["status"] = True
        data["title"] = "Add Curriculum"
        data["template"] = render_to_string(
            "swift/curriculum/curriculum_form.html", context, request=request
        )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        response = {}
        form = CurriculumForm(request.POST or None)
        if form.is_valid():
            try:
                with transaction.atomic():
                    name = request.POST.get("name", None)
                    # CHECK THE DATA EXISTS
                    if not Curriculum.objects.filter(name=name).exists():
                        obj = Curriculum.objects.create(name=name)

                        # log entry
                        log_data = {}
                        log_data["module_name"] = "Curriculum"
                        log_data["action_type"] = CREATE
                        log_data["log_message"] = "Curriculum Created"
                        log_data["status"] = SUCCESS
                        log_data["model_object"] = obj
                        log_data["db_data"] = {"name": name}
                        log_data["app_visibility"] = True
                        log_data["web_visibility"] = True
                        log_data["error_msg"] = ""
                        log_data["fwd_link"] = "/curriculum/"
                        LogUserActivity(request, log_data)

                        response["status"] = True
                        response["message"] = "Added successfully"
                    else:
                        response["status"] = False
                        response["message"] = "Curriculum Already exists"

            except Exception as error:
                log_data = {}
                log_data["module_name"] = "Curriculum"
                log_data["action_type"] = CREATE
                log_data["log_message"] = "Curriculum updation failed"
                log_data["status"] = FAILED
                log_data["model_object"] = None
                log_data["db_data"] = {}
                log_data["app_visibility"] = False
                log_data["web_visibility"] = False
                log_data["error_msg"] = error
                log_data["fwd_link"] = "/curriculum/"
                LogUserActivity(request, log_data)

                response["status"] = False
                response["message"] = "Something went wrong"
        else:
            response["status"] = False
            context = {"form": form}
            response["title"] = "Edit Curriculum"
            response["valid_form"] = False
            response["template"] = render_to_string(
                "swift/curriculum/curriculum_form.html", context, request=request
            )
        return JsonResponse(response)


class CurriculumUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)
        data = {}
        obj = get_object_or_404(Curriculum, id=id)
        form = CurriculumForm(instance=obj)
        context = {"form": form, "id": id}
        data["status"] = True
        data["title"] = "Edit Curriculum"
        data["template"] = render_to_string(
            "swift/curriculum/curriculum_form.html", context, request=request
        )
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data, response = {}, {}
        id = kwargs.get("pk", None)
        obj = get_object_or_404(Curriculum, id=id)
        previous_name = obj.name
        form = CurriculumForm(request.POST or None, instance=obj)

        if form.is_valid():
            try:
                with transaction.atomic():
                    if (
                        Curriculum.objects.filter(
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
                    log_data["module_name"] = "Curriculum"
                    log_data["action_type"] = UPDATE
                    log_data["log_message"] = "Curriculum Updated"
                    log_data["status"] = SUCCESS
                    log_data["model_object"] = obj
                    log_data["db_data"] = {
                        "previous_name": previous_name,
                        "updated_name": obj.name,
                    }
                    log_data["app_visibility"] = True
                    log_data["web_visibility"] = True
                    log_data["error_msg"] = ""
                    log_data["fwd_link"] = "/curriculum/"
                    LogUserActivity(request, log_data)

                    response["status"] = True
                    response["message"] = "Curriculum updated successfully"
                    return JsonResponse(response)

            except Exception as dberror:
                log_data = {}
                log_data["module_name"] = "Curriculum"
                log_data["action_type"] = UPDATE
                log_data["log_message"] = "Curriculum updation failed"
                log_data["status"] = FAILED
                log_data["model_object"] = None
                log_data["db_data"] = {}
                log_data["app_visibility"] = False
                log_data["web_visibility"] = False
                log_data["error_msg"] = dberror
                log_data["fwd_link"] = "/curriculum/"
                LogUserActivity(request, log_data)

                response["message"] = "Something went wrong"
                response["status"] = True
        else:
            response["status"] = False
            context = {"form": form}
            response["title"] = "Edit Curriculum"
            response["valid_form"] = False
            response["template"] = render_to_string(
                "swift/curriculum/curriculum_form.html", context, request=request
            )
            return JsonResponse(response)


class CurriculumDelete(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk", None)
        response = {}
        obj = get_object_or_404(Curriculum, id=id)
        obj.is_active = False
        obj.save()

        # log entry
        log_data = {}
        log_data["module_name"] = "Curriculum"
        log_data["action_type"] = DELETE
        log_data["log_message"] = f"Deleted Curriculum {obj.name}"
        log_data["status"] = SUCCESS
        log_data["model_object"] = None
        log_data["db_data"] = {"name": obj.name}
        log_data["app_visibility"] = True
        log_data["web_visibility"] = True
        log_data["error_msg"] = ""
        log_data["fwd_link"] = "/Curriculum/"
        LogUserActivity(request, log_data)

        response["status"] = True
        response["message"] = "Curriculum deleted successfully"
        return JsonResponse(response)

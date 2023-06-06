from django.urls import path
from swift.views.account import (
    SignIn,
    Home,
    SignOut,
    ForgotPassword,
)

from swift.views.curriculum import (
    CurriculumView,
    CurriculumCreate,
    CurriculumUpdate,
    CurriculumDelete,
)

from swift.views.course import (
    CourseView,
    CourseCreate,
    CourseUpdate,
    CourseDelete,
)


from swift.views.subject import (
    SubjectsView,
    SubjectCreate,
    SubjectUpdate,
    SubjectDelete,
)

from swift.views.topic import (
    TopicView,
    TopicCreate,
    TopicUpdate,
    TopicDelete,
    # FilteredSubjectsView,
    GetSubjectsView,
)

from swift.views.subtopic import (
    SubtopicView,
    SubtopicCreate,
    SubtopicUpdate,
    SubtopicDelete,
    FiltersearchSubjectsView,
    FiltersearchTopicsView,
    FiltersearchCoursesView,
)

app_name = "appswift"
# views
urlpatterns = [
    # Landing Page
    path("", SignIn.as_view(), name="signin"),
    path("home/", Home.as_view(), name="home"),
    # Login Actions
    path("signin/", SignIn.as_view(), name="signin"),
    path("forgot-password/", ForgotPassword.as_view(), name="forgot_password"),
    path("signout/", SignOut.as_view(), name="signout"),
    # Curriculum
    path("curriculum/", CurriculumView.as_view(), name="curriculum"),
    path("curriculum/create/", CurriculumCreate.as_view(), name="create_curriculum"),
    path(
        "curriculum/<int:pk>/update/",
        CurriculumUpdate.as_view(),
        name="update_curriculum",
    ),
    path(
        "curriculum/<int:pk>/delete/",
        CurriculumDelete.as_view(),
        name="delete_curriculum",
    ),
    # Course
    path("course/", CourseView.as_view(), name="course"),
    path("course/create/", CourseCreate.as_view(), name="create_course"),
    path("course/<int:pk>/update/", CourseUpdate.as_view(), name="update_course"),
    path("course/<int:pk>/delete/", CourseDelete.as_view(), name="delete_course"),
    # Subject
    path("subject/", SubjectsView.as_view(), name="subject"),
    path("subject/create/", SubjectCreate.as_view(), name="create_subject"),
    path("subject/<int:pk>/update/", SubjectUpdate.as_view(), name="update_subject"),
    path("subject/<int:pk>/delete/", SubjectDelete.as_view(), name="delete_subject"),
    # Topic
    path("topic/", TopicView.as_view(), name="topic"),
    path("topic/create/", TopicCreate.as_view(), name="create_topic"),
    path("topic/<int:pk>/update/", TopicUpdate.as_view(), name="update_topic"),
    path("topic/<int:pk>/delete/", TopicDelete.as_view(), name="delete_topic"),
    path("topic/searchfilter/", GetSubjectsView.as_view(), name="searchfilter_topic"),
    # Subtopic
    path("subtopic/", SubtopicView.as_view(), name="subtopic"),
    path("subtopic/create/", SubtopicCreate.as_view(), name="create_subtopic"),
    path("subtopic/<int:pk>/update/", SubtopicUpdate.as_view(), name="update_subtopic"),
    path("subtopic/<int:pk>/delete/", SubtopicDelete.as_view(), name="delete_subtopic"),
    # search filter in subtopic
    path(
        "filter_subjects/", FiltersearchSubjectsView.as_view(), name="filter_subjects"
    ),
    path("filter_topics/", FiltersearchTopicsView.as_view(), name="filter_topics"),
    path("filter_courses/", FiltersearchCoursesView.as_view(), name="filter_courses"),
]

from django.contrib import admin
from .models import Curriculum,Course,Subject,Topic,SubTopic
# Register your models here.

admin.site.register(Curriculum)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Topic)
admin.site.register(SubTopic)


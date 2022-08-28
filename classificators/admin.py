from django.contrib import admin
from .models import Project, UserGroup, UserTag

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('caption', 'description')
    search_fields = ('caption', 'description')
    readonly_fields = ('id',)

class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('caption', 'description')
    search_fields = ('caption', 'description')
    readonly_fields = ('id',)

class UserTagAdmin(admin.ModelAdmin):
    list_display = ('caption', 'description')
    search_fields = ('caption', 'description')
    readonly_fields = ('id',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(UserGroup, UserGroupAdmin)
admin.site.register(UserTag, UserTagAdmin)
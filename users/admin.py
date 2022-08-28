from django.contrib import admin
from .models import UserData, PersonalInfo, TelegramUser, SystemUser

# list_display = _()
# search_fields = _()
# list_filter = _()

class UserDataAdmin(admin.ModelAdmin):
    list_display = ('uFullName', 'uEmail', 'uID')
    search_fields = ('uID', 'uFullName', 'uEmail')

class SystemUserAdmin(admin.ModelAdmin):
    list_display = ('keyUser', 'uLogin')
    search_fields = ('keyUser', 'uLogin')

class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('keyUser', 'uNickName', 'uTelegramID')
    search_fields = ('keyUser', 'uNickName', 'uTelegramID')

admin.site.register(UserData, UserDataAdmin)
admin.site.register(PersonalInfo)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(SystemUser, SystemUserAdmin)

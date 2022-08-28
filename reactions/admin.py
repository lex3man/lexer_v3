from django.contrib import admin
from .models import Command, Answer, Keyboard, KeyboardButton, State

class CommandAdmin(admin.ModelAdmin):
    list_display = ('caption', 'bot')
    list_filter = ('caption', 'bot')
    
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('bot', 'state', 'answer_id', 'text')
    list_filter = ('bot', 'state')
    search_fields = ('text', 'answer_id')

admin.site.register(Answer, AnswerAdmin)
admin.site.register(State)
admin.site.register(Keyboard)
admin.site.register(KeyboardButton)
admin.site.register(Command, CommandAdmin)
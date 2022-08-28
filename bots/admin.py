from django.contrib import admin
from .models import TelegramBot

# Register your models here.
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ('caption', 'tg_id', 'url', 'active')
    search_fields = ('caption', 'tg_id', 'url')
    actions = [TelegramBot.start, TelegramBot.stop]
    readonly_fields = ('active', 'tg_id')
    list_filter = ('active',)

admin.site.register(TelegramBot, TelegramBotAdmin)
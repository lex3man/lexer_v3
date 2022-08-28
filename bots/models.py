from django.db import models
from django.contrib import admin
from classificators.models import Project
from .telegram_bot_controller.bots_manager import BotHandler, active_bots
import redis

system_data_cache = redis.Redis(db=0)
bots_status = redis.Redis(db=1)

class TelegramBot(models.Model):
    project = models.ForeignKey(Project, verbose_name='Проект', null=True, on_delete=models.SET_NULL)
    caption = models.CharField(verbose_name='Название бота', max_length=100, unique=True)
    tg_id = models.CharField(verbose_name='Telegram ID бота', max_length=15, unique=True, null=True)
    token = models.CharField(verbose_name='Токен', max_length=50, unique=True)
    url = models.CharField(verbose_name='Ссылка на бота', max_length=100,unique=True)
    active = models.BooleanField(verbose_name='Работает', default=False)

    class Meta:
        verbose_name = 'Телеграм бот'
        verbose_name_plural = 'Телеграм боты'

    def __str__(self):
        return self.caption

    @admin.action(description = 'Запустить выбранных ботов')
    def start(self, request, queryset):
        # queryset.update(active = True)
        for b in queryset:
            if b.active == False:
                try:
                    if bots_status[b.caption] == 'on': continue
                except: pass
                bot = BotHandler(b.token, b.caption)
                active_bots.update({b.caption:bot})
                bot.start_aiogram_app()
                b.active = True
                b.save()

    @admin.action(description = 'Остановить выбранных ботов')
    def stop(self, request, queryset):
        # queryset.update(active = False)
        for b in queryset:
            if b.active:
                try:
                    bot = active_bots.pop(b.caption)
                    bot.bot_down()
                except: BotHandler.kill(b.caption)
                b.active = False
                b.save()
from django.db import models
import uuid
import random, string

def idGenerate(lenght: int):
    sights = string.digits + string.ascii_lowercase
    return ''.join(random.choices(sights, k = lenght))

class Project(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    caption = models.CharField(verbose_name='Название проекта', max_length=100)
    description = models.TextField(verbose_name='Описание', null=True)
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
    
    def __str__(self):
        return self.caption

class UserGroup(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    project = models.ForeignKey(Project, verbose_name='Группа пользователей проекта', on_delete=models.CASCADE)
    caption = models.CharField(verbose_name='Название группы', max_length=100)
    description = models.TextField(verbose_name='Описание', null=True)

    class Meta:
        verbose_name = 'Группа пользователей'
        verbose_name_plural = 'Группы пользователей'
    
    def __str__(self):
        return self.caption

class UserTag(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4)
    project = models.ForeignKey(Project, verbose_name='Тэг проекта', on_delete=models.CASCADE)
    caption = models.CharField(verbose_name='Название тэга', max_length=100)
    description = models.TextField(verbose_name='Описание', null=True)
    priority = models.IntegerField(verbose_name='Приоритет учёта тэга (чем больше, тем приоритетнее)', default=1)

    class Meta:
        verbose_name = 'Тэг пользователей'
        verbose_name_plural = 'Тэги пользователей'
    
    def __str__(self):
        return self.caption
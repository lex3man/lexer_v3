from django.db import models
from classificators.models import Project, UserGroup, UserTag

class UserData(models.Model):
    uID = models.CharField(verbose_name='ID Пользователя', max_length=50, unique=True)
    uFirstName = models.CharField(verbose_name='Имя', max_length=50, null=True)
    uLastName = models.CharField(verbose_name='Фамилия', max_length=100, null=True)
    uFullName = models.CharField(verbose_name='Полное имя', max_length=150)
    uEmail = models.CharField(verbose_name='Адрес электронной почты', max_length=100, null=True)
    from_project = models.ForeignKey(Project, verbose_name='Проект', on_delete=models.DO_NOTHING, null=True, blank=True)
    groups = models.ManyToManyField(UserGroup, verbose_name='Группы', blank=True)
    tags = models.ManyToManyField(UserTag, verbose_name='Тэги', blank=True)
    
    class Meta:
        verbose_name_plural = 'Собеседники'
        verbose_name = 'Собеседник'
    
    def __str__(self) -> str:
        return f'{self.uFullName} ({self.uEmail} / id {self.uID})'

class SystemUser(models.Model):
    keyUser = models.ForeignKey(UserData, verbose_name='Собеседник', on_delete=models.CASCADE)
    uLogin = models.CharField(verbose_name='Логин', max_length=100, unique=True)
    uPasswd = models.CharField(verbose_name='Пароль', max_length=150, editable=False, null=True)
    
    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
    
    def __str__(self):
        return self.keyUser.__str__()
    
class PersonalInfo(models.Model):
    GEND = [('male', 'Мужской'), ('female', 'Женский'), ('notset','Не указан')]
    
    keyUser = models.ForeignKey(UserData, verbose_name='Собеседник', on_delete=models.CASCADE)
    uPhoneNumber = models.CharField(verbose_name='Номер телефона', max_length=50, unique=True)
    uGender = models.CharField(verbose_name='Пол', max_length=10, choices=GEND, default='notset')
    
    class Meta:
        verbose_name = 'Дополнительная информация'
        verbose_name_plural = 'Дополнительная информация'
    
    def __str__(self):
        return self.keyUser.__str__()
    
class TelegramUser(models.Model):
    keyUser = models.ForeignKey(UserData, verbose_name='Собеседник', on_delete=models.CASCADE)
    uNickName = models.CharField(verbose_name='Никнейм', max_length=100)
    uTelegramID = models.CharField(verbose_name='Телеграм ID', max_length=50, unique=True)
    
    class Meta:
        verbose_name = 'Данные телеграм'
        verbose_name_plural = 'Данные телеграм'
    
    def __str__(self):
        return self.keyUser.__str__()
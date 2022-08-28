from django.db import models
from classificators.models import UserTag, UserGroup
from bots.models import TelegramBot

LANG_CHOICES = [
        ('RUS', 'Русский'),
        ('ENG', 'English'),
        ('TUR', 'Turkish'),
        ('GER', 'German'),
        ('FR', 'Frankish'),
    ]

class State(models.Model):
    bot = models.ForeignKey(TelegramBot, verbose_name='Бот', on_delete=models.CASCADE)
    stateID = models.CharField(verbose_name='ID', max_length=50, unique=True)
    caption = models.CharField(verbose_name='Наименование', max_length=100, unique=True)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    
    def __str__(self):
        return self.caption

class KeyboardButton(models.Model):
    caption = models.CharField(verbose_name = 'Наименование', max_length = 50, unique = True)
    text = models.CharField(verbose_name = 'Текст кнопки', max_length = 50)
    order = models.IntegerField(verbose_name = 'Номер строки размещения кнопки', default = 1)
    
    class Meta:
        verbose_name = 'Кнопка клавиатуры'
        verbose_name_plural = 'Кнопки для клавиатур'
    
    def __str__(self):
        return self.text

class Keyboard(models.Model):
    KB_TYPES = [
        ('std', 'Стандартная'),
        ('inl', 'Инлайн'),
    ]
    type = models.CharField(verbose_name='Тип клавиатуры', max_length=5, choices=KB_TYPES, default='std')
    caption = models.CharField(verbose_name = 'Наименование', max_length = 50)
    name = models.CharField(verbose_name = 'Имя переменной клавиатуры', max_length = 50, unique = True)
    buttons = models.ManyToManyField(KeyboardButton, verbose_name = 'Кнопки', related_query_name = 'keyboard')
    
    class Meta:
        verbose_name = 'Клавиатура'
        verbose_name_plural = 'Клавиатуры'
    
    def __str__(self):
        return self.name

class Answer(models.Model):
    CHANGES = [
        ('NONE', 'Без изменений'),
        ('ADD', 'Добавить'),
        ('REM', 'Удалить')
    ]
    
    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    bot = models.ForeignKey(TelegramBot, verbose_name='Бот', on_delete=models.CASCADE)
    state = models.ForeignKey(State, verbose_name='Позиция', on_delete=models.SET_NULL, null=True)
    answer_id = models.CharField(verbose_name='Идентификатор', max_length=50, unique=True, default='new_state')
    from_button = models.ForeignKey(KeyboardButton, verbose_name='По кнопке', on_delete=models.SET_NULL, null=True)
    text = models.TextField(verbose_name='Текст реакции (не обязательно)', null=True, blank=True)
    delay = models.IntegerField(verbose_name='Задержка реакции, сек', default=0)
    keyboard = models.ForeignKey(Keyboard, verbose_name='Клавиатура', on_delete=models.SET_NULL, null=True)
    jump_to = models.ForeignKey('self', verbose_name='Автопереход', on_delete=models.SET_NULL, null=True)
    tag_action = models.CharField(verbose_name='Тэги пользователя', max_length=5, choices = CHANGES, default='NONE')
    tags = models.ManyToManyField(UserTag, verbose_name='')
    
    class Meta:
        verbose_name = 'Ответ бота'
        verbose_name_plural = 'Ответы'
    
    def __str__(self):
        return self.caption

class Command(models.Model):
    bot = models.ForeignKey(TelegramBot, verbose_name='Бот', on_delete=models.CASCADE)
    caption = models.CharField(verbose_name='Текст команды (start, напимер)', max_length=100)
    text = models.TextField(verbose_name='Текст реакции на команду (не обязательно)', null=True, blank=True)
    delay = models.IntegerField(verbose_name='Задержка реакции, сек', default=0)
    keyboard = models.ForeignKey(Keyboard, verbose_name='Клавиатура', on_delete=models.SET_NULL, null=True, blank=True)
    jump_to = models.ForeignKey(Answer, verbose_name='Автопереход', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
    
    def __str__(self):
        return self.caption
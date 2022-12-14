# Generated by Django 4.0.6 on 2022-07-25 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classificators', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uID', models.CharField(max_length=50, unique=True, verbose_name='ID Пользователя')),
                ('uFirstName', models.CharField(max_length=50, null=True, verbose_name='Имя')),
                ('uLastName', models.CharField(max_length=100, null=True, verbose_name='Фамилия')),
                ('uFullName', models.CharField(max_length=150, verbose_name='Полное имя')),
                ('uEmail', models.CharField(max_length=100, null=True, verbose_name='Адрес электронной почты')),
                ('from_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='classificators.project', verbose_name='Проект')),
                ('groups', models.ManyToManyField(blank=True, to='classificators.usergroup', verbose_name='Группы')),
                ('tags', models.ManyToManyField(blank=True, to='classificators.usertag', verbose_name='Тэги')),
            ],
            options={
                'verbose_name': 'Собеседник',
                'verbose_name_plural': 'Собеседники',
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uNickName', models.CharField(max_length=100, verbose_name='Никнейм')),
                ('uTelegramID', models.CharField(max_length=50, unique=True, verbose_name='Телеграм ID')),
                ('keyUser', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.userdata', verbose_name='Собеседник')),
            ],
            options={
                'verbose_name': 'Данные телеграм',
                'verbose_name_plural': 'Данные телеграм',
            },
        ),
        migrations.CreateModel(
            name='SystemUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uLogin', models.CharField(max_length=100, unique=True, verbose_name='Логин')),
                ('uPasswd', models.CharField(editable=False, max_length=150, null=True, verbose_name='Пароль')),
                ('keyUser', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.userdata', verbose_name='Собеседник')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uPhoneNumber', models.CharField(max_length=50, unique=True, verbose_name='Номер телефона')),
                ('uGender', models.CharField(choices=[('male', 'Мужской'), ('female', 'Женский'), ('notset', 'Не указан')], default='notset', max_length=10, verbose_name='Пол')),
                ('keyUser', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.userdata', verbose_name='Собеседник')),
            ],
            options={
                'verbose_name': 'Дополнительная информация',
                'verbose_name_plural': 'Дополнительная информация',
            },
        ),
    ]

# Generated by Django 4.0.6 on 2022-08-01 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0003_telegrambot_tg_id'),
        ('classificators', '0001_initial'),
        ('reactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyboardButton',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=50, unique=True, verbose_name='Наименование')),
                ('language', models.CharField(choices=[('RUS', 'Русский'), ('ENG', 'English'), ('TUR', 'Turkish'), ('GER', 'German'), ('FR', 'Frankish')], default='RUS', max_length=5, verbose_name='Язык перевода')),
                ('text', models.CharField(max_length=50, verbose_name='Текст кнопки')),
                ('order', models.IntegerField(default=1, verbose_name='Номер строки размещения кнопки')),
            ],
            options={
                'verbose_name': 'Кнопка клавиатуры',
                'verbose_name_plural': 'Кнопки для клавиатур',
            },
        ),
        migrations.RemoveField(
            model_name='command',
            name='project',
        ),
        migrations.CreateModel(
            name='Keyboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=50, verbose_name='Наименование')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Имя переменной клавиатуры')),
                ('language', models.CharField(choices=[('RUS', 'Русский'), ('ENG', 'English'), ('TUR', 'Turkish'), ('GER', 'German'), ('FR', 'Frankish')], default='RUS', max_length=5, verbose_name='Язык перевода')),
                ('buttons', models.ManyToManyField(related_query_name='keyboard', to='reactions.keyboardbutton', verbose_name='Кнопки')),
            ],
            options={
                'verbose_name': 'Клавиатура',
                'verbose_name_plural': 'Клавиатуры',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('RUS', 'Русский'), ('ENG', 'English'), ('TUR', 'Turkish'), ('GER', 'German'), ('FR', 'Frankish')], default='RUS', max_length=5, verbose_name='Язык перевода')),
                ('caption', models.CharField(max_length=100, verbose_name='Текст команды (start, напимер)')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Текст реакции на команду (не обязательно)')),
                ('delay', models.IntegerField(default=0, verbose_name='Задержка реакции, сек')),
                ('tag_action', models.CharField(default='NONE', max_length=5, verbose_name='Тэги пользователя')),
                ('bot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bots.telegrambot', verbose_name='Бот')),
                ('jump_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reactions.answer', verbose_name='Автопереход')),
                ('keyboard', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reactions.keyboard', verbose_name='Клавиатура')),
                ('tags', models.ManyToManyField(to='classificators.usertag', verbose_name='')),
            ],
            options={
                'verbose_name': 'Ответ бота',
                'verbose_name_plural': 'Ответы',
            },
        ),
        migrations.AddField(
            model_name='command',
            name='jump_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reactions.answer', verbose_name='Автопереход'),
        ),
        migrations.AddField(
            model_name='command',
            name='keyboard',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reactions.keyboard', verbose_name='Клавиатура'),
        ),
    ]

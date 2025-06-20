# Generated by Django 5.1.7 on 2025-06-06 08:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0002_customeruser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название курса')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание курса')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст вопроса')),
            ],
            options={
                'verbose_name': 'Вопрос теста',
                'verbose_name_plural': 'Вопросы тестов',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название материала')),
                ('file', models.FileField(upload_to='course_materials/', verbose_name='Файл')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание материала')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='education.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Материал курса',
                'verbose_name_plural': 'Материалы курсов',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='Текст варианта ответа')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Это правильный ответ?')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='education.question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Вариант ответа',
                'verbose_name_plural': 'Варианты ответов',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название теста')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание теста')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='education.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Тест',
                'verbose_name_plural': 'Тесты',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='education.test', verbose_name='Тест'),
        ),
    ]

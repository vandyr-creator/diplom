from django.contrib.auth.models import AbstractUser
from django.db import models


class News(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.TextField()
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Provision(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.TextField()
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Board(models.Model):
    name = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    description = models.TextField()
    specifications = models.TextField()

    def __str__(self):
        return self.name


class Contest(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    prize = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class CustomerUser(AbstractUser):
    class Roles(models.TextChoices):
        EMPLOYEE = 'employee', 'Сотрудник'
        CURATOR = 'curator', 'Куратор'
        ADMIN = 'admin', 'Администратор'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.EMPLOYEE,
        verbose_name="Роль"
    )

    def is_employee(self):
        return self.role == self.Roles.EMPLOYEE

    def is_curator(self):
        return self.role == self.Roles.CURATOR

    def is_admin(self):
        return self.role == self.Roles.ADMIN


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Material(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название материала")
    file = models.FileField(upload_to='course_materials/', verbose_name="Файл")
    description = models.TextField(blank=True, null=True, verbose_name="Описание материала")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    class Meta:
        verbose_name = "Материал курса"
        verbose_name_plural = "Материалы курсов"

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class Test(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='tests',
        verbose_name="Курс"
    )
    title = models.CharField(max_length=255, verbose_name="Название теста")
    description = models.TextField(blank=True, null=True, verbose_name="Описание теста")

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return f"{self.title} ({self.course.title})"


class Question(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Тест"
    )
    text = models.TextField(verbose_name="Текст вопроса")

    class Meta:
        verbose_name = "Вопрос теста"
        verbose_name_plural = "Вопросы тестов"

    def __str__(self):
        return self.text[:50] + "..." if len(self.text) > 50 else self.text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name="Вопрос"
    )
    text = models.CharField(max_length=255, verbose_name="Текст варианта ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Это правильный ответ?")

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"

    def __str__(self):
        return self.text

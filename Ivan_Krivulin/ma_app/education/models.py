from django.contrib.auth.models import User, AbstractUser
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


from django.contrib.auth.models import AbstractUser
from django.db import models

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


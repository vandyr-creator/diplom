
from django.contrib.auth.admin import UserAdmin
from .models import CustomerUser
from django.contrib import admin
from .models import News, Provision, Board, Contest  # добавь Contest сюда

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'prize')  # какие поля показывать
    search_fields = ('title', 'description', 'prize')  # по каким полям искать
    list_filter = ('start_date', 'end_date')  # по каким фильтровать
    ordering = ('-start_date',)  # сортировка по умолчанию


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'content', 'pub_date')

@admin.register(Provision)
class ProvisionAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'content', 'pub_date')

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'description', 'specifications')

@admin.register(CustomerUser)
class CustomerUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')

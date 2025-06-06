from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Course, Material, Test, Question, Choice
from .models import CustomerUser
from .models import News, Provision, Board, Contest


class MaterialInline(admin.StackedInline):
    model = Material
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    min_num = 2
    max_num = 10


class QuestionInline(admin.StackedInline):
    model = Question
    inlines = [ChoiceInline]
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    inlines = [MaterialInline]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'file', 'uploaded_at')
    search_fields = ('title', 'description', 'course__title')
    list_filter = ('course', 'uploaded_at')


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'description')
    search_fields = ('title', 'description', 'course__title')
    list_filter = ('course',)
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'test')
    search_fields = ('text', 'test__title')
    list_filter = ('test',)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('question', 'is_correct')
    search_fields = ('text',)


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'prize')
    search_fields = ('title', 'description', 'prize')
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)


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

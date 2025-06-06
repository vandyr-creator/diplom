from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import Form
from django.forms import ModelChoiceField, RadioSelect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic import TemplateView
from education.forms import CustomUserCreationForm
from education.models import News, Board, Provision, Contest, CustomerUser
from django.db.models import Q
from .models import Course, Material, Test, Question


class CourseListView(ListView):
    model = Course
    template_name = 'education/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).distinct()
        return queryset.order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_app'] = 'courses'
        return context

class ContestListView(ListView):
    model = Contest
    template_name = 'education/contest_list.html'
    context_object_name = 'contests'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            ).distinct()
        return queryset.order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_app'] = 'contests'
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'education/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['materials'] = self.object.materials.all()
        context['tests'] = self.object.tests.all()
        return context


class MaterialDetailView(DetailView):
    model = Material
    template_name = 'education/material_detail.html'
    context_object_name = 'material'


class TestAttemptView(FormView):
    template_name = 'education/test_attempt.html'
    success_url = reverse_lazy('education:test_result')

    def get_form(self, form_class=None):
        test = get_object_or_404(Test, pk=self.kwargs['pk'])
        questions = test.questions.prefetch_related('choices').all()

        class TestForm(Form):
            def __init__(self, *args, **kwargs):
                self.test = kwargs.pop('test_instance')
                super().__init__(*args, **kwargs)

                for question in questions:
                    self.fields[f'question_{question.pk}'] = ModelChoiceField(
                        queryset=question.choices.all(),
                        widget=RadioSelect,
                        empty_label=None,
                        label=question.text,
                        required=True
                    )

        return TestForm(test_instance=test, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = get_object_or_404(Test, pk=self.kwargs['pk'])
        return context


    def form_valid(self, form):
        test = get_object_or_404(Test, pk=self.kwargs['pk'])
        score = 0
        total_questions = test.questions.count()
        user_answers = {}

        for field_name, selected_choice in form.cleaned_data.items():
            if field_name.startswith('question_'):
                question_pk = int(field_name.split('_')[1])
                question = get_object_or_404(Question, pk=question_pk)
                user_answers[question.pk] = selected_choice.pk
                if selected_choice.is_correct:
                    score += 1

        self.request.session['test_score'] = score
        self.request.session['total_questions'] = total_questions
        self.request.session['test_id'] = test.pk

        return super().form_valid(form)


class TestResultView(DetailView):
    model = Test
    template_name = 'education/test_result.html'
    context_object_name = 'test'

    def get_object(self, queryset=None):
        test_id = self.request.session.get('test_id')
        if not test_id:
            return redirect(reverse_lazy('education:course_list'))
        return get_object_or_404(Test, pk=test_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        score = self.request.session.pop('test_score', 0)
        total_questions = self.request.session.pop('total_questions', 1)

        context['score'] = score
        context['total_questions'] = total_questions
        context['half_total_questions'] = total_questions / 2
        return context

class RenderMainPage(View):
    def get(self, request):
        current_user = None
        role = None

        if request.user.is_authenticated:
            current_user = CustomerUser.objects.get(pk=request.user.pk)
            role = current_user.role

        news = News.objects.all().order_by('-pub_date')
        return render(request, "education/main.html", context={
            "user": current_user,
            "role": role,
            "news": news
        })


class Schemes(View):
    def get(self, request):
        return render(request, "education/schemes.html")


class ProvisionEducation(View):
    def get(self, request):
        return render(request, "education/provision_education.html")


class SchemeChecking(View):
    def get(self, request):
        return render(request, "education/scheme_checking.html")


class NewsView(View):
    def get(self, request):
        news = News.objects.all().order_by('-pub_date')
        return render(request, "education/news.html", context={"news": news})


class NewDetailView(View):
    def get(self, request, news_id):
        new = get_object_or_404(News, id=news_id)
        return render(request, 'education/new_detail.html', {'new': new})


class TutorialsMain(View):
    def get(self, request):
        provisions = Provision.objects.all().order_by('-pub_date')
        boards = Board.objects.all()

        current_user = request.user if request.user.is_authenticated else None
        role = current_user.role if current_user else None

        return render(request, 'education/tutorials.html', {
            'provisions': provisions,
            'boards': boards,
            'role': role
        })


class ProvisionDetailView(View):
    def get(self, request, pk):
        provision = get_object_or_404(Provision, id=pk)
        return render(request, 'education/provision_detail.html', {'provision': provision})


class BoardDetailView(View):
    def get(self, request, pk):
        board = get_object_or_404(Board, id=pk)
        return render(request, 'education/board_detail.html', {'board': board})


class ContestListView(View):
    def get(self, request):
        contests = Contest.objects.all().order_by('-start_date')
        return render(request, 'education/contest_list.html', {'contests': contests})


class ContestDetailView(View):
    def get(self, request, pk):
        contest = get_object_or_404(Contest, id=pk)
        return render(request, 'education/contest_detail.html', {'contest': contest})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = CustomerUser.Roles.EMPLOYEE  # или другая роль по логике
            user.save()
            login(request, user)
            return redirect('education:main')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = '/login.html'
    next_page = 'education:profile'


def logout_view(request):
    logout(request)
    return redirect('education:login')


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'education/profile.html'

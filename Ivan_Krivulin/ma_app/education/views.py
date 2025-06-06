from http.client import HTTPResponse

from django.contrib.auth import authenticate, login, user_logged_in, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from education.models import News, Board, Provision, Contest, CustomerUser

from education.forms import CustomUserCreationForm


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

from . import views
from django.urls import path, include
app_name = "education"

urlpatterns = [
    path('', views.RenderMainPage.as_view(), name='main'),
    path('schemes/', views.Schemes.as_view(), name='schemes'),
    path('provision/', views.ProvisionEducation.as_view(), name='provision'),
    path('scheme-checking/', views.SchemeChecking.as_view(), name='scheme_check'),
    path('news/', views.NewsView.as_view(), name="news"),
    path('news/<int:news_id>/', views.NewDetailView.as_view(), name="news_detail"),
    path('tutorials/', views.CourseListView.as_view(), name="tutorials"),

    path('tutorials/provision/<int:pk>/', views.ProvisionDetailView.as_view(), name="provision_detail"),
    path('tutorials/boards/<int:pk>/', views.BoardDetailView.as_view(), name="board_detail"),

    path('contests/', views.ContestListView.as_view(), name='contest_list'),
    path('contest/<int:pk>', views.ContestDetailView.as_view(), name='contest_detail'),

    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),

    path('profile', views.UserProfileView.as_view(), name='profile'),

    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('materials/<int:pk>/', views.MaterialDetailView.as_view(), name='material_detail'),
    path('tests/<int:pk>/attempt/', views.TestAttemptView.as_view(), name='test_attempt'),
    path('tests/result/', views.TestResultView.as_view(), name='test_result'),
]
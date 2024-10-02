from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_signup_view, dashboard, AnalyzeURLView, reset_password
from app01 import views
urlpatterns = [
    path('', login_signup_view, name='login_signup'),  # Login/Signup page
    path('dashboard/', dashboard, name='dashboard'),   # Dashboard URL
    path('api/analyze-url/', AnalyzeURLView.as_view(), name='analyze_url'),  # URL analysis endpoint
    path('logout/', auth_views.LogoutView.as_view(next_page='login_signup'), name='logout'),  # Logout URL
    path('add-history/', views.add_history, name='add_history'),# to add history
    path('clear-history/', views.clear_history, name='clear_history'),#to clear history
    path('reset-password/', reset_password, name='reset_password'),# to reset password
]

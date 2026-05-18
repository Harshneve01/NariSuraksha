from django.urls import path
from . import views

urlpatterns = [

    # ---------------- HOME ----------------
    path('', views.home, name='home'),

    # ---------------- AUTH ----------------
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    # ---------------- DASHBOARD ----------------
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-contact/', views.add_contact, name='add_contact'),

    # ---------------- SOS ----------------
    path('sos/', views.send_sos, name='sos'),

    # ---------------- ALERT ACTION ----------------
    path('alert/<int:alert_id>/<str:action>/', views.update_alert_status, name='update_alert'),

    # ---------------- POLICY PAGE (NEW) ----------------
    path('policy/', views.policy, name='policy'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('contact/sent', views.contact_sent, name='contact_sent'),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('user/<username>/', views.profile, name='profile'),
    path('family/create/', views.FamilyCreate.as_view(), name='family_create'),
    path('family/join/', views.join_family, name='join_family'),
]
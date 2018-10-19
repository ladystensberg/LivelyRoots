from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('contact/sent', views.contact_sent, name='contact_sent'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('user/<username>/', views.profile, name='profile'),
    path('user/<username>/edit_profile/', views.edit_profile, name='edit_profile'),
    path('user/<username>/delete_confirm', views.delete_user_confirm, name='delete_user_confirm'),
    path('user/<username>/delete', views.delete_user, name='delete_user'),
    path('user/<username>/posts', views.user_posts, name='user_posts'),
    path('family/create/', views.FamilyCreate.as_view(), name='family_create'),
    path('family/join/', views.join_family, name='join_family'),
    path('posts/', views.post_feed, name='post_feed'),
    path('posts/create_post/', views.create_post, name='create_post'),
    path('posts/<int:post_id>', views.view_post, name='view_post'),
    path('posts/<int:post_id>/delete_post', views.delete_post, name='delete_post'),
    path('posts/<int:pk>/update_post/', views.UpdatePost.as_view(), name='update_post'),
    path('posts/<int:post_id>/delete_post_confirm', views.delete_post_confirm, name='delete_post_confirm'),
    path('posts/<int:post_id>/add_comment', views.add_comment, name='add_comment'),
]
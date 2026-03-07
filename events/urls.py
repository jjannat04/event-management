from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('events', views.event_list, name='event_list'),           
    path('create/', views.event_create, name='event_create'), 
    path('<int:pk>/update/', views.event_update, name='event_update'), 
    path('<int:pk>/delete/', views.event_delete, name='event_delete'), 

    path('participants/', views.participant_list, name='participant_list'), 
    path('participants/create/', views.participant_create, name='participant_create'),
    path('participants/<int:pk>/delete/', views.participant_delete, name='participant_delete'),
    path('participant-dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('organizer-dashboard/', views.organizer_dashboard, name='organizer_dashboard'),

    path('categories/', views.category_list, name='category_list'), 
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('events/<int:pk>/rsvp/', views.rsvp_event, name='event_rsvp'),
    path('activate/<int:user_id>/<path:token>/', views.activate_account, name='activate_account'),

    ]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
urlpatterns = [
    
    path('', views.home, name='home'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('events/', views.EventListView.as_view(), name='event_list'),         
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/create/', views.EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),

    path('participants/', views.participant_list, name='participant_list'), 
    path('participants/create/', views.participant_create, name='participant_create'),
    path('participants/<int:pk>/delete/', views.participant_delete, name='participant_delete'),
    path('participant-dashboard/', views.participant_dashboard, name='participant_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('organizer-dashboard/', views.organizer_dashboard, name='organizer_dashboard'),

    path('categories/', views.category_list, name='category_list'), 
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('events/<int:pk>/rsvp/', views.rsvp_event, name='event_rsvp'),
    path('activate/<int:user_id>/<path:token>/', views.activate_account, name='activate_account'),

    path('profile/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

   

    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='events/password_change.html',
        success_url='/events/profile/'
    ), name='password_change'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
    template_name='events/password_reset.html',
    success_url=reverse_lazy('password_reset_done') # Add this line
), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='events/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='events/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='events/password_reset_complete.html'
    ), name='password_reset_complete'),


]
from django.urls import path
from calen import views

urlpatterns = [
    path('auth/', views.Authenticate.as_view(), name=''),
    path('cal/', views.Calendars.as_view(), name='calendar'),
    path('callist/', views.CalendarList.as_view(), name='calendar-list'),
    path('evlist/', views.EvList.as_view(), name='event-list'),
    path('crev/', views.CreateEv.as_view(), name='create-event'),
    path('delev/<str:pk>', views.DelEvent.as_view(), name='delete-event'),
    path('upev/', views.UpdEvent.as_view(), name='update-event'),
    path('home/', views.Home, name='home-page'),
]
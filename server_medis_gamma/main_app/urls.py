from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('logout/', LogoutView.as_view(next_page='staff-login'), name='logout'),
    path('pasien/<int:pk>/', views.patient_view, name='patient'),
    path('pasien/edit/<int:pk>/', views.edit_view, name='edit'),
    path('pasien/delete/<int:patient_id>/', views.delete_patient, name='delete'),
    path('pasien/new/', views.neu_patient, name='new'),
    path('api/reading/<int:reading_id>/', views.get_reading_detail, name='get-reading-detail'),
    path('assign_node/', views.assign_node_view, name='assign_node'),
]

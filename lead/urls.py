from django.urls import path

from . import views

app_name = 'leads'

urlpatterns = [
    path('add-lead/', views.add_lead, name='add'),
    path('<int:pk>/', views.leads_detail, name='detail'),
    path('<int:pk>/delete/', views.leads_delete, name='delete'),
    path('<int:pk>/edit/', views.leads_edit, name='edit'),
    path('<int:pk>/convert/', views.convert_to_client, name='convert'),
    path('', views.leads_list, name='list'),
    path('export/', views.export_to_excel, name='export_to_excel'),
]

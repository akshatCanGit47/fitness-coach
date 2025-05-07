from django.urls import path
from . import views

app_name = 'fitness'  # NAMESPACE DECLARATION

urlpatterns = [
    # Dashboard URL
    path('', views.dashboard, name='dashboard'),
    
    # Result URL
    path('result/<int:prediction_id>/', views.result_view, name='result'),
]
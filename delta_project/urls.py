from django.contrib import admin
from django.urls import path
from chatbot import views  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('ask/', views.ask_ai, name='ask'),  # <--- Make sure this line exists!
]
from django.urls import path
from .views import index, SignUpView

urlpatterns = [
    path('', index, name='home'),
    path("signup/", SignUpView.as_view(), name="signup"),
]
from django.urls import path
from . import views
app_name = "main"
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('ticket', views.TicketPage.as_view(), name='ticket'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path("logout", views.logout, name='logout'),
    path("login", views.Login.as_view(), name='login'),
    path("mail/verify", views.VerifyMail.as_view(), name='verify_mail'),
]

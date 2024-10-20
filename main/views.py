from django.shortcuts import render, redirect
from django.views import View
# Create your views here.


class Index(View):
    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        return render(request, 'main/index.html')


class TicketPage(View):
    def get(self, request):
        return redirect('signup_login')

    def post(self, request):
        # if cookie is present, then show current ticket, else redirect to signup/login page
        if 'user_cookie' in request.COOKIES:
            # Show current ticket

            return render(request, 'ticket.html')
        else:
            # Redirect to signup/login page
            return redirect('signup_login')


class SignUp(View):
    def get(self, request):
        return render(request, 'main/signup.html')


class Login(View):
    def get(self, request):
        return render(request, 'main/login.html')

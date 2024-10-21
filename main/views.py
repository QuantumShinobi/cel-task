from .mail import *
import uuid
from .models import User, Query
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
import bcrypt
from .mail import send__mail, send_verify_mail, check_if_key_is_valid


class Index(View):
    def get(self, request):
        return render(request, 'main/index.html')

    def post(self, request):
        return render(request, 'main/index.html')


class TicketPage(View):
    def get(self, request):
        user = User.get_user(request)
        return render(request, "main/ticket.html", context={"user": user})

    def post(self, request):
        pass
        email = request.POST['email']
        print(email)
        print
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            return user.authenticate(password, request)
        return render(request, "main/error.html", context={'error': "There is no account associated with this email"})


class SignUp(View):
    def get(self, request):
        try:
            u_id = request.COOKIES['user-identity']
            print(u_id)
        except KeyError:
            return render(request, 'main/signup.html')
        else:
            try:
                user = User.objects.get(unique_id=u_id)
            except User.DoesNotExist:
                response = render(request, 'main/index.html')
                response.delete_cookie('user-identity')
                return response
            return redirect('main:ticket')

    def post(self, request):
        try:
            u_id = request.COOKIES['user-identity']
            print(u_id)
        except KeyError:
            name = request.POST['name']
            password = request.POST['password']
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                return render(request, 'main/signup.html', context={"error": "Email already exists"})
            else:
                if len(password) < 8:
                    return render(request, 'main/signup.html', context={"error": "Password must be at least 8 characters long"})
            hash_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            name = name.capitalize()
            new_user = User.objects.create(
                name=name, email=email, password=hash_pw)
            response = redirect('main:ticket')
            response.set_cookie("user-identity", str(new_user.unique_id))
            # verifymail(email)
            # send_verify_mail(email, request, new_user)
            return response
        else:
            try:
                user = User.objects.get(unique_id=u_id)
            except User.DoesNotExist:
                response = render(request, 'main/index.html')
                response.delete_cookie('user-identity')
                return response
            return render(request, 'main/ticket.html', context={"user": user})


class Login(View):
    def get(self, request):
        return render(request, 'main/login.html')

    def post(self, request):
        try:
            u_id = request.COOKIES['user-identity']
        except KeyError:
            email = request.POST['email']
            print(email)
            password = request.POST['password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'main/login.html', context={"error": "Email not found"})
            else:
                if bcrypt.checkpw(password.encode('utf-8'), user.password):
                    response = redirect('main:ticket')
                    response.set_cookie("user-identity", str(user.unique_id))
                    return response
                else:
                    return render(request, 'main/login.html', context={"error": "Password incorrect"})
        else:
            try:
                user = User.objects.get(unique_id=u_id)
            except User.DoesNotExist:
                response = render(request, 'main/index.html')
                response.delete_cookie('user-identity')
                return response
            return render(request, 'main/ticket.html', context={"user": user})


class MailView(View):
    @staticmethod
    def get(request):
        check_if_key_is_valid(Query)
        return render(request, 'mail/index.html')

    @staticmethod
    def post(request):
        check_if_key_is_valid(Query)
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect(f"http://{request.META['HTTP_HOST']}/mail?invalid=true")
        else:
            email = user.email
            if email is not None and email.isspace() is False:
                if user.email_is_verified is True:
                    id = Query.objects.create(user=user, mail=user.email)
                    send__mail(id, user.email, request, user)
                    return render(request, "mail/sent.html")
                return redirect(f"http://{request.META['HTTP_HOST']}/mail?not_verified=true")
            else:
                return redirect(f"http://{request.META['HTTP_HOST']}/mail?mail_invalid=true")


class ResetPasswordView(View):
    @staticmethod
    def get(request, id1, id2):
        try:
            id1 = uuid.UUID(id1)
            id2 = uuid.UUID(id2)
            query = Query.objects.get(unique_id=id1)
        except (Query.DoesNotExist, AttributeError, TypeError):
            raise Http404
        else:
            if query.unique_id_2 == id2:
                user = query.user
                return render(request, "mail/reset_pwd.html", {"user": user})
            raise Http404

    @staticmethod
    def post(request):
        new_pwd = request.POST['new_password']
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Http404
        else:
            hash_pwd = bcrypt.hashpw(
                bytes(new_pwd, 'utf-8'), bcrypt.gensalt())
            user.password = hash_pwd
            user.save()
            try:
                query = Query.objects.get(user=user)
            except Query.DoesNotExist:
                return render(request, "error.html", context={'error': "email not correct"})
            query.delete()
            return render(request, "mail/done.html")


class VerifyMail(View):
    @staticmethod
    def get(request, id):
        try:
            user = User.objects.get(unique_id=uuid.UUID(id))
        except (User.DoesNotExist):
            print("UUID NOT FOUND")
            return HttpResponse("NOT FOUND")
        else:
            if user.email_is_verified is False and user.email.isspace() is False and user.email != "":
                user.email_is_verified = True
                user.save()
                return render(request, "mail/verified.html")
            raise Http404


def logout(request):
    response = redirect('main:index')
    response.delete_cookie('user-identity')
    return response

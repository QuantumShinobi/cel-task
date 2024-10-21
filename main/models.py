from django.db import models
import uuid
import bcrypt
from django.shortcuts import render, redirect
import json
from datetime import datetime, timezone


class User(models.Model):
    password = models.BinaryField(editable=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    email_is_verified = models.BooleanField(default=False)
    unique_id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    no_of_tickets = models.IntegerField(default=0)
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def authenticate(self, pwd, request, bot=False):
        if bot is False:
            if type(self.password) == memoryview:
                if bcrypt.checkpw(bytes(pwd, 'utf-8'), self.password.tobytes()):

                    response = render(request, 'main/logout.html',
                                      context={"title": "Login",
                                               "text": "Logging you in"})
                    response.set_cookie(
                        "user-identity", str(self.unique_id), max_age=31556952)
                    return response
                return render(request, "main/login.html", context={"error": "Password is incorrect"})
            else:
                if bcrypt.checkpw(bytes(pwd, 'utf-8'), self.password):
                    response = render(request, 'main/logout.html',
                                      context={"title": "Login",
                                               "text": "Logging you in"})
                    response.set_cookie("user-identity", str(self.unique_id))
                    return response

        elif bot == True:
            return render(request, "main/login.html", context={"error": "Password is incorrect"})
        elif bot is True:
            return bcrypt.checkpw(bytes(pwd, 'utf-8'), self.password)

    @staticmethod
    def get_user(request):
        try:
            request.COOKIES['user-identity']
        except (KeyError, AttributeError):
            return redirect("main:login")
        else:
            id = request.COOKIES['user-identity']
            try:
                user = User.objects.get(unique_id=id)
            except User.DoesNotExist:
                res = render(request, "main/logout.html",
                             context={"text": "Loading"})
                res.delete_cookie("user-identity")
                return res
            else:
                return user

    @staticmethod
    def logout(request):
        try:
            request.COOKIES['user-identity']
        except KeyError:
            return redirect("main:index")
        else:
            response = render(request, 'main/logout.html',
                              context={"title": "Logout", "text": "Logging you out"})
            response.delete_cookie("user-identity")
            return response


class Query(models.Model):
    unique_id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    unique_id_2 = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    # time_created = models.DateTimeField(default=datetime.now(tz=timezone.utc))
    time_created = models.DateTimeField(auto_now_add=True)

    mail = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID - {self.unique_id}\n TIME - {self.time_created}"

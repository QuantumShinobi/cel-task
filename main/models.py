from django.db import models
import uuid
import bcrypt
from django.shortcuts import render, redirect
import json


class User(models.Model):
    username = models.CharField(max_length=25, unique=True)
    password = models.BinaryField(editable=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    email_is_verified = models.BooleanField(default=False)
    unique_id = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False)
    no_of_tickets = models.IntegerField(default=0)
    ticket_id = models.UUIDField(default=uuid.uuid4, editable=False)
    warned_email = models.BooleanField(default=False, editable=True)

    def __str__(self):
        return self.username

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

    def transaction(self, new_transaction_created):
        jsonDec = json.decoder.JSONDecoder()
        try:
            current_list = jsonDec.decode(self.transaction_list)
        except (TypeError, json.decoder.JSONDecodeError):
            current_list = []

        current_list.append(str(new_transaction_created.transaction_id))
        self.transaction_list = json.dumps(current_list)
        self.save()
        new_transaction_created.save()
        return True

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

    def get_friends(self):
        jsonDec = json.decoder.JSONDecoder()
        friends_list = []
        try:
            for id in jsonDec.decode(self.friends_list):
                frnd = User.objects.get(unique_id=id)
                friends_list.append(frnd)

            return friends_list
        except (User.DoesNotExist, TypeError, json.decoder.JSONDecodeError):
            return None

    def add_friend(self, username):
        jsonDec = json.decoder.JSONDecoder()
        friends_list = []
        try:
            for id in jsonDec.decode(self.friends_list):
                friends_list.append(id)
        except (User.DoesNotExist, TypeError):
            friends_list = []
        try:
            friend = User.objects.get(username=username)
        except User.DoesNotExist:
            return False
        else:
            if friend.unique_id == self.unique_id:
                return False
            friends_list.append(str(friend.unique_id))
            self.friends_list = json.dumps(list(set(friends_list)))
            self.save()
            return True

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

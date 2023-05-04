"""
This module contains views for user authentication and management.
"""

import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from final_project.utils.http_responses import data_status, ok_status, failed_status


def get_user(request, username):
    """
    Returns user information (username and adops permission) for a given username.

    Args:
        request: HttpRequest object.
        username: str, the username to retrieve information for.

    Returns:
        HttpResponse object with a JSON response containing the username and adops permission.
    """
    user = User.objects.get(username=username)
    return data_status({
        'username': user.username,
        'adops': user.has_perm('admin.adops_permission')
    })


def create_user(request):
    """
    Creates a new user with the provided information.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with a success status.
    """
    data = json.loads(request.body.decode())
    if request.method == 'POST':
        username = data['username']
        email = data['email']
        password = data['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = False
        adops_permission = Permission.objects.get(codename='adops_permission')
        if data['adops']:
            user.user_permissions.add(adops_permission)

        user.save()
        messages.success(request, 'User created successfully')
    return ok_status()


def login_view(request):
    """
    Authenticates a user and returns an access token and refresh token if successful.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with a JSON response containing the access token and refresh token, or an error status.
    """
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        user = None
        try:
            username = data['username']
            password = data['password']
            user = authenticate(request, username=username, password=password)
        except Exception as e:
            print("ERROR: Login error", e)
        if user:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            return data_status({'access': str(access), 'refresh': str(refresh)})
        else:
            print('Invalid login credentials')
            return failed_status('Invalid login credentials or the user is not approved by our administration.')
    return ok_status()


def logout_view(request):
    """
    Logs out a user and revokes their refresh token.

    Args:
        request: HttpRequest object.

    Returns:
        HttpResponse object with a success status or an error status if the token is invalid or there is a token error.
    """
    try:
        if request.headers['Authorization']:
            data = json.loads(request.body.decode())
            refresh_token = data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
    except InvalidToken:
        return failed_status("Invalid token")
    except TokenError:
        return failed_status("Token error")
    return ok_status()

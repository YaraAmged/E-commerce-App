from django.shortcuts import redirect
from django.contrib.auth import logout


def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before

        # the view (and later middleware) are called.
        if (not request.user.is_authenticated and request.path_info not in ["/user/login", "/user/registration", "/favicon", "/"]) and "admin" not in request.path_info:
            print("will redirect case 1")
            return redirect("user:login")
        elif request.user.is_authenticated and "admin" not in request.path_info and request.user.is_staff:
            print("will redirect case 2")
            logout(request)
            return redirect("user:login")

        response = get_response(request)
        return response

    return middleware

from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login


def generate_jwt_token(user):
    """Genera un token JWT para un usuario"""
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            # Validar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            # Crear usuario con contraseña cifrada
            user = User(username=username)
            user.set_password(password)  # Usa bcrypt automáticamente
            user.save()

            # Generar un token JWT para el nuevo usuario
            tokens = generate_jwt_token(user)

            return JsonResponse(
                {
                    "message": "User registered successfully",
                    "tokens": tokens,
                }
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            # Autenticar al usuario
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # Inicia sesión

                # Generar un token JWT para el usuario autenticado
                tokens = generate_jwt_token(user)

                return JsonResponse(
                    {
                        "message": "Login successful",
                        "tokens": tokens,
                    }
                )
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

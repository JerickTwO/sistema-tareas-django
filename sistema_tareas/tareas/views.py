from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login

User = get_user_model()


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
            email = data.get("email")
            username = data.get("username")
            password = data.get("password")
            rol = data.get("role")  # Validar el rol

            # Validar campos obligatorios
            if not username or not password or not rol or not email:
                return JsonResponse(
                    {"error": "username, password, email, and role are required"},
                    status=400,
                )

            # Validar si el rol es válido
            if rol not in ["admin", "estudiante"]:
                return JsonResponse({"error": "Invalid role"}, status=400)

            # Validar si el usuario ya existe
            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            # Validar si el usuario ya existe
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            # Crear usuario
            user = User(username=username, rol=rol, email=email)
            user.set_password(password)  # Cifrar contraseña
            user.save()

            # Generar un token JWT
            tokens = generate_jwt_token(user)

            return JsonResponse(
                {
                    "message": "User registered successfully",
                    "tokens": tokens,
                },
                status=201,
            )
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")

            # Autenticar al usuario
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)  # Inicia sesión

                # Generar un token JWT para el usuario autenticado
                tokens = generate_jwt_token(user)

                return JsonResponse(
                    {
                        "message": f"Login successful, welcome {user.username}",
                        "tokens": tokens,
                    }
                )
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

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
        "jwt": str(refresh.access_token),
    }


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            id = data.get("id")
            email = data.get("email")
            name = data.get("name")
            password = data.get("password")
            confirm_password = data.get("confirmPassword")
            role = data.get("role", True)

            # Validar campos obligatorios
            if not name or not password or not email:
                return JsonResponse(
                    {"error": "username, password, and email are required"},
                    status=400,
                )

            # Validar si el usuario ya existe
            if User.objects.filter(username=name).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            # Validar si el usuario ya existe
            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            if password != confirm_password:
                return JsonResponse(
                    {"error": "Passwords do not match"},
                    status=400,
                )

            # Crear usuario
            user = User(username=name, email=email, rol=role)
            user.set_password(password)  # Cifrar contraseña
            user.save()

            return JsonResponse(
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.username,
                    "password": None,
                    "role": "ESTUDIANTE" if user.rol == 1 else "ADMINISTRADOR",
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
            role = data.get("userRole")

            # Autenticar al usuario
            user = authenticate(request, username=email, password=password, role=role)
            if user is not None:
                login(request, user)  # Inicia sesión

                # Generar un token JWT para el usuario autenticado
                tokens = generate_jwt_token(user)

                return JsonResponse(
                    {
                        "jwt": tokens["jwt"],  # Incluye solo el token de acceso
                        "userId": user.id,  # ID del usuario autenticado
                        "userRole": "ESTUDIANTE" if user.rol == 1 else "ADMINISTRADOR",
                    },
                    status=200,
                )
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

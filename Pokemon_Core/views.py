from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import FavoritePokemon
from .serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction, models

class FavoritePokemonToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        pokemon_name = request.data.get("pokemon_name")
        pokemon_id = request.data.get("pokemon_id")

        if not pokemon_name and not pokemon_id:
            return Response({"error": "pokemon_name and pokemon_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        favorite, created = FavoritePokemon.objects.get_or_create(user=request.user, pokemon_name=pokemon_name, pokemon_id=pokemon_id)

        if not created:
            favorite.is_favorite = not favorite.is_favorite
            favorite.save()
            message = "added to" if favorite.is_favorite else "removed from"
        else:
            message = "added to"

        return Response({"message": f"{pokemon_name}, {pokemon_id} {message} favorites."}, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        favorite_pokemons = FavoritePokemon.objects.filter(user=request.user, is_favorite=True)

        favorite_data = [
            {"name": favorite.pokemon_name, "id": favorite.pokemon_id}
            for favorite in favorite_pokemons
        ]

        if not favorite_data:
            return Response({"message": "No favorite Pokémon found."}, status=status.HTTP_200_OK)

        return Response({"favorite_pokemons": favorite_data}, status=status.HTTP_200_OK)
    
class FavoritePokemonOrder(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        order = request.data.get("order")
        pokemon_id = request.data.get("pokemon_id")

        if not order and not pokemon_id:
            return Response({"error": "order and pokemon_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favorite_pokemon = FavoritePokemon.objects.get(user=request.user, pokemon_id=pokemon_id, is_favorite=True)
        except FavoritePokemon.DoesNotExist:
            return Response({"error": "Favorite Pokémon not found."}, status=status.HTTP_404_NOT_FOUND)
        
        old_order = favorite_pokemon.order

        if old_order == order:
            return Response({"message": "No changes needed."}, status=status.HTTP_200_OK)
        
        with transaction.atomic():
            if old_order > order:
                FavoritePokemon.objects.filter(
                    user=request.user,
                    order__gte=order,
                    order__lt=old_order
                ).update(order=models.F('order') + 1)
            else:
                FavoritePokemon.objects.filter(
                    user=request.user,
                    order__gt=old_order,
                    order__lte=order
                ).update(order=models.F('order') - 1)

        favorite_pokemon.order = order
        favorite_pokemon.save()

        return Response({"message": f"{pokemon_id} is in the order: {order}, in favorites page."}, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    """Registra um novo usuário"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()
            return Response(
                {"message": f"User {user.username} registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username e senha são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuário não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user = authenticate(request, username=user.username, password=password)
        if user is None:
            return Response(
                {"error": "Username ou senha inválidos."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            status=status.HTTP_200_OK
        )
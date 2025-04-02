from django.db import models
from django.contrib.auth.models import User


class FavoritePokemon(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_pokemons"
    )
    pokemon_name = models.CharField(max_length=100)
    pokemon_id = models.IntegerField()
    is_favorite = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)  

    class Meta:
        unique_together = ('user', 'pokemon_name', 'pokemon_id')
        ordering = ['order']

    def __str__(self):
        return f"{self.pokemon_name} (Favorito de {self.user.username})"

    def save(self, *args, **kwargs):
        if self.order is None or self.order <= 0:
            max_order = FavoritePokemon.objects.filter(user=self.user).aggregate(models.Max('order'))['order__max']
            self.order = (max_order or 0) + 1  
        super().save(*args, **kwargs)

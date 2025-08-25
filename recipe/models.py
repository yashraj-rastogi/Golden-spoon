from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='recipes/')
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')  # Prevent duplicate saves

    def __str__(self):
        return f"{self.user.username} saved {self.recipe.name}"

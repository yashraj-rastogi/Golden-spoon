from django.urls import path
from .views import recipe_list, add_recipe, browse_recipes, view_recipe, about, contact, profile, signup, save_recipe, unsave_recipe, saved_recipes

urlpatterns = [
    path('', recipe_list, name='recipe_list'),
    path('add/', add_recipe, name='add_recipe'),
    path('browse/', browse_recipes, name='browse_recipes'),
    path('recipe/<int:recipe_id>/', view_recipe, name='view_recipe'),
    path('recipe/<int:recipe_id>/save/', save_recipe, name='save_recipe'),
    path('recipe/<int:recipe_id>/unsave/', unsave_recipe, name='unsave_recipe'),
    path('saved-recipes/', saved_recipes, name='saved_recipes'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('profile/', profile, name='profile'),
    path('signup/', signup, name='signup'),
]

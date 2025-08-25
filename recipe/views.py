from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.files.base import ContentFile
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.http import JsonResponse
from .models import Recipe, SavedRecipe
from .forms import CustomUserCreationForm

def logout_view(request):
    logout(request)
    return redirect('recipe_list')

def home(request):
    recipes = Recipe.objects.all().order_by('-id')
    return render(request, 'front.html', {'recipes': recipes})

def recipe_list(request):
    recipes = Recipe.objects.all().order_by('-id')
    print('DEBUG: Recipes passed to template:')
    for r in recipes:
        print(f'ID: {r.id}, Name: {r.name}, Description: {r.description}')
    return render(request, 'front.html', {'recipes': recipes})

@login_required
def add_recipe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image_file = request.FILES.get('image')
        image_url = request.POST.get('image_url')
        
        # Debug information
        print("POST Data received:")
        print(f"Name: {name}")
        print(f"Description: {description}")
        print(f"Image File: {image_file}")
        print(f"Image URL: {image_url}")

        if name and description:
            # Create a recipe instance in memory without saving it yet
            recipe = Recipe(name=name, description=description)

            # Handle image upload from file
            if image_file:
                recipe.image = image_file
            # Handle image upload from URL
            elif image_url:
                try:
                    response = requests.get(image_url, stream=True)
                    if response.status_code == 200:
                        # Get a valid filename from the URL
                        img_name = image_url.split('/')[-1].split('?')[0]
                        # If no extension in filename, try to get it from Content-Type
                        if '.' not in img_name:
                            content_type = response.headers.get('Content-Type', '')
                            if 'image/jpeg' in content_type:
                                img_name += '.jpg'
                            elif 'image/png' in content_type:
                                img_name += '.png'
                            elif 'image/webp' in content_type:
                                img_name += '.webp'
                            else:
                                img_name += '.jpg'  # default to jpg
                        
                        # Save the downloaded content to the image field
                        recipe.image.save(img_name, ContentFile(response.content), save=False)
                except (requests.exceptions.RequestException, ValueError) as e:
                    print(f"Error downloading image from URL: {e}")
            
            # Assign owner and save the recipe instance to the database once.
            # This will save the recipe and the image (if any) correctly.
            if request.user.is_authenticated:
                recipe.owner = request.user
            recipe.save()
            
            # Debug information after save
            print("\nRecipe saved:")
            print(f"Recipe ID: {recipe.id}")
            print(f"Image name: {recipe.image.name if recipe.image else 'No image'}")
            print(f"Image URL: {recipe.image.url if recipe.image else 'No image'}")
            print(f"Image path: {recipe.image.path if recipe.image else 'No image'}")
            
            # Redirect to the browse page to see the newly added recipe
            return redirect('browse_recipes')

    return render(request, 'add_recipe.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(f"DEBUG: Signup POST data: {request.POST}")
        if form.is_valid():
            print("DEBUG: Form is valid, creating user...")
            try:
                user = form.save()
                print(f"DEBUG: User created: {user.username} with email: {user.email}")
                login(request, user)
                print("DEBUG: User logged in, redirecting to profile")
                return redirect('profile')
            except Exception as e:
                print(f"DEBUG: Error creating user: {e}")
                form.add_error(None, f"An error occurred while creating your account: {e}")
        else:
            # Print form errors for debugging
            print(f"DEBUG: Form errors: {form.errors}")
            print(f"DEBUG: Form non-field errors: {form.non_field_errors()}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='login')
def profile(request):
    user = request.user
    recipes = user.recipes.all().order_by('-id')
    saved_count = SavedRecipe.objects.filter(user=user).count()
    return render(request, 'profile.html', {
        'profile_user': user, 
        'recipes': recipes,
        'saved_count': saved_count
    })

def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedRecipe.objects.filter(user=request.user, recipe=recipe).exists()
    
    context = {
        'recipe': recipe,
        'is_saved': is_saved
    }
    return render(request, 'view_recipe.html', context)

@login_required
def save_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    saved_recipe, created = SavedRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    
    if created:
        return JsonResponse({'saved': True, 'message': 'Recipe saved!'})
    else:
        return JsonResponse({'saved': False, 'message': 'Recipe already saved'})

@login_required
def unsave_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    try:
        saved_recipe = SavedRecipe.objects.get(user=request.user, recipe=recipe)
        saved_recipe.delete()
        return JsonResponse({'saved': False, 'message': 'Recipe removed from saved'})
    except SavedRecipe.DoesNotExist:
        return JsonResponse({'saved': False, 'message': 'Recipe was not saved'})

@login_required
def saved_recipes(request):
    saved_recipes = SavedRecipe.objects.filter(user=request.user).order_by('-saved_at')
    return render(request, 'saved_recipes.html', {'saved_recipes': saved_recipes})

def browse_recipes(request):
    query = request.GET.get('q', '')
    if query:
        recipes = Recipe.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)).order_by('-id')
    else:
        # Show all recipes, ordered by the most recently created
        recipes = Recipe.objects.all().order_by('-id')
    
    # Add debug information
    for recipe in recipes:
        print(f"Recipe: {recipe.name}")
        print(f"Image URL: {recipe.image.url if recipe.image else 'No image'}")
        print(f"Image path: {recipe.image.path if recipe.image else 'No image'}")
        
    return render(request, 'browse_recipes.html', {'recipes': recipes})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
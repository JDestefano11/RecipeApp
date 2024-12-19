from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.db.models import Q, Count
from .models import Recipe
from ingredients.models import Ingredient
from categories.models import Category
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    success_url = reverse_lazy('home')
    redirect_authenticated_user = True

def home(request):
    return render(request, 'recipes/recipes_home.html')

def recipe_list(request):
    recipes = Recipe.objects.all()
    charts = generate_charts(recipes)
    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'charts': charts
    })

@login_required(login_url='login')
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required(login_url='login')
def add_recipe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        cooking_time = request.POST.get('cooking_time')
        difficulty = request.POST.get('difficulty')
        category_id = request.POST.get('category')
        ingredient_ids = request.POST.getlist('ingredients')
        
        recipe = Recipe.objects.create(
            name=name,
            description=description,
            cooking_time=cooking_time,
            difficulty=difficulty,
            category_id=category_id,
            author=request.user
        )
        
        if ingredient_ids:
            recipe.ingredients.set(ingredient_ids)
        
        if request.FILES.get('image'):
            recipe.image = request.FILES['image']
            recipe.save()
            
        return redirect('recipe-detail', pk=recipe.pk)
        
    categories = Category.objects.all()
    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/add_recipe.html', {
        'categories': categories,
        'ingredients': ingredients,
        'difficulties': ['Easy', 'Medium', 'Hard']
    })

def recipe_search(request):
    results_df = None
    charts = None
    recipes = Recipe.objects.all()
    
    if request.GET:
        query = request.GET.get('query', '')
        cooking_time = request.GET.get('cooking_time', '')
        difficulty = request.GET.get('difficulty', '')
        
        if query:
            recipes = recipes.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        
        if cooking_time:
            recipes = recipes.filter(cooking_time__lte=int(cooking_time))
        
        if difficulty:
            recipes = recipes.filter(difficulty=difficulty)
        
        if recipes.exists():
            results_df = pd.DataFrame(list(recipes.values('id', 'name', 'cooking_time', 'difficulty')))
            results_df['ingredients_count'] = recipes.annotate(
                ingredients_count=Count('ingredients')
            ).values_list('ingredients_count', flat=True)
            
            charts = generate_charts(recipes)

    context = {
        'results_df': results_df,
        'charts': charts,
        'query': request.GET.get('query', ''),
        'cooking_time': request.GET.get('cooking_time', ''),
        'difficulty': request.GET.get('difficulty', '')
    }
    
    return render(request, 'recipes/search.html', context)

@login_required(login_url='login')
def ingredient_list(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredients/ingredient_list.html', {'ingredients': ingredients})

@login_required(login_url='login')
def ingredient_detail(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)
    return render(request, 'ingredients/ingredient_detail.html', {'ingredient': ingredient})

@login_required(login_url='login')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})

@login_required(login_url='login')
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'categories/category_detail.html', {'category': category})

def logout_view(request):
    logout(request)
    return redirect('logout_success')

def logout_success(request):
    return render(request, 'auth/success.html')

def about_me(request):
    return render(request, 'recipes/about.html', {
        'name': 'Your Name',
        'github_url': 'https://github.com/yourusername',
        'linkedin_url': 'https://linkedin.com/in/yourusername',
        'email': 'your.email@example.com'
    })

def generate_charts(recipes):
    # Bar Chart
    difficulties = recipes.values('difficulty').annotate(count=Count('id'))
    plt.figure(figsize=(10, 6))
    plt.bar([d['difficulty'] for d in difficulties], [d['count'] for d in difficulties])
    plt.title('Recipes by Difficulty Level')
    plt.xlabel('Difficulty')
    plt.ylabel('Number of Recipes')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    bar_chart = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    # Pie Chart
    categories = recipes.values('category__name').annotate(count=Count('id'))
    plt.figure(figsize=(10, 10))
    plt.pie([c['count'] for c in categories], labels=[c['category__name'] for c in categories])
    plt.title('Recipe Distribution by Category')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    pie_chart = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    # Line Chart
    cooking_times = recipes.values('cooking_time').order_by('cooking_time')
    plt.figure(figsize=(12, 6))
    plt.plot([c['cooking_time'] for c in cooking_times], range(len(cooking_times)))
    plt.title('Recipe Complexity (Cooking Time Distribution)')
    plt.xlabel('Cooking Time (minutes)')
    plt.ylabel('Cumulative Recipes')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    line_chart = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return {
        'bar_chart': bar_chart,
        'pie_chart': pie_chart,
        'line_chart': line_chart
    }

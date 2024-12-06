from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe-list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe-detail'),
    path('ingredients/', views.ingredient_list, name='ingredient-list'),
    path('ingredient/<int:pk>/', views.ingredient_detail, name='ingredient-detail'),
    path('categories/', views.category_list, name='category-list'),
    path('category/<int:pk>/', views.category_detail, name='category-detail'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
  path('logout/', views.logout_view, name='logout'),
path('logout/success/', views.logout_success, name='logout_success'),
path('search/', views.recipe_search, name='recipe-search'),
 path('recipe/add/', views.add_recipe, name='add-recipe'),
 path('about/', views.about_me, name='about-me'),
]

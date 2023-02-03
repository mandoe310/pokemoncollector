from django.shortcuts import render

pokemons = [
    {'name': 'Charmander', 'type': 'fire', 'description': 'fire breathing amphibian', 'special': 'ember', 'hp': '50'},
    {'name': 'Squirtle', 'type': 'water', 'description': 'water pumping turtle', 'special': 'bubble', 'hp': '40'},
    {'name': 'Bulbasaur', 'type': 'grass', 'description': 'vine whipping frog', 'special': 'leech seed', 'hp': '40'},
    {'name': 'Pikachu', 'type': 'electric', 'description': 'electrifying yellow squirrel', 'special': 'thunder jolt', 'hp': '40'},
]

def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def pokemons_index(request):
    return render(request, 'pokemons/index.html', {
        'pokemons': pokemons
    })
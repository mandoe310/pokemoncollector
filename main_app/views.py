from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Pokemon, Trainer
from .forms import EvolutionForm


def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def pokemons_index(request):
    pokemons = Pokemon.objects.all()
    return render(request, 'pokemons/index.html', {
        'pokemons': pokemons
    })

def pokemons_detail(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    id_list = pokemon.trainers.all().values_list('id')
    trainers_pokemon_doesnt_have = Trainer.objects.exclude(id__in=id_list)
    evolution_form = EvolutionForm()
    return render(request, 'pokemons/detail.html', {
       'pokemon': pokemon, 'evolution_form': evolution_form,
       'trainers': trainers_pokemon_doesnt_have 
    })

class PokemonCreate(CreateView):
  model = Pokemon
  fields = ['name', 'type', 'description', 'special', 'hp']

class PokemonUpdate(UpdateView):
  model = Pokemon
  fields = ['type', 'description', 'special', 'hp']

class PokemonDelete(DeleteView):
  model = Pokemon
  success_url = '/pokemons'

def add_evolution(request, pokemon_id):
  # create a ModelForm instance using 
  # the data that was submitted in the form
  form = EvolutionForm(request.POST)
  # validate the form
  print('hello')
  if form.is_valid():
    # We want a model instance, but
    # we can't save to the db yet
    # because we have not assigned the
    # cat_id FK.
    new_evolution = form.save(commit=False)
    new_evolution.pokemon_id = pokemon_id
    new_evolution.save()
    print(new_evolution)
    print('hello')
  return redirect('detail', pokemon_id=pokemon_id)

class TrainerList(ListView):
  print(Trainer.objects.all())
  model = Trainer

class TrainerDetail(DetailView):
  model = Trainer

class TrainerCreate(CreateView):
  model = Trainer
  fields = 'name', 'age'

class TrainerUpdate(UpdateView):
  model = Trainer
  fields = ['name', 'age']

class TrainerDelete(DeleteView):
  model = Trainer
  success_url = '/trainers'

def assoc_trainer(request, pokemon_id, trainer_id):
  Pokemon.objects.get(id=pokemon_id).trainers.add(trainer_id)
  return redirect('detail', pokemon_id=pokemon_id)

def disassoc_trainer(request, pokemon_id, trainer_id):
  Pokemon.objects.get(id=pokemon_id).trainers.remove(trainer_id)
  return redirect('detail', pokemon_id=pokemon_id)
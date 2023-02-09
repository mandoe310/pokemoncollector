import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pokemon, Trainer, Photo
from .forms import EvolutionForm


def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def pokemons_index(request):
    pokemons = Pokemon.objects.filter(user=request.user)
    return render(request, 'pokemons/index.html', {
        'pokemons': pokemons
    })

@login_required
def pokemons_detail(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    id_list = pokemon.trainers.all().values_list('id')
    trainers_pokemon_doesnt_have = Trainer.objects.exclude(id__in=id_list)
    evolution_form = EvolutionForm()
    return render(request, 'pokemons/detail.html', {
       'pokemon': pokemon, 'evolution_form': evolution_form,
       'trainers': trainers_pokemon_doesnt_have 
    })

class PokemonCreate(LoginRequiredMixin, CreateView):
  model = Pokemon
  fields = ['name', 'type', 'description', 'special', 'hp']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PokemonUpdate(LoginRequiredMixin, UpdateView):
  model = Pokemon
  fields = ['type', 'description', 'special', 'hp']

class PokemonDelete(LoginRequiredMixin, DeleteView):
  model = Pokemon
  success_url = '/pokemons'

@login_required
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
  return redirect('detail', pokemon_id=pokemon_id)

class TrainerList(LoginRequiredMixin, ListView):
  print(Trainer.objects.all())
  model = Trainer

class TrainerDetail(LoginRequiredMixin, DetailView):
  model = Trainer

class TrainerCreate(LoginRequiredMixin, CreateView):
  model = Trainer
  fields = 'name', 'age'

class TrainerUpdate(LoginRequiredMixin, UpdateView):
  model = Trainer
  fields = ['name', 'age']

class TrainerDelete(LoginRequiredMixin, DeleteView):
  model = Trainer
  success_url = '/trainers'

@login_required
def assoc_trainer(request, pokemon_id, trainer_id):
  Pokemon.objects.get(id=pokemon_id).trainers.add(trainer_id)
  return redirect('detail', pokemon_id=pokemon_id)

@login_required
def disassoc_trainer(request, pokemon_id, trainer_id):
  Pokemon.objects.get(id=pokemon_id).trainers.remove(trainer_id)
  return redirect('detail', pokemon_id=pokemon_id)

@login_required
def add_photo(request, pokemon_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            Photo.objects.create(url=url, pokemon_id=pokemon_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', pokemon_id=pokemon_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
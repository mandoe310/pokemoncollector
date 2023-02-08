from django.db import models
from django.urls import reverse
from datetime import date

STAGES = (
  ('O', 'One'),
  ('T', 'Two'),
  ('N', 'None'),
)


# Create your models here.
class Trainer(models.Model):
  name = models.CharField(max_length=50)
  age = models.IntegerField()

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('trainers_detail', kwargs={'pk': self.id})


class Pokemon(models.Model):
  name = models.CharField(max_length=100)
  type = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  special = models.TextField(max_length=100)
  hp = models.IntegerField()
  trainers = models.ManyToManyField(Trainer)

  def __str__(self):
    return f'{self.name} ({self.id})'

  def get_absolute_url(self):
    return reverse('detail', kwargs={'pokemon_id': self.id})


class Evolution(models.Model):
  name = models.CharField(max_length=50)
  stage = models.CharField(
    max_length=1,
    choices=STAGES,
    default=STAGES[0][0]
  )

  pokemon = models.ForeignKey(
    Pokemon,
    on_delete=models.CASCADE
  )

  def __str__(self):
    return f"{self.get_stage_display()}"

class Photo(models.Model):
    url = models.CharField(max_length=200)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for pokemon_id: {self.pokemon_id} @{self.url}"


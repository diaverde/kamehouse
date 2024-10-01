import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from .models import People

def index(request):
  people = People.objects.all()
  template = loader.get_template('index.html')
  peopleAtHome = []
  peopleAway = []
  for person in people:
    if person.isHere:
        peopleAtHome.append(person)
    else:
        peopleAway.append(person)
  context = {
    'peopleAtHome': peopleAtHome,
    'peopleAway': peopleAway,
  }
  return HttpResponse(template.render(context, request))

@csrf_protect
@csrf_exempt
def add(request):
  if request.method == 'POST':
    json_data = json.loads(request.body)
    try:
      x = json_data['nombre']
      y = json_data['enCasa']
      person = People(name=x, isHere=y)
      person.save()
    except KeyError:
      return HttpResponseBadRequest("Malformed data!")
    return HttpResponseRedirect(reverse('index'))

@csrf_protect
@csrf_exempt
def delete(request, id):
  person = People.objects.get(id=id)
  person.delete()
  return HttpResponseRedirect(reverse('index'))

@csrf_protect
@csrf_exempt
def update(request, id):
  if request.method == 'PUT':
    json_data = json.loads(request.body)
    try:
      x = json_data['nombre']
      y = json_data['enCasa']
      person = People.objects.get(id=id)
      person.name = x
      person.isHere = y
      person.save()
    except KeyError:
      return HttpResponseBadRequest("Malformed data!")
    return HttpResponseRedirect(reverse('index'))
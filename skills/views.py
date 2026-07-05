import json
from django.views import View  # sem utilização de Django Rest Framework (DRF)
from django.http import HttpRequest, JsonResponse
from .models import Skill

# from django.shortcuts import render # para renderização de HTML


# Create your views here --> with no DRF
class SkillList(View):
    def get(self, request):
        skills = Skill.objects.all()
        dados = [skill.to_json() for skill in skills]
        return JsonResponse(dados, safe=False)

    def post(self, request: HttpRequest):
        body = json.loads(request.body)
        skill = Skill.objects.create(name=body.get("name"))
        return JsonResponse(skill.to_json(), status=201)

from django.urls import path

# from django.views.decorators.csrf import csrf_exempt

from .views import SkillList

app_name = "skills"
urlpatterns = [
    # não precisa de csrf_exempt porque o APIView do DRF já faz isso
    # path("", csrf_exempt(SkillList.as_view()), name="list"),
    path("", SkillList.as_view(), name="list"),
]

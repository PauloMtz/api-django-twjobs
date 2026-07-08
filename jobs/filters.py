from django_filters import rest_framework as filters

from .models import Job


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    # sem implementação porque a classe pai já implementa o necessário
    ...


class JobFilterSet(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    location = filters.CharFilter(field_name="location", lookup_expr="icontains")
    salary_gte = filters.NumberFilter(field_name="salary", lookup_expr="gte")
    salary_lte = filters.NumberFilter(field_name="salary", lookup_expr="lte")
    skills = CharInFilter(field_name="skills__name")

    class Meta:
        model = Job
        fields = {
            "title": [],
            "company": [],
            "location": [],
            "job_type": ["exact"],
            "job_level": ["exact"],
            "salary": [],
            "skills": [],
        }

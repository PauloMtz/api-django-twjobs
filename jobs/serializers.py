from rest_framework import serializers

from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ("is_active",)  # todos os campos, exceto o is_active
        extra_kwargs = {
            "title": {"min_length": 10},
            "salary": {"min_value": 1000},  # o write only abaixo é apenas demonstração
            "description": {"min_length": 10, "max_length": 150, "write_only": True},
            "company": {"min_length": 3},
            "location": {"min_length": 10},
        }

    # o extra_kwargs substitui todas essas validações abaixo
    # def validate_title(self, value):
    #    if len(value) < 5:
    #        raise serializers.ValidationError("deve ter pelo menos 5 caracteres.")
    #    return value

    # def validate_salary(self, value):
    #    if value < 0:
    #        raise serializers.ValidationError("não pode ser negativo.")
    #    return value

    # def validate_description(self, value):
    #    if len(value) < 10:
    #        raise serializers.ValidationError("deve ter pelo menos 10 caracteres.")
    #    return value

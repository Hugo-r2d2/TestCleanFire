from rest_framework import serializers
from .models import MunicipioQueimada

class MunicipioQueimadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MunicipioQueimada
        fields = '__all__'
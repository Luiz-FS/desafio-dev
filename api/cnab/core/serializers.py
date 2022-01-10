from rest_framework import serializers
from core import models


class CNABDocumentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CNABDocumentation
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = "__all__"


class FileSerializer(serializers.ModelSerializer):
    display_status = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = models.File
        fields = "__all__"

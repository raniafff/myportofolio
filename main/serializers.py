from rest_framework import serializers
from django.utils.html import strip_tags
from main.models import Project, Education


class ProjectSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'tech_stack',
            'project_url',
            'project_image_url',
            'star_count',
            'is_starred',
        ]
        read_only_fields = ['id', 'star_count', 'is_starred']

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.starred_by.filter(id=request.user.id).exists()
        return False

    def validate_title(self, value):
        cleaned = strip_tags(value).strip()
        if not cleaned:
            raise serializers.ValidationError("Judul proyek tidak boleh kosong.")
        return cleaned

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate_tech_stack(self, value):
        cleaned = strip_tags(value).strip()
        if not cleaned:
            raise serializers.ValidationError("Tech stack tidak boleh kosong.")
        return cleaned


class EducationSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            'id',
            'institution',
            'degree',
            'start_year',
            'end_year',
            'is_current',
            'description',
            'star_count',
            'is_starred',
        ]
        read_only_fields = ['id', 'star_count', 'is_starred']

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.starred_by.filter(id=request.user.id).exists()
        return False

    def validate_institution(self, value):
        cleaned = strip_tags(value).strip()
        if not cleaned:
            raise serializers.ValidationError("Nama institusi tidak boleh kosong.")
        return cleaned

    def validate_degree(self, value):
        cleaned = strip_tags(value).strip()
        if not cleaned:
            raise serializers.ValidationError("Gelar/jurusan tidak boleh kosong.")
        return cleaned

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate(self, attrs):
        start_year = attrs.get('start_year')
        end_year = attrs.get('end_year')
        is_current = attrs.get('is_current', False)

        if start_year is not None and start_year < 1900:
            raise serializers.ValidationError({"start_year": "Tahun mulai tidak valid."})

        if not is_current and end_year is not None and start_year is not None:
            if end_year < start_year:
                raise serializers.ValidationError({"end_year": "Tahun selesai tidak boleh sebelum tahun mulai."})

        return attrs


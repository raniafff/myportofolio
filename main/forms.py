from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, Textarea, URLInput, NumberInput, CheckboxInput
from django.utils.html import strip_tags
from main.models import Project, Education

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]
        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }
        widgets = {
            "title": TextInput(attrs={"placeholder": "Portfolio Website", "maxlength": 255}),
            "description": Textarea(attrs={"placeholder": "Ceritakan Proyekmu", "rows": 3}),
            "tech_stack": TextInput(attrs={"placeholder": "Django, Python, HTML, CSS"}),
            "project_url": URLInput(attrs={"placeholder": "https://github.com/..."}),
            "project_image_url": URLInput(attrs={"placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000"}),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Nama proyek tidak boleh hanya berisi tag HTML.")
        return title

    def clean_tech_stack(self):
        return strip_tags(self.cleaned_data["tech_stack"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'start_year', 'end_year', 'is_current', 'description']
        labels = {
            'institution': 'Nama Institusi',
            'degree': 'Gelar / Jurusan',
            'start_year': 'Tahun Mulai',
            'end_year': 'Tahun Selesai',
            'is_current': 'Sedang Berjalan (Masih Menempuh)',
            'description': 'Deskripsi / Aktivitas',
        }
        widgets = {
            'institution': TextInput(attrs={'placeholder': 'Contoh: Universitas Indonesia', 'maxlength': 255}),
            'degree': TextInput(attrs={'placeholder': 'Contoh: S1 Sistem Informasi', 'maxlength': 255}),
            'start_year': NumberInput(attrs={'placeholder': 'Contoh: 2022', 'min': 1900, 'max': 2100}),
            'end_year': NumberInput(attrs={'placeholder': 'Contoh: 2026', 'min': 1900, 'max': 2100}),
            'is_current': CheckboxInput(attrs={'class': 'checkbox-input'}),
            'description': Textarea(attrs={'placeholder': 'Ceritakan kegiatan, organisasi, atau pencapaianmu', 'rows': 3}),
        }

    def clean_institution(self):
        institution = strip_tags(self.cleaned_data.get("institution", "")).strip()
        if not institution:
            raise ValidationError("Nama institusi tidak boleh hanya berisi tag HTML.")
        return institution

    def clean_degree(self):
        degree = strip_tags(self.cleaned_data.get("degree", "")).strip()
        if not degree:
            raise ValidationError("Gelar/jurusan tidak boleh hanya berisi tag HTML.")
        return degree

    def clean_description(self):
        return strip_tags(self.cleaned_data.get("description", "")).strip()

    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get('is_current')
        start_year = cleaned_data.get('start_year')
        end_year = cleaned_data.get('end_year')

        if not is_current and not end_year:
            self.add_error('end_year', 'Tahun selesai wajib diisi jika pendidikan tidak sedang berjalan.')
        elif start_year and end_year and end_year < start_year:
            self.add_error('end_year', 'Tahun selesai tidak boleh mendahului tahun mulai.')

        return cleaned_data
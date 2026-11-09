from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Contact, Education, Experience, Hobby, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami dasar pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

    def test_hobbies_url_is_exist(self):
        response = self.client.get('/hobbies/')
        self.assertEqual(response.status_code, 200)

    def test_hobbies_using_correct_template(self):
        response = self.client.get(reverse('main:show_hobbies'))
        self.assertTemplateUsed(response, 'hobbies.html')

    def test_empty_hobbies_list(self):
        response = self.client.get(reverse('main:show_hobbies'))
        self.assertContains(response, "Belum ada data hobi yang ditambahkan.")

    def test_hobby_data_is_displayed(self):
        Hobby.objects.create(
            name="Membaca Buku",
            description="Membaca novel fiksi dan sains",
            frequency="Setiap hari"
        )
        response = self.client.get(reverse('main:show_hobbies'))
        self.assertContains(response, "Membaca Buku")


class ContactHTMXTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name="Ahmad Dahlan",
            email="ahmad@example.com"
        )

    def test_contact_list_page(self):
        response = self.client.get(reverse("main:contact_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contacts.html")
        self.assertContains(response, "Ahmad Dahlan")
        self.assertContains(response, "ahmad@example.com")

    def test_contact_add_htmx(self):
        response = self.client.post(reverse("main:contact_add"), {
            "name": "Budi Santoso",
            "email": "budi@example.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "_contact_rows.html")
        self.assertContains(response, "Budi Santoso")
        self.assertTrue(Contact.objects.filter(name="Budi Santoso").exists())

    def test_contact_search_htmx(self):
        response = self.client.get(reverse("main:contact_search"), {"q": "Ahmad"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ahmad Dahlan")

        response_empty = self.client.get(reverse("main:contact_search"), {"q": "TidakAda"})
        self.assertEqual(response_empty.status_code, 200)
        self.assertContains(response_empty, "Belum ada kontak")

    def test_contact_edit_row_htmx(self):
        response = self.client.get(reverse("main:contact_edit", args=[self.contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "_contact_edit_row.html")
        self.assertContains(response, "value=\"Ahmad Dahlan\"")

    def test_contact_update_htmx(self):
        response = self.client.put(
            reverse("main:contact_update", args=[self.contact.id]),
            data="name=Ahmad+Updated&email=updated@example.com",
            content_type="application/x-www-form-urlencoded"
        )
        self.assertEqual(response.status_code, 200)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "Ahmad Updated")
        self.assertEqual(self.contact.email, "updated@example.com")

    def test_contact_delete_htmx(self):
        response = self.client.delete(reverse("main:contact_delete", args=[self.contact.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())


class ProjectDRFAPITest(APITestCase):
    def setUp(self):
        # Create roles
        self.owner = User.objects.create_superuser(
            username="owner_user",
            password="password123",
            email="owner@example.com"
        )
        self.regular_user = User.objects.create_user(
            username="regular_user",
            password="password123"
        )
        self.editor_user = User.objects.create_user(
            username="editor_user",
            password="password123"
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor_user.groups.add(editor_group)

        # Create sample project
        self.project = Project.objects.create(
            title="Portfolio Website",
            description="Personal developer portfolio with Django",
            tech_stack="Django, HTML, CSS",
            project_url="https://example.com",
            project_image_url="https://example.com/image.png"
        )

    # 1. Visitor Permissions
    def test_visitor_can_read_list_and_detail(self):
        # List
        res_list = self.client.get(reverse("api_v1:api_project_list"))
        self.assertEqual(res_list.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_list.data), 1)

        # Detail
        res_detail = self.client.get(reverse("api_v1:api_project_detail", args=[self.project.id]))
        self.assertEqual(res_detail.status_code, status.HTTP_200_OK)
        self.assertEqual(res_detail.data["title"], "Portfolio Website")

    def test_visitor_cannot_create_or_modify_or_delete(self):
        initial_count = Project.objects.count()

        # Create
        res_create = self.client.post(reverse("api_v1:api_project_list"), {
            "title": "Hacked",
            "description": "Desc",
            "tech_stack": "Python"
        })
        self.assertIn(res_create.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Project.objects.count(), initial_count)
        self.assertFalse(Project.objects.filter(title="Hacked").exists())

        # Update
        res_update = self.client.put(reverse("api_v1:api_project_detail", args=[self.project.id]), {
            "title": "Hacked",
            "description": "Desc",
            "tech_stack": "Python"
        })
        self.assertIn(res_update.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio Website")

        # Delete
        res_delete = self.client.delete(reverse("api_v1:api_project_detail", args=[self.project.id]))
        self.assertIn(res_delete.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertTrue(Project.objects.filter(id=self.project.id).exists())

        # Star
        res_star = self.client.post(reverse("api_v1:api_project_toggle_star", args=[self.project.id]))
        self.assertIn(res_star.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(self.project.starred_by.count(), 0)

    # 2. Regular User Permissions
    def test_regular_user_can_toggle_star(self):
        self.client.force_authenticate(user=self.regular_user)
        res_star = self.client.post(reverse("api_v1:api_project_toggle_star", args=[self.project.id]))
        self.assertEqual(res_star.status_code, status.HTTP_200_OK)
        self.assertTrue(res_star.data["is_starred"])
        self.assertEqual(res_star.data["star_count"], 1)
        self.assertEqual(self.project.starred_by.count(), 1)

        # Toggle again to remove star
        res_unstar = self.client.post(reverse("api_v1:api_project_toggle_star", args=[self.project.id]))
        self.assertEqual(res_unstar.status_code, status.HTTP_200_OK)
        self.assertFalse(res_unstar.data["is_starred"])
        self.assertEqual(res_unstar.data["star_count"], 0)
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_regular_user_cannot_create_or_modify_or_delete(self):
        self.client.force_authenticate(user=self.regular_user)
        initial_count = Project.objects.count()

        res_create = self.client.post(reverse("api_v1:api_project_list"), {
            "title": "New Proj",
            "description": "Desc",
            "tech_stack": "Django"
        })
        self.assertEqual(res_create.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), initial_count)
        self.assertFalse(Project.objects.filter(title="New Proj").exists())

        res_update = self.client.put(reverse("api_v1:api_project_detail", args=[self.project.id]), {
            "title": "Updated",
            "description": "Desc",
            "tech_stack": "Django"
        })
        self.assertEqual(res_update.status_code, status.HTTP_403_FORBIDDEN)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio Website")

        res_delete = self.client.delete(reverse("api_v1:api_project_detail", args=[self.project.id]))
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Project.objects.filter(id=self.project.id).exists())

    # 3. Editor Permissions
    def test_editor_can_modify_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor_user)

        # Can PUT / PATCH
        res_patch = self.client.patch(reverse("api_v1:api_project_detail", args=[self.project.id]), {
            "title": "Portfolio Website v2"
        })
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio Website v2")

        # Cannot POST (create)
        initial_count = Project.objects.count()
        res_create = self.client.post(reverse("api_v1:api_project_list"), {
            "title": "Editor Created",
            "description": "Desc",
            "tech_stack": "Django"
        })
        self.assertEqual(res_create.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), initial_count)
        self.assertFalse(Project.objects.filter(title="Editor Created").exists())

        # Cannot DELETE
        res_delete = self.client.delete(reverse("api_v1:api_project_detail", args=[self.project.id]))
        self.assertEqual(res_delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Project.objects.filter(id=self.project.id).exists())

    # 4. Superuser (Owner) Permissions
    def test_owner_can_create_update_delete(self):
        self.client.force_authenticate(user=self.owner)

        # Create
        res_create = self.client.post(reverse("api_v1:api_project_list"), {
            "title": "New AI App",
            "description": "Artificial Intelligence application",
            "tech_stack": "Python, PyTorch",
            "project_url": "https://example.com/ai",
            "project_image_url": "https://example.com/ai.png"
        })
        self.assertEqual(res_create.status_code, status.HTTP_201_CREATED)
        new_id = res_create.data["id"]
        self.assertTrue(Project.objects.filter(id=new_id).exists())

        # Delete
        res_delete = self.client.delete(reverse("api_v1:api_project_detail", args=[new_id]))
        self.assertEqual(res_delete.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(id=new_id).exists())

    # 5. Search filtering & Validation
    def test_project_search_query(self):
        res_match = self.client.get(reverse("api_v1:api_project_list"), {"q": "Portfolio"})
        self.assertEqual(res_match.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_match.data), 1)

        res_nomatch = self.client.get(reverse("api_v1:api_project_list"), {"q": "NonExistentKeyword"})
        self.assertEqual(res_nomatch.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res_nomatch.data), 0)

    def test_project_validation_empty_title(self):
        self.client.force_authenticate(user=self.owner)
        initial_count = Project.objects.count()
        res = self.client.post(reverse("api_v1:api_project_list"), {
            "title": "   ",
            "description": "Desc",
            "tech_stack": "Django"
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Project.objects.count(), initial_count)

    # 6. CSRF Enforcement with APIClient & .login()
    def test_csrf_rejection_without_token(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        csrf_client.login(username="owner_user", password="password123")
        initial_count = Project.objects.count()

        # POST without X-CSRFToken header must be rejected
        res = csrf_client.post(reverse("api_v1:api_project_list"), {
            "title": "CSRF Project",
            "description": "Desc",
            "tech_stack": "Django"
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), initial_count)
        self.assertFalse(Project.objects.filter(title="CSRF Project").exists())

    def test_csrf_success_with_token(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        csrf_client.login(username="owner_user", password="password123")

        # Set cookie by accessing page
        csrf_client.get(reverse("main:show_project"))
        csrf_token = csrf_client.cookies.get("csrftoken").value

        res = csrf_client.post(
            reverse("api_v1:api_project_list"),
            {
                "title": "CSRF Verified Project",
                "description": "Desc",
                "tech_stack": "Django"
            },
            format="json",
            headers={"X-CSRFToken": csrf_token}
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(title="CSRF Verified Project").exists())


class EducationDRFAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner_edu",
            password="password123"
        )
        self.regular_user = User.objects.create_user(
            username="regular_edu",
            password="password123"
        )
        self.editor_user = User.objects.create_user(
            username="editor_edu",
            password="password123"
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        self.editor_user.groups.add(editor_group)

        self.education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            start_year=2024,
            end_year=2028,
            is_current=True,
            description="Kuliah di Fasilkom UI"
        )

    def test_visitor_can_read_education(self):
        res = self.client.get(reverse("api_v1:api_education_list"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_visitor_cannot_write_education(self):
        initial_count = Education.objects.count()
        res_create = self.client.post(reverse("api_v1:api_education_list"), {
            "institution": "Hacked",
            "degree": "Hacked",
            "start_year": 2020
        })
        self.assertIn(res_create.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
        self.assertEqual(Education.objects.count(), initial_count)

    def test_regular_user_cannot_create_education(self):
        self.client.force_authenticate(user=self.regular_user)
        initial_count = Education.objects.count()
        res = self.client.post(reverse("api_v1:api_education_list"), {
            "institution": "ITB",
            "degree": "Informatika",
            "start_year": 2020
        })
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Education.objects.count(), initial_count)

    def test_editor_can_modify_education(self):
        self.client.force_authenticate(user=self.editor_user)
        res_patch = self.client.patch(reverse("api_v1:api_education_detail", args=[self.education.id]), {
            "degree": "S1 Ilmu Komputer"
        })
        self.assertEqual(res_patch.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S1 Ilmu Komputer")

    def test_owner_can_create_and_delete_education(self):
        self.client.force_authenticate(user=self.owner)
        res = self.client.post(reverse("api_v1:api_education_list"), {
            "institution": "SMA Negeri 1",
            "degree": "MIPA",
            "start_year": 2021,
            "end_year": 2024,
            "is_current": False,
            "description": "Jurusan MIPA"
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        new_id = res.data["id"]
        self.assertTrue(Education.objects.filter(id=new_id).exists())

        res_del = self.client.delete(reverse("api_v1:api_education_detail", args=[new_id]))
        self.assertEqual(res_del.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Education.objects.filter(id=new_id).exists())

    def test_toggle_education_star(self):
        self.client.force_authenticate(user=self.regular_user)
        res = self.client.post(reverse("api_v1:api_education_toggle_star", args=[self.education.id]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["is_starred"])
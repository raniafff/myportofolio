from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience
from main.models import Hobby
from main.models import Contact


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
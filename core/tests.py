import json

from django.test import Client, TestCase

from .models import MenuItem


class MenuApiTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        for idx in range(1, 16):
            MenuItem.objects.create(
                name=f"Item {idx}",
                description="Kenyan fast food",
                category=MenuItem.Category.SNACK,
                price_kes="150.00",
                is_available=True,
            )

    def test_menu_pagination_allows_three_pages(self) -> None:
        response = self.client.get("/api/menu/?page=3")
        self.assertEqual(response.status_code, 200)

    def test_menu_pagination_blocks_page_four(self) -> None:
        response = self.client.get("/api/menu/?page=4")
        self.assertEqual(response.status_code, 400)


class ContactApiTests(TestCase):
    def test_create_contact_message(self) -> None:
        payload = {
            "customer_name": "Amina",
            "phone_number": "+254700000000",
            "message": "Do you offer tea and mandazi?",
        }
        response = self.client.post(
            "/api/contact/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

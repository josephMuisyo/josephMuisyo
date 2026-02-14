# Kenyan Fast Food Restaurant Backend (Django)

This project provides a Django backend for a local Kenyan fast-food and snacks restaurant website.

## Features
- Menu API for fast foods, snacks, and drinks.
- Contact API for customer inquiries.
- Scroll/pagination support limited to **3 pages** as requested.
- Django admin support for managing menu items and messages.

## API Endpoints
- `GET /api/health/` - Service health check.
- `GET /api/menu/?page=1&category=snack` - Paginated menu list (pages 1 to 3 only).
- `POST /api/contact/` - Submit customer message.

## Setup
1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Create admin user:
   ```bash
   python manage.py createsuperuser
   ```
5. Run server:
   ```bash
   python manage.py runserver
   ```

## Example Contact Payload
```json
{
  "customer_name": "Amina Otieno",
  "phone_number": "+254712345678",
  "message": "Can I get samosa and chips delivered in Westlands?"
}
```

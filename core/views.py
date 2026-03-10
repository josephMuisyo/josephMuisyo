import json

from django.core.paginator import EmptyPage, Paginator
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import CustomerMessage, MenuItem

MAX_SCROLL_PAGES = 3
PAGE_SIZE = 6


def menu_item_to_dict(menu_item: MenuItem) -> dict:
    return {
        "id": menu_item.id,
        "name": menu_item.name,
        "description": menu_item.description,
        "category": menu_item.category,
        "price_kes": float(menu_item.price_kes),
        "is_available": menu_item.is_available,
    }


@require_GET
def health_check(_: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok", "service": "restaurant-backend"})


@require_GET
def menu_list(request: HttpRequest) -> JsonResponse:
    page_number = int(request.GET.get("page", 1))
    category = request.GET.get("category")

    queryset = MenuItem.objects.filter(is_available=True)
    if category:
        queryset = queryset.filter(category=category)

    paginator = Paginator(queryset, PAGE_SIZE)

    if page_number < 1:
        page_number = 1
    if page_number > MAX_SCROLL_PAGES:
        return JsonResponse(
            {
                "detail": "Only the first three scroll pages are available.",
                "max_pages": MAX_SCROLL_PAGES,
            },
            status=400,
        )

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = []

    results = [menu_item_to_dict(item) for item in page_obj]

    return JsonResponse(
        {
            "page": page_number,
            "page_size": PAGE_SIZE,
            "max_scroll_pages": MAX_SCROLL_PAGES,
            "total_items": paginator.count,
            "items": results,
        }
    )


@csrf_exempt
@require_POST
def customer_message_create(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"detail": "Invalid JSON payload."}, status=400)

    required_fields = ["customer_name", "phone_number", "message"]
    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        return JsonResponse(
            {"detail": "Missing required fields.", "missing_fields": missing},
            status=400,
        )

    customer_message = CustomerMessage.objects.create(
        customer_name=payload["customer_name"].strip(),
        phone_number=payload["phone_number"].strip(),
        message=payload["message"].strip(),
    )

    return JsonResponse(
        {
            "id": customer_message.id,
            "detail": "Your message has been received. We will contact you shortly.",
        },
        status=201,
    )

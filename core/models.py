from django.db import models


class MenuItem(models.Model):
    class Category(models.TextChoices):
        FAST_FOOD = "fast_food", "Fast Food"
        SNACK = "snack", "Snack"
        DRINK = "drink", "Drink"

    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices)
    price_kes = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.category})"


class CustomerMessage(models.Model):
    customer_name = models.CharField(max_length=120)
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Message from {self.customer_name}"

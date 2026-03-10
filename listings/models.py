from django.db import models


class Developer(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    company = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Property(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=140)
    location = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    area_sqft = models.PositiveIntegerField()
    image_url = models.URLField()
    description = models.TextField()

    def __str__(self):
        return self.title

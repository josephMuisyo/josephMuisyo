from django.shortcuts import render
from .models import Developer, Property


def home(request):
    developers = Developer.objects.all().order_by('name')
    properties = Property.objects.select_related('developer').all().order_by('price')

    if not developers.exists():
        seed_demo_data()
        developers = Developer.objects.all().order_by('name')
        properties = Property.objects.select_related('developer').all().order_by('price')

    context = {
        'developers': developers,
        'properties': properties,
        'payment_methods': [
            'Bank transfer',
            'Cheque deposits',
            'Online money transfer',
            'Visa',
        ],
    }
    return render(request, 'listings/home.html', context)


def seed_demo_data():
    dev1 = Developer.objects.create(
        name='Grace Wanjiru',
        email='grace@urbannest.dev',
        phone='+254-700-111-222',
        company='Urban Nest Developers',
    )
    dev2 = Developer.objects.create(
        name='Daniel Kiptoo',
        email='daniel@horizonhomes.co',
        phone='+254-700-333-444',
        company='Horizon Homes',
    )
    dev3 = Developer.objects.create(
        name='Amina Yusuf',
        email='amina@primebrick.africa',
        phone='+254-700-555-666',
        company='Prime Brick Africa',
    )

    Property.objects.bulk_create([
        Property(
            developer=dev1,
            title='3 Bedroom Garden Villa',
            location='Nairobi, Karen',
            price=22000000,
            bedrooms=3,
            bathrooms=3,
            area_sqft=2800,
            image_url='https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&q=80',
            description='A serene gated villa with private garden and nearby schools.',
        ),
        Property(
            developer=dev2,
            title='2 Bedroom Modern Apartment',
            location='Nairobi, Kilimani',
            price=11500000,
            bedrooms=2,
            bathrooms=2,
            area_sqft=1400,
            image_url='https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80',
            description='Contemporary apartment near malls, offices and social amenities.',
        ),
        Property(
            developer=dev3,
            title='4 Bedroom Family Maisonette',
            location='Mombasa, Nyali',
            price=26500000,
            bedrooms=4,
            bathrooms=4,
            area_sqft=3200,
            image_url='https://images.unsplash.com/photo-1570129477492-45c003edd2be?auto=format&fit=crop&w=1200&q=80',
            description='Spacious maisonette perfect for large families near the beach.',
        ),
    ])

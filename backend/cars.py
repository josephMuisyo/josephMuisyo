from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Car:
    id: str
    brand: str
    model: str
    year: int
    mileage: int
    color: str
    price: int


BRAND_MODELS: dict[str, list[str]] = {
    "Toyota": ["Corolla", "RAV4", "Hilux", "Camry", "Prado", "Yaris"],
    "Mercedes": ["C200", "E300", "GLA", "GLE", "A180", "S500"],
    "Bmw": ["320i", "X3", "X5", "M3", "118i", "530d"],
    "Honda": ["Civic", "CR-V", "Accord", "Fit", "HR-V", "Pilot"],
    "Mitsubishi": ["Lancer", "Outlander", "Pajero", "ASX", "Eclipse Cross", "Triton"],
}

COLORS = ["White", "Black", "Silver", "Red", "Blue", "Grey", "Green", "Orange"]
YEARS = [year for year in range(2011, 2025)]


def generate_cars() -> list[Car]:
    cars: list[Car] = []
    count = 1

    for brand, models in BRAND_MODELS.items():
        for i in range(36):
            model = models[i % len(models)]
            year = YEARS[(i + len(models)) % len(YEARS)]
            mileage = 5000 + i * 2300 + len(models) * 100
            color = COLORS[(i + count) % len(COLORS)]
            price = 12000 + i * 1450 + len(brand) * 780

            cars.append(
                Car(
                    id=f"{brand.lower()}-{count}",
                    brand=brand,
                    model=model,
                    year=year,
                    mileage=mileage,
                    color=color,
                    price=price,
                )
            )
            count += 1

    return cars


CARS = generate_cars()
CARS_JSON = [asdict(car) for car in CARS]
BRANDS = list(BRAND_MODELS.keys())

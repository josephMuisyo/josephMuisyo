const brandModels = {
  Toyota: ['Corolla', 'RAV4', 'Hilux', 'Camry', 'Prado', 'Yaris'],
  Mercedes: ['C200', 'E300', 'GLA', 'GLE', 'A180', 'S500'],
  Bmw: ['320i', 'X3', 'X5', 'M3', '118i', '530d'],
  Honda: ['Civic', 'CR-V', 'Accord', 'Fit', 'HR-V', 'Pilot'],
  Mitsubishi: ['Lancer', 'Outlander', 'Pajero', 'ASX', 'Eclipse Cross', 'Triton'],
};

const colors = ['White', 'Black', 'Silver', 'Red', 'Blue', 'Grey', 'Green', 'Orange'];

const years = Array.from({ length: 14 }, (_, index) => 2011 + index);

const cars = [];
let count = 1;

Object.entries(brandModels).forEach(([brand, models]) => {
  for (let i = 0; i < 36; i += 1) {
    const model = models[i % models.length];
    const year = years[(i + models.length) % years.length];
    const mileage = 5000 + i * 2300 + models.length * 100;
    const color = colors[(i + count) % colors.length];
    const price = 12000 + i * 1450 + brand.length * 780;

    cars.push({
      id: `${brand.toLowerCase()}-${count}`,
      brand,
      model,
      year,
      mileage,
      color,
      price,
    });

    count += 1;
  }
});

module.exports = { cars };

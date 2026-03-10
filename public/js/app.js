const selectedCarKey = 'selectedCar';
const carGrid = document.getElementById('carGrid');
const brandFilter = document.getElementById('brandFilter');
const summary = document.getElementById('summary');

let cars = [];

const renderCars = (brand = 'all') => {
  carGrid.innerHTML = '';
  const filteredCars = brand === 'all' ? cars : cars.filter((car) => car.brand === brand);

  filteredCars.forEach((car) => {
    const card = document.createElement('article');
    card.className = 'car-card';
    card.innerHTML = `
      <h3>${car.brand} ${car.model}</h3>
      <p><strong>Year:</strong> ${car.year}</p>
      <p><strong>Mileage:</strong> ${car.mileage.toLocaleString()} km</p>
      <p><strong>Color:</strong> ${car.color}</p>
      <p class="price"><strong>Price:</strong> $${car.price.toLocaleString()}</p>
      <button class="card-btn" data-id="${car.id}">Select this vehicle</button>
    `;
    carGrid.appendChild(card);
  });

  document.querySelectorAll('.card-btn').forEach((button) => {
    button.addEventListener('click', () => {
      const selected = filteredCars.find((car) => car.id === button.dataset.id);
      localStorage.setItem(selectedCarKey, JSON.stringify(selected));
      window.location.href = '/selection';
    });
  });
};

const initialize = async () => {
  const response = await fetch('/api/cars');
  const data = await response.json();
  cars = data.cars;

  summary.innerHTML = `
    <h2>Available inventory</h2>
    <p>Total cars displayed: <strong>${data.total}</strong></p>
    <p>Brands on display: <strong>${data.brands.join(', ')}</strong></p>
  `;

  data.brands.forEach((brand) => {
    const option = document.createElement('option');
    option.value = brand;
    option.textContent = brand;
    brandFilter.appendChild(option);
  });

  brandFilter.addEventListener('change', (event) => {
    renderCars(event.target.value);
  });

  renderCars();
};

initialize();

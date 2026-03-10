const selectionMessage = document.getElementById('selectionMessage');
const selectedCarPanel = document.getElementById('selectedCar');
const selectedCar = JSON.parse(localStorage.getItem('selectedCar'));

if (!selectedCar) {
  selectionMessage.innerHTML = '<h2>No vehicle selected</h2><p>Please choose one vehicle from the inventory page.</p>';
  selectedCarPanel.innerHTML = '<p>Your selected vehicle details will appear here.</p>';
} else {
  selectionMessage.innerHTML = `<h2>Selected vehicle confirmed</h2>
    <p>You have selected exactly one vehicle. You can proceed to checkout.</p>
    <a class="primary-btn" href="/checkout">Proceed to checkout</a>`;

  selectedCarPanel.innerHTML = `
    <h3>${selectedCar.brand} ${selectedCar.model}</h3>
    <p><strong>Year of manufacture:</strong> ${selectedCar.year}</p>
    <p><strong>Mileage:</strong> ${selectedCar.mileage.toLocaleString()} km</p>
    <p><strong>Color:</strong> ${selectedCar.color}</p>
    <p><strong>Price:</strong> $${selectedCar.price.toLocaleString()}</p>
    <p><strong>Car ID:</strong> ${selectedCar.id}</p>
  `;
}

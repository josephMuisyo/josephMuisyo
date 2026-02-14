const checkoutForm = document.getElementById('checkoutForm');
const paymentMethod = document.getElementById('paymentMethod');
const depositField = document.getElementById('depositField');
const depositPercent = document.getElementById('depositPercent');
const carIdInput = document.getElementById('carId');
const checkoutResult = document.getElementById('checkoutResult');

const selectedCar = JSON.parse(localStorage.getItem('selectedCar'));

if (selectedCar) {
  carIdInput.value = selectedCar.id;
  checkoutResult.innerHTML = `<h3>Selected vehicle</h3><p>${selectedCar.brand} ${selectedCar.model} (${selectedCar.year}) - $${selectedCar.price.toLocaleString()}</p>`;
} else {
  checkoutResult.innerHTML = '<p>No car selected yet. Go to Inventory and pick one car first.</p>';
}

const updateDepositField = () => {
  const isHirePurchase = paymentMethod.value === 'hire purchase';
  depositField.style.display = isHirePurchase ? 'grid' : 'none';
};

updateDepositField();
paymentMethod.addEventListener('change', updateDepositField);

checkoutForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  if (!selectedCar) {
    checkoutResult.innerHTML = '<p>Please select a car before checkout.</p>';
    return;
  }

  const payload = {
    carId: selectedCar.id,
    paymentMethod: paymentMethod.value,
  };

  if (paymentMethod.value === 'hire purchase') {
    payload.depositPercent = Number(depositPercent.value);
  }

  const response = await fetch('/api/checkout', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await response.json();

  checkoutResult.innerHTML = response.ok
    ? `<h3>Success</h3><p>${data.message}</p><p>Payment method: ${data.paymentMethod}</p>
       ${data.depositPercent ? `<p>Deposit: ${data.depositPercent}%</p>` : ''}`
    : `<h3>Checkout failed</h3><p>${data.message}</p>`;
});

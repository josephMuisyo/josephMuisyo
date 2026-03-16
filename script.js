const defaultReviews = [
  {
    name: 'Grace Wanjiku',
    property: 'Apartment block in Nairobi',
    rating: 5,
    text: 'Ray Properties improved occupancy and tenant communication within three months.'
  },
  {
    name: 'Otieno Mwangi',
    property: 'Retail units in Mombasa',
    rating: 4,
    text: 'Very responsive management team and clear monthly financial statements.'
  },
  {
    name: 'Amina Hassan',
    property: 'Farm lease in Eldoret',
    rating: 5,
    text: 'Professional handling of lease renewals and maintenance coordination.'
  }
];

function setupMobileMenu() {
  const toggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');
  if (!toggle || !navLinks) return;

  toggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
}

function setFooterYear() {
  const yearNodes = document.querySelectorAll('#year');
  yearNodes.forEach((year) => {
    year.textContent = new Date().getFullYear();
  });
}

function renderReviews() {
  const reviewGrid = document.getElementById('review-grid');
  if (!reviewGrid) return;

  reviewGrid.innerHTML = defaultReviews
    .map(
      (review) => `
        <article class="card">
          <h3>${review.name}</h3>
          <p class="review-meta">Property: ${review.property}</p>
          <p class="review-meta">Rating: ${'⭐'.repeat(review.rating)}</p>
          <p>${review.text}</p>
        </article>
      `
    )
    .join('');
}

function setupPricingForm() {
  const form = document.getElementById('pricing-form');
  const result = document.getElementById('estimate-result');
  if (!form || !result) return;

  const sizeRates = { small: 18000, medium: 35000, large: 65000 };
  const locationRates = { regional: 5000, urban: 12000, major: 20000 };
  const termDiscountFactor = { short: 1, mid: 0.95, long: 0.9 };

  form.addEventListener('submit', (event) => {
    event.preventDefault();

    const size = document.getElementById('property-size').value;
    const location = document.getElementById('property-location').value;
    const worth = Number(document.getElementById('property-worth').value);
    const term = document.getElementById('management-term').value;

    const valueFactor = worth * 0.0025;
    const gross = sizeRates[size] + locationRates[location] + valueFactor;
    const estimate = Math.round(gross * termDiscountFactor[term]);

    result.innerHTML = `
      <strong>Estimated Monthly Management Charge:</strong> KES ${estimate.toLocaleString()}<br />
      <small>This estimate is based on size, location, property worth estimate, and intended management term.</small>
    `;
  });
}

setupMobileMenu();
setFooterYear();
renderReviews();
setupPricingForm();

const services = [
  { name: 'Classic Manicure', category: 'nails', price: 800, description: 'Nail shaping, cuticle care, and polish finish.' },
  { name: 'Gel Polish + Manicure', category: 'nails', price: 1500, description: 'Long-lasting gel polish with neat manicure prep.' },
  { name: 'Acrylic Full Set', category: 'nails', price: 3000, description: 'Stylish acrylic extension set with your preferred length.' },
  { name: 'Nail Art Design', category: 'nails', price: 700, description: 'Creative custom nail art per set.' },
  { name: 'Express Facial', category: 'spa', price: 1800, description: 'Quick cleansing facial for a fresh and glowing skin.' },
  { name: 'Deep Cleansing Facial', category: 'spa', price: 3200, description: 'Steam, exfoliation, mask and hydration treatment.' },
  { name: 'Body Scrub & Polish', category: 'spa', price: 3500, description: 'Full body exfoliation for smooth radiant skin.' },
  { name: 'Pedicure Deluxe', category: 'spa', price: 1800, description: 'Foot soak, scrub, callus care, and polish.' },
  { name: 'Swedish Massage (60 min)', category: 'massage', price: 3500, description: 'Relaxing full body massage for stress relief.' },
  { name: 'Deep Tissue Massage (60 min)', category: 'massage', price: 4200, description: 'Targeted pressure for muscle tension and pain relief.' },
  { name: 'Hot Stone Massage (75 min)', category: 'massage', price: 5000, description: 'Warm stone therapy for deeper relaxation and circulation.' },
  { name: 'Aromatherapy Massage (60 min)', category: 'massage', price: 3900, description: 'Calming essential oils blended with soothing massage.' },
  { name: 'Wash & Blow Dry', category: 'hair', price: 1200, description: 'Hair wash, treatment and polished blow dry finish.' },
  { name: 'Braiding (Simple Lines)', category: 'hair', price: 2500, description: 'Neat protective style for everyday elegance.' },
  { name: 'Wig Installation', category: 'hair', price: 3000, description: 'Secure and natural-looking wig install.' },
  { name: 'Hair Treatment + Steam', category: 'hair', price: 2200, description: 'Repair and strengthen dry or damaged hair.' },
  { name: 'Soft Glam Makeup', category: 'makeup', price: 2500, description: 'Natural glam look perfect for events and photos.' },
  { name: 'Bridal Makeup', category: 'makeup', price: 6500, description: 'Long-wear bridal package with consultation.' }
];

const defaultReviews = [
  {
    name: 'Mercy N.',
    service: 'Gel Polish + Manicure',
    rating: 5,
    text: 'Super neat nails and very friendly team. My set lasted over 3 weeks!'
  },
  {
    name: 'Brenda W.',
    service: 'Deep Tissue Massage',
    rating: 5,
    text: 'Best massage I have had around Rongai. The ambiance is calm and professional.'
  },
  {
    name: 'Linet A.',
    service: 'Braiding + Pedicure',
    rating: 4,
    text: 'Loved the service variety. I got everything done in one visit and on time.'
  }
];

function formatKES(amount) {
  return new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 }).format(amount);
}

function renderServices(filter = 'all') {
  const grid = document.getElementById('service-grid');
  const select = document.getElementById('selected-service');
  if (!grid) return;

  const filtered = filter === 'all' ? services : services.filter((item) => item.category === filter);
  grid.innerHTML = filtered
    .map(
      (item) => `
      <article class="card">
        <span class="tag">${item.category}</span>
        <h3>${item.name}</h3>
        <p>${item.description}</p>
        <p class="price">${formatKES(item.price)}</p>
      </article>
    `
    )
    .join('');

  if (select) {
    select.innerHTML = '<option value="">Choose a service</option>';
    services.forEach((service) => {
      const option = document.createElement('option');
      option.value = service.name;
      option.textContent = `${service.name} - ${formatKES(service.price)}`;
      select.appendChild(option);
    });
  }
}

function setupFilters() {
  const filterButtons = document.querySelectorAll('.filter-btn');
  if (!filterButtons.length) return;

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      filterButtons.forEach((btn) => btn.classList.remove('active'));
      button.classList.add('active');
      renderServices(button.dataset.filter);
    });
  });
}

function setupBookingForm() {
  const form = document.getElementById('booking-form');
  const message = document.getElementById('booking-message');
  if (!form || !message) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const name = document.getElementById('name').value.trim();
    const service = document.getElementById('selected-service').value;
    const date = document.getElementById('date').value;

    message.textContent = `Thank you, ${name}! Your request for ${service} on ${date} has been received. We will contact you on +25477879217 for confirmation.`;
    message.style.color = '#7a1d55';
    form.reset();
  });
}

function getReviews() {
  const stored = localStorage.getItem('annie-beauty-reviews');
  if (!stored) return defaultReviews;
  try {
    const parsed = JSON.parse(stored);
    return Array.isArray(parsed) ? parsed : defaultReviews;
  } catch (error) {
    return defaultReviews;
  }
}

function saveReviews(reviews) {
  localStorage.setItem('annie-beauty-reviews', JSON.stringify(reviews));
}

function renderReviews() {
  const reviewGrid = document.getElementById('review-grid');
  if (!reviewGrid) return;

  const reviews = getReviews();
  reviewGrid.innerHTML = reviews
    .map(
      (review) => `
      <article class="card">
        <h3>${review.name}</h3>
        <p class="review-meta">Service: ${review.service}</p>
        <p class="review-meta">Rating: ${'⭐'.repeat(review.rating)}</p>
        <p>${review.text}</p>
      </article>
    `
    )
    .join('');
}

function setupReviewForm() {
  const form = document.getElementById('review-form');
  const message = document.getElementById('review-message');
  if (!form || !message) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const newReview = {
      name: document.getElementById('reviewer-name').value.trim(),
      service: document.getElementById('review-service').value.trim(),
      rating: Number(document.getElementById('review-rating').value),
      text: document.getElementById('review-text').value.trim()
    };

    const updatedReviews = [newReview, ...getReviews()];
    saveReviews(updatedReviews);
    renderReviews();
    form.reset();
    message.textContent = 'Thanks for your feedback! Your review has been posted.';
    message.style.color = '#7a1d55';
  });
}

function setupMobileMenu() {
  const toggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');
  if (!toggle || !navLinks) return;

  toggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
  });
}

function setFooterYear() {
  const yearElement = document.getElementById('year');
  if (yearElement) yearElement.textContent = new Date().getFullYear();
}

renderServices();
setupFilters();
setupBookingForm();
renderReviews();
setupReviewForm();
setupMobileMenu();
setFooterYear();

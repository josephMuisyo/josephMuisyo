const compareBoxes = Array.from(document.querySelectorAll('.compare-box'));
const buyBoxes = Array.from(document.querySelectorAll('.buy-box'));
const propertyCards = Array.from(document.querySelectorAll('.property-card'));
const selectedCount = document.getElementById('selected-count');
const comparisonTable = document.getElementById('comparison-table');
const paymentForm = document.getElementById('payment-form');
const paymentMessage = document.getElementById('payment-message');

function getPropertyFromCard(card) {
    const id = Number(card.dataset.id);
    return window.PROPERTY_DATA.find((item) => item.id === id);
}

function updateComparison() {
    const selected = propertyCards
        .filter((card) => card.querySelector('.compare-box').checked)
        .map(getPropertyFromCard);

    if (selected.length < 2) {
        comparisonTable.innerHTML = '<p>Select at least 2 homes to compare side-by-side.</p>';
        return;
    }

    const header = selected.map((home) => `<th>${home.title}</th>`).join('');
    const rows = [
        ['Location', (home) => home.location],
        ['Price (KES)', (home) => home.price],
        ['Bedrooms', (home) => home.bedrooms],
        ['Bathrooms', (home) => home.bathrooms],
        ['Area (sqft)', (home) => home.area],
    ].map(([label, accessor]) =>
        `<tr><td>${label}</td>${selected.map((home) => `<td>${accessor(home)}</td>`).join('')}</tr>`
    ).join('');

    comparisonTable.innerHTML = `<table><thead><tr><th>Feature</th>${header}</tr></thead><tbody>${rows}</tbody></table>`;
}

function updateSelectedCount() {
    const count = buyBoxes.filter((box) => box.checked).length;
    selectedCount.textContent = count;
}

compareBoxes.forEach((box) => box.addEventListener('change', updateComparison));
buyBoxes.forEach((box) => box.addEventListener('change', updateSelectedCount));

paymentForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const count = buyBoxes.filter((box) => box.checked).length;
    const method = paymentForm.querySelector('input[name="payment_method"]:checked')?.value;

    if (count === 0) {
        paymentMessage.textContent = 'Select at least one home before making payment.';
        return;
    }

    paymentMessage.textContent = `Great! You selected ${count} home(s). Continue with ${method}.`;
});

const mapRoot = ReactDOM.createRoot(document.getElementById('react-map-root'));

function MapEmbed({ location }) {
    const src = `https://www.google.com/maps?q=${encodeURIComponent(location)}&output=embed`;
    return <iframe title="Google map" src={src} loading="lazy" width="100%" height="360"></iframe>;
}

function MapContainer() {
    const [location, setLocation] = React.useState(document.getElementById('location-input').value);

    React.useEffect(() => {
        const btn = document.getElementById('map-btn');
        const input = document.getElementById('location-input');
        const handler = () => setLocation(input.value || 'Nairobi');
        btn.addEventListener('click', handler);
        return () => btn.removeEventListener('click', handler);
    }, []);

    return (
        <div className="map-wrapper">
            <MapEmbed location={location} />
        </div>
    );
}

mapRoot.render(<MapContainer />);
updateComparison();
updateSelectedCount();

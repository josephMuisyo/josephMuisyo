# HomeMatch Realty Web App

Django-based real estate matching platform where developers list homes and customers can:

- See developer contacts for direct communication
- Compare 2+ homes side-by-side
- Select multiple homes to buy
- Choose only the approved payment methods: Bank transfer, Cheque deposits, Online money transfer, and Visa
- Explore preferred locations using a React-prop driven Google Maps embed

## Run

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

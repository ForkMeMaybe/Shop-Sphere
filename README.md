# Shop-Sphere E-Commerce Backend

Welcome to the backend of Shop-Sphere, a robust e-commerce application designed to provide a seamless shopping experience. This repository contains the backend logic, database models, APIs, and integrations required to power the Shop-Sphere platform.

## 🚀 Hosted At

Access the live application backend at: [https://shop-sphere-app.onrender.com/](https://shop-sphere-app.onrender.com/)
Access the live application frontend at: [https://shop-sphere-frontend.onrender.com//](https://shop-sphere-frontend.onrender.com//)

---

## 🛠️ Features

- **Razorpay**: Razorpay integration for online payments.
- **Product Management**: APIs to manage product listings, categories, and inventory.
- **User Authentication**: Secure user login, registration and password reset functionality.
- **Order Management**: Handle cart, orders.
- **Admin Dashboard**: Manage users, products, and orders efficiently.
- **Scalable Architecture**: Designed for performance and scalability.

---

## 🛑 Requirements

Ensure you have the following installed on your system:

- Python *
- pip or pipenv (Python package manager)
- A virtual environment tool (e.g., `venv` or `virtualenv`)
- A database (e.g., PostgreSQL, SQLite for local development)

---

## 🛠️ Setup Instructions

Follow these steps to get the backend running locally:

1. **Clone the Repository**
   ```bash
   HTTPS:
   git clone [https://github.com/yourusername/shop-sphere-backend.git](https://github.com/ForkMeMaybe/Shop-Sphere.git)
   SSH:
   git clone git@github.com:ForkMeMaybe/Shop-Sphere.git
   cd Shop-Sphere
   ```

2. **Create and Activate a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

   or use pipenv directly
   pipenv install -r requirements.txt
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   -- or
   pipenv install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory and add the following:
   ```env
   For development purposed just make change in dev.py accordingly and for production set the following:
   SECRET_KEY=your_secret_key_here
   DEBUG=your_debug_conf
   DATABASE_URL=your_database_connection_string
   ALLOWED_HOSTS=allowed_hosts_separated_by_space
   REDIS_URL=your_redis_url
   ```

5. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

---

## 🧪 Testing

Run the test suite to ensure everything is working as expected:

```bash
python manage.py pytest
```

---

## 📁 Project Structure

```plaintext
Directory structure:
└── forkmemaybe-shop-sphere/
    ├── Pipfile
    ├── celerybeat-schedule
    ├── db.sqlite3
    ├── manage.py
    ├── pytest.ini
    ├── requirements.txt
    ├── Shop_Sphere/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── celery.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── settings/
    │       ├── common.py
    │       ├── dev.py
    │       └── prod.py
    ├── core/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── migrations/
    │   │   ├── 0001_initial.py
    │   │   └── __init__.py
    │   ├── signals/
    │   │   └── handlers.py
    │   ├── static/
    │   │   └── core/
    │   │       └── styles.css
    │   └── templates/
    │       └── core/
    │           └── index.html
    ├── likes/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tests.py
    │   ├── views.py
    │   └── migrations/
    │       ├── 0001_initial.py
    │       └── __init__.py
    ├── locustfiles/
    │   └── browse_products.py
    ├── playground/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── tasks.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── views.py
    │   ├── migrations/
    │   │   └── __init__.py
    │   ├── static/
    │   │   └── images/
    │   └── templates/
    │       ├── hello.html
    │       └── emails/
    │           └── hello.html
    ├── store/
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── filters.py
    │   ├── models.py
    │   ├── pagination.py
    │   ├── permissions.py
    │   ├── serializers.py
    │   ├── tests.py
    │   ├── urls.py
    │   ├── validators.py
    │   ├── views.py
    │   ├── migrations/
    │   │   ├── 0001_initial.py
    │   │   ├── 0002_rename_price_product_unit_price.py
    │   │   ├── 0003_product_slug.py
    │   │   ├── 0004_alter_collection_options_alter_customer_options_and_more.py
    │   │   ├── 0005_rename_reviews_review.py
    │   │   ├── 0006_remove_cartitem_cart_remove_cartitem_product_and_more.py
    │   │   ├── 0007_cart_cartitem.py
    │   │   ├── 0008_alter_cartitem_cart_alter_cartitem_unique_together.py
    │   │   ├── 0009_alter_cartitem_quantity.py
    │   │   ├── 0010_alter_customer_options_remove_customer_email_and_more.py
    │   │   ├── 0011_alter_order_options_alter_customer_birth_date.py
    │   │   ├── 0012_alter_customer_options.py
    │   │   ├── 0013_alter_collection_featured_product_and_more.py
    │   │   ├── 0014_review_user_alter_productimage_image.py
    │   │   ├── 0015_remove_review_name.py
    │   │   ├── 0016_alter_product_unit_price.py
    │   │   └── __init__.py
    │   ├── signals/
    │   │   ├── __init__.py
    │   │   └── handlers.py
    │   ├── static/
    │   │   └── store/
    │   │       └── styles.css
    │   └── tests/
    │       ├── conftest.py
    │       └── test_collections.py
    └── tags/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── models.py
        ├── tests.py
        ├── views.py
        └── migrations/
            ├── 0001_initial.py
            └── __init__.py
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork this repository.
2. Create a new branch with your feature/bugfix: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Create a Pull Request.
---

## 📞 Contact

For any inquiries or support, please reach out to:

- **Email**: forkmemaybe@gmail.com
- **GitHub Issues**: [https://github.com/ForkMeMaybe/Shop-Sphere/issues]


# Django E-Commerce

A simple e-commerce web application built with Django.

## Features

- Product management
- Category management
- Product image upload
- Responsive product listing
- Product search
- Product filtering
- User authentication
- Password management
- Profile management
- Address management
- Pagination
- Automated testing

## Technologies

- Python
- Django
- SQLite
- HTML
- CSS
- Pillow
- Argon2
- Git

## Project Structure

    project/
    |---manage.py
    |---requirements.txt
    |---README.md
    |---SECURITY.md
    |---LICENSE
    |---.gitignore
    │
    |---.github/
    |---config/
    |---products/
    |---users/
    |---templates/
    |---static/

## Installation

### 1. Clone the repository

    git clone https://github.com/veltorex/django-ecommerce.git
    cd django-ecommerce

### 2. Create a virtual environment

    python -m venv venv

### 3. Activate the virtual environment

#### Windows

    venv\Scripts\activate

### 4. Install dependencies

    pip install -r requirements.txt

### 5. Run migrations

    python manage.py migrate

### 6. Create a superuser

    python manage.py createsuperuser

### 7. Run the development server

    python manage.py runserver

Open the application in your browser:

    http://127.0.0.1:8000/

## Admin Panel

After creating a superuser, you can access the Django admin panel at:

    http://127.0.0.1:8000/admin/

## Environment Variables

Create a `.env` file in the project root:

    SECRET_KEY=your-secret-key
    DEBUG=True

Do not commit your `.env` file to the repository.


## Future Improvements

- User favorites
- Shopping cart
- Order management
- Add product reviews and ratings
- Add order status tracking
- Add email notifications
- Improve product recommendations
- Add advanced filtering
- Improve UI/UX
- Deploy the application

## Testing

Run the Django test suite with:

    python manage.py test

## Development

This project is built for learning and development purposes.

The main goal is to practice Django concepts such as:

- Models
- QuerySets
- Forms
- File uploads
- Authentication
- Password management
- Sessions
- User profiles
- Address management
- Database relationships
- Django Admin
- Password hashing
- Testing

## Contributing

Contributions, issues, and feature requests are welcome.

### Steps

1. Fork the repository.
2. Create a new branch.

    git checkout -b feature/new-feature

3. Make your changes.
4. Commit your changes.

    git add .
    git commit -m "add new feature"

5. Push the branch.

    git push origin feature/new-feature

6. Open a Pull Request.

## License

This project is licensed under the MIT License.

See the LICENSE file for more information.
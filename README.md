# Django E-Commerce Project

A full-stack e-commerce web application built using Django, Django REST Framework, MySQL, HTML, CSS, and JavaScript.

## Features

- User registration and login
- User profile management
- Change password
- Product listing
- Product detail pages
- Shopping cart
- Increase/decrease cart quantity
- Remove items from cart
- Clear cart
- Checkout
- Payment processing
- Order history
- Order cancellation
- Product reviews
- Wishlist
- Django Admin
- REST API for product management
- Token-based API authentication
- API testing with Postman

## Technologies Used

- Python
- Django
- Django REST Framework
- MySQL
- SQL
- HTML
- CSS
- JavaScript
- Git
- GitHub
- Postman

## REST API

### Product APIs

| Method | Endpoint | Authentication |
|---|---|---|
| GET | `/api/products/` | Public |
| POST | `/api/products/` | Token required |
| GET | `/api/products/<id>/` | Public |
| PUT | `/api/products/<id>/` | Token required |
| PATCH | `/api/products/<id>/` | Token required |
| DELETE | `/api/products/<id>/` | Token required |

## Authentication

The API uses Django REST Framework Token Authentication.

Authenticated requests use:

```text
Authorization: Token <your-token>
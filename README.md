# Django E-Commerce Web Application

Welcome to the Django E-Commerce Web Application or Velocity Cart! This project allows users to create accounts, shop for products, leave comments, and more.

## Features

1. **User Authentication:**
   - Users can sign up using their email.
   - After submitting the form, a random OTP will be sent to the user's email for verification.
   - Users can change their account password by submitting their account email.
   - Password change requires email verification through a one-time-use link.

2. **Product Management:**
   - Users can view and search for products.
   - Web site owner can set a home page poster or banner image.
   - Application automatically manages and updates the home page image.
   - Product with multipale images.

3. **Shopping Cart:**
   - Users can add and remove products from their shopping cart.
   - Users can place orders after adding products to the cart or user can directly place order without adding product to the cart.

4. **Product Ratings and Comments:**
   - Users can rate products after placing an order (one-time use link).
   - Users can comment on products and reply to each comment seprately.

## Application on Internet
https://velocitycart.pythonanywhere.com/

## Installation

To run the project locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/your-username/your-repo.git

# Navigate to the project directory
cd your-repo

# Install dependencies
pip install -r requirements.txt

# Perform migrations
python manage.py migrate

# Run the development server
python manage.py runserver


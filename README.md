# 🍕 FoodCart - Food Delivery Web Application

A complete, production-ready food delivery web application built entirely with **Python and Django**. This is a full-stack implementation featuring user authentication, restaurant management, menu ordering, and order tracking.

## 📋 Features

### 👥 User Authentication & Roles
- **Customer Registration & Login**: Users can create accounts as customers
- **Restaurant Owner Accounts**: Separate registration for restaurant owners
- **User Profiles**: Extended profile with addresses, phone numbers, and preferences
- **Multiple Delivery Addresses**: Customers can save and manage delivery addresses
- **Secure Password Management**: Uses Django's built-in authentication system

### 🍽️ Restaurant Management
- **Restaurant Registration**: Owners can register and manage their restaurants
- **Restaurant Dashboard**: Complete management interface for owners
- **Restaurant Verification**: Admin verification system
- **Opening/Closing Hours**: Define restaurant operating hours
- **Restaurant Ratings & Reviews**: Customer reviews and ratings

### 📱 Menu Management
- **Food Categories**: Organize menu items by categories (Chinese, Italian, etc.)
- **Menu Items**: Add/edit/delete menu items with details
- **Item Pricing**: Dynamic pricing for all menu items
- **Item Availability**: Mark items as available or out of stock
- **Vegetarian/Non-Vegetarian**: Item type indicators
- **Item Images**: Upload and display item images
- **Preparation Time**: Show estimated preparation time for each item

### 🛒 Shopping Cart & Orders
- **Dynamic Shopping Cart**: Add/remove items with quantity management
- **Single Restaurant Ordering**: Users can only order from one restaurant per cart
- **Cart Persistence**: Cart data persists across sessions
- **Multiple Payment Methods**: Cash on Delivery, Card, Wallet (simulated)
- **Delivery Tracking**: Real-time order status updates
- **Order History**: Complete order history for customers
- **Order Details**: Detailed view of each order with items and pricing

### 📦 Order Management
- **Order Statuses**: Placed → Confirmed → Preparing → Ready → Out for Delivery → Delivered
- **Order Numbering**: Unique order numbers for tracking
- **Estimated Delivery**: Show estimated delivery time
- **Price Breakdown**: Subtotal, delivery fee, discount, and total
- **Restaurant Order View**: Owners can see and manage orders

### ⭐ Reviews & Ratings
- **Customer Reviews**: Rate and review delivered orders
- **Restaurant Ratings**: Aggregate ratings from customer reviews
- **Review Management**: Edit or view submitted reviews

### 🔐 Admin Features
- **Django Admin Interface**: Full admin control over all entities
- **User Management**: Manage users and their roles
- **Restaurant Verification**: Approve/reject restaurant registrations
- **Order Management**: View and manage all orders
- **Analytics**: Built-in Django admin statistics

## 🛠️ Tech Stack

- **Backend**: Python 3.8+
- **Web Framework**: Django 4.2.7
- **Database**: SQLite (default, easily switchable to PostgreSQL/MySQL)
- **Frontend**: Django Templates (HTML + CSS)
- **Styling**: Bootstrap 5.3
- **Image Handling**: Pillow 10.1.0

## 📁 Project Structure

```
foodcart/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── db.sqlite3                        # SQLite database (auto-created)
│
├── foodcart/                         # Main project folder
│   ├── __init__.py
│   ├── settings.py                   # Django configuration
│   ├── urls.py                       # Main URL routing
│   ├── views.py                      # Main views (home page)
│   ├── asgi.py                       # ASGI config
│   └── wsgi.py                       # WSGI config
│
├── accounts/                          # User authentication app
│   ├── migrations/
│   ├── templates/accounts/            # Account templates
│   │   ├── signup.html
│   │   ├── login.html
│   │   ├── profile.html
│   │   ├── add_address.html
│   │   └── edit_address.html
│   ├── models.py                      # UserProfile, Address models
│   ├── views.py                       # Auth views
│   ├── forms.py                       # Auth forms
│   ├── urls.py                        # Auth URLs
│   ├── admin.py                       # Admin configuration
│   └── apps.py                        # App config
│
├── restaurants/                       # Restaurant management app
│   ├── migrations/
│   ├── templates/restaurants/         # Restaurant templates
│   │   ├── list.html                 # Browse restaurants
│   │   ├── detail.html               # Restaurant menu
│   │   ├── register.html             # Register restaurant
│   │   ├── owner_dashboard.html      # Owner dashboard
│   │   ├── edit_restaurant.html
│   │   ├── add_item.html
│   │   ├── edit_item.html
│   │   └── add_category.html
│   ├── models.py                      # Restaurant, MenuItem, Category models
│   ├── views.py                       # Restaurant views
│   ├── forms.py                       # Restaurant forms
│   ├── urls.py                        # Restaurant URLs
│   ├── admin.py                       # Admin configuration
│   └── apps.py                        # App config
│
├── orders/                            # Order management app
│   ├── migrations/
│   ├── templates/orders/              # Order templates
│   │   ├── cart.html                 # Shopping cart
│   │   ├── checkout.html             # Checkout page
│   │   ├── order_detail.html         # Order details
│   │   ├── order_history.html        # Order history
│   │   └── review.html               # Review form
│   ├── models.py                      # Cart, Order, OrderItem models
│   ├── views.py                       # Order views
│   ├── forms.py                       # Order forms
│   ├── urls.py                        # Order URLs
│   ├── admin.py                       # Admin configuration
│   └── apps.py                        # App config
│
├── templates/                         # Shared templates
│   ├── base.html                     # Base template (navigation, footer)
│   ├── home.html                     # Home page
│   └── 404.html                      # Error pages
│
├── static/                            # Static files
│   ├── css/
│   │   └── style.css                 # Main stylesheet
│   └── js/
│       └── main.js                   # Main JavaScript
│
└── media/                            # User uploads (images)
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone or Download Project
```bash
cd d:\Projects\foodcart
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Create Database & Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 7: Collect Static Files (Production)
```bash
python manage.py collectstatic --noinput
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## 📖 How to Use

### For Customers
1. **Sign Up**: Create a customer account at `/accounts/signup/`
2. **Browse Restaurants**: Visit home page or `/restaurants/`
3. **View Menu**: Click on a restaurant to see its menu
4. **Add to Cart**: Add items from the menu
5. **Checkout**: Proceed to `/orders/checkout/`
6. **Place Order**: Provide delivery address and payment method
7. **Track Order**: View order status in order history
8. **Review**: Rate restaurants after delivery

### For Restaurant Owners
1. **Sign Up**: Create account as "Restaurant Owner"
2. **Register Restaurant**: Go to `/restaurants/register/`
3. **Add Menu**: Add food categories and menu items from dashboard
4. **Manage Orders**: View incoming orders and update status
5. **View Dashboard**: `/restaurants/dashboard/` shows all orders and metrics

### For Admin
1. **Access Admin Panel**: Go to `/admin/`
2. **Login**: Use superuser credentials
3. **Manage Users**: Verify users and manage roles
4. **Verify Restaurants**: Approve restaurant registrations
5. **Monitor Orders**: View all orders in the system
6. **Analytics**: Check built-in statistics and reports

## 📝 API Endpoints

### Authentication
- `GET /accounts/signup/` - Signup page
- `POST /accounts/signup/` - Create account
- `GET /accounts/login/` - Login page
- `POST /accounts/login/` - Authenticate user
- `GET /accounts/logout/` - Logout

### Restaurants
- `GET /restaurants/` - List all restaurants
- `GET /restaurants/<id>/` - Restaurant detail & menu
- `GET /restaurants/register/` - Register restaurant form
- `POST /restaurants/register/` - Create new restaurant
- `GET /restaurants/dashboard/` - Restaurant owner dashboard

### Menu Management
- `GET /restaurants/menu/add/` - Add menu item form
- `POST /restaurants/menu/add/` - Create menu item
- `GET /restaurants/menu/<id>/edit/` - Edit menu item form
- `POST /restaurants/menu/<id>/edit/` - Update menu item
- `POST /restaurants/menu/<id>/delete/` - Delete menu item

### Cart & Orders
- `GET /orders/cart/` - View shopping cart
- `POST /orders/cart/add/` - Add item to cart (AJAX)
- `GET /orders/checkout/` - Checkout page
- `POST /orders/checkout/` - Place order
- `GET /orders/<id>/` - Order details
- `GET /orders/` - Order history
- `GET /orders/<id>/review/` - Review order form
- `POST /orders/<id>/review/` - Submit review

### User Profile
- `GET /accounts/profile/` - User profile
- `POST /accounts/profile/` - Update profile
- `GET /accounts/address/add/` - Add address form
- `POST /accounts/address/add/` - Create address
- `GET /accounts/address/<id>/edit/` - Edit address form
- `POST /accounts/address/<id>/delete/` - Delete address

## 🎨 Customization

### Change Brand Colors
Edit `/static/css/style.css`:
```css
:root {
    --primary-color: #ff5e1f;  /* Change this to your brand color */
    --dark-color: #1c1c1c;
    --light-color: #f5f5f5;
}
```

### Configure Email
Edit `swiggy_clone/settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

### Use PostgreSQL (Instead of SQLite)
Edit `swiggy_clone/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'foodcart',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🔒 Security Features

- **CSRF Protection**: Built-in CSRF token validation
- **Password Hashing**: Django's secure password hashing
- **SQL Injection Prevention**: Django ORM protection
- **XSS Protection**: Template auto-escaping
- **Authentication Required**: Login decorators on sensitive views
- **Authorization Checks**: Role-based access control

## 📊 Database Models

### accounts.UserProfile
- Extended user information
- Role assignment (Customer, Restaurant Owner, Delivery Partner)
- Phone number, address, profile picture

### accounts.Address
- Multiple delivery addresses per customer
- Address type (Home, Work, Other)
- Default address selection

### restaurants.Restaurant
- Restaurant information and details
- Owner (OneToOne with User)
- Rating and review count
- Operating hours

### restaurants.Category
- Food categories (Chinese, Italian, etc.)
- Related to specific restaurant

### restaurants.MenuItem
- Individual menu items/dishes
- Pricing, availability, preparation time
- Related to restaurant and category

### orders.Cart
- Shopping cart for logged-in users
- OneToOne with User

### orders.CartItem
- Individual items in cart
- Quantity management
- Related to cart and menu item

### orders.Order
- Complete order information
- Order tracking and status
- Payment and delivery details

### orders.OrderItem
- Items within an order
- Price snapshot at time of order

### orders.Review
- Customer reviews for orders
- Ratings and comments
- Related to order, user, and restaurant

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Migration Issues
```bash
python manage.py migrate --run-syncdb
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### Database Reset (Development Only)
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Models](https://docs.djangoproject.com/en/4.2/topics/db/models/)
- [Django Templates](https://docs.djangoproject.com/en/4.2/topics/templates/)
- [Django Forms](https://docs.djangoproject.com/en/4.2/topics/forms/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

## 📝 Code Conventions

- **Models**: Use descriptive names and add docstrings
- **Views**: Use class-based views where appropriate
- **Forms**: Create custom forms for validation
- **Templates**: Keep templates DRY (Don't Repeat Yourself)
- **CSS**: Use utility classes and custom styles
- **Comments**: Add comments for complex logic

## 🚀 Deployment

### For Production:
1. Set `DEBUG = False` in settings.py
2. Update `ALLOWED_HOSTS` with your domain
3. Use a production database (PostgreSQL recommended)
4. Set up proper email backend
5. Use a production WSGI server (Gunicorn, uWSGI)
6. Use a reverse proxy (Nginx)
7. Enable HTTPS with SSL certificate

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn foodcart.wsgi:application --bind 0.0.0.0:8000
```

## 📄 License

This project is open source and available for educational purposes.

## 👨‍💻 Author

Created as a complete Django learning project demonstrating best practices in web development.

## ⭐ Features Completed

- ✅ User authentication (signup, login, logout)
- ✅ User roles (customer, restaurant owner, delivery partner)
- ✅ Restaurant registration and management
- ✅ Menu management (add/edit/delete items)
- ✅ Food categories
- ✅ Restaurant browsing
- ✅ Menu viewing
- ✅ Shopping cart
- ✅ Order placement
- ✅ Order status tracking
- ✅ Payment simulation
- ✅ Order history
- ✅ Reviews and ratings
- ✅ User profile management
- ✅ Multiple delivery addresses
- ✅ Django admin interface
- ✅ Responsive design
- ✅ Search and filtering

## 🎯 Future Enhancements

- Real payment gateway integration (Stripe, PayPal)
- Delivery partner tracking with real-time location
- Advanced search and filtering
- Coupon and discount system
- Real-time notifications (WebSockets)
- Mobile app (React Native/Flutter)
- Analytics dashboard
- Multi-language support
- Wallet system
- Referral program

---

**Happy Coding! 🚀**

For questions or issues, please refer to the Django documentation or create issues in your repository.

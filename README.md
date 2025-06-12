# Human Resource Management system

This README provides instructions for setting up the project locally using Docker Compose, and also offers a way to access a live demo if you prefer not to set up.

## 🚀 Live Demo (No Local Setup Required)

If you just want to explore the API without setting up your local environment, you can access it here:

[**Click here to visit the live API!**](https://hr-system-management-app.onrender.com/swagger/)

You can use the following **superuser credentials** to log in and explore the API

* **Username:** `super.hr`
* **Password:** `password1`

---

## 💻 Local Setup (For Development)

Follow these steps to get the project running on your local machine using Docker Compose.

### Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Git**: For cloning the repository.
    * [Download Git](https://git-scm.com/downloads)
* **Docker Desktop**: Includes Docker Engine and Docker Compose.
    * [Download Docker Desktop](https://www.docker.com/products/docker-desktop)

### 1. Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/Faithaigo/hr-system-capstone.git
cd hr-capstone-system
```

### 2. Create Environment Variables

Create a ``.env`` file in the root of the project directory (where ``compose.yml`` is located). This stores sensitive information and configurations.
Open the ``.env`` file and add the following minimal required variables. 

```bash
DJANGO_SECRET_KEY=your_generated_secret_key
DEBUG=TRUE
DJANGO_ALLOWED_HOSTS=localhost,0.0.0.0
DJANGO_LOGLEVEL=info
DATABASE_ENGINE=postgresql
DATABASE_NAME=yourdb
DATABASE_USERNAME=youruser
DATABASE_PASSWORD=yourpassword
DATABASE_HOST=db #Service name in compose.yml
DATABASE_PORT=5432
```

### 3. Build and Run the Containers

Navigate to the root of the project where ``compose.yml`` is located and run:

```bash
docker compose up --build -d
```

### 4. Create a Superuser
You'll need to create a superuser to access the API endpoints:

```bash
docker compose run --rm django-web python manage.py createsuperuser
```

Follow the prompts to set up your username, email, and password.

### 5. Access the Application

The application should now be running and accessible at:

[http://localhost:8000](http://localhost:8000)

You can access the Django Admin panel at:

[http://localhost:8000/admin/](http://localhost:8000/admin/)

### 6. Access API Documentation

Once the application is running, you can access the interactive API documentation (powered by Swagger UI) at:

[http://localhost:8000/swagger/](http://localhost:8000/swagger/)

### 7. Run Tests

To run the tests:

```bash
docker compose run --rm django-web python manage.py test
```

### 8. Stopping the Project

To stop all running containers without removing their data:

```bash
docker compose stop
```



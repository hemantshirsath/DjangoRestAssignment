### Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Endpoints](#endpoints)
    - [1. Retrieve Token](#1-retrieve-token)
    - [2. Retrieve User Information](#2-retrieve-user-information)
    - [3. List and Create Works](#3-list-and-create-works)
    - [4. List and Create Artists](#4-list-and-create-artists)
    - [5. Register a New User](#5-register-a-new-user)

## Getting Started

### Prerequisites

- Python 3.x
- Django
- Django REST Framework
- Other dependencies...

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   ```

2. Change into the project directory:

   ```bash
   cd yourproject
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Run migrations:

   ```bash
   python manage.py migrate
   ```

7. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:

   ```bash
   python manage.py runserver
   ```

The project should now be accessible at http://127.0.0.1:8000/.

## API Documentation

### Authentication

All API endpoints require token-based authentication. Retrieve a token by following the [Retrieve Token](#1-retrieve-token) endpoint.

### Endpoints

#### 1. Retrieve Token

- **Endpoint:** `/api/token/`
- **Method:** POST
- **Description:** Retrieve a token by providing valid username and password.
- **Request Body:**
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response:**
  ```json
  {
    "token": "your_access_token",
    "user_id": 1,
    "username": "your_username"
  }
  ```

#### 2. Retrieve User Information

- **Endpoint:** `/api/token/`
- **Method:** GET
- **Description:** Retrieve information about the currently authenticated user.
- **Authentication:** Token-based authentication required.
- **Response:**
  ```json
  {
    "user_id": 1,
    "username": "your_username"
  }
  ```

#### 3. List and Create Works

- **Endpoint:** `/api/works/`
- **Method:** GET, POST
- **Description:** List all works or create a new work.
- **Authentication:** Token-based authentication required for creating works.
- **Parameters:**
  - `work_type`: Filter works by type (optional).
  - `artist`: Search works by artist name (optional).
- **Response (GET):**
  ```json
  [
    {
      "link": "https://example.com",
      "work_type": "YouTube"
    },
    ...
  ]
  ```
- **Request Body (POST):**
  ```json
  {
    "link": "https://example.com",
    "work_type": "YouTube"
  }
  ```
- **Response (POST):**
  ```json
  {
    "link": "https://example.com",
    "work_type": "YouTube"
  }
  ```

#### 4. List and Create Artists

- **Endpoint:** `/api/artists/`
- **Method:** GET, POST
- **Description:** List all artists or create a new artist.
- **Authentication:** Token-based authentication required for creating artists.
- **Response (GET):**
  ```json
  [
    {
      "id": 1,
      "name": "Artist Name",
      "user": "username",
      "works": [...]
    },
    ...
  ]
  ```
- **Request Body (POST):**
  ```json
  {
    "name": "Artist Name"
  }
  ```
- **Response (POST):**
  ```json
  {
    "id": 1,
    "name": "Artist Name",
    "user": "username",
    "works": []
  }
  ```

#### 5. Register a New User

- **Endpoint:** `/api/register/`
- **Method:** POST
- **Description:** Register a new user.
- **Request Body:**
  ```json
  {
    "username": "new_user",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "token": "your_access_token",
    "user_id": 2,
    "username": "new_user"
  }
  ```

Feel free to add more details and information specific to your project in the README and API documentation.

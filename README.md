# 🏋️ Online Fitness Studio API

This project is a simple backend API for a fitness studio where clients can view available classes and book a spot.
Built with Django REST Framework and SQLite (in-memory) for simplicity.

---
# 📌 Features

- View all upcoming fitness classes (Yoga, Zumba, HIIT, etc.)

- Book a spot in a class (with slot validation)

- Retrieve all bookings for a specific client by email

- Error handling for overbooking & invalid requests

- Input validation & clean modular code

---
# ⚙️ Setup Instructions

## 1️⃣ Clone the Repository
- `git clone https://github.com/mdshahabaz/Fitness-Studio-Booking-API.git`
- `cd fitness_app`

## 2️⃣ Create a Virtual Environment
- `python -m venv venv` Create virtual environment
- `venv\Scripts\activate` Activate Virtual environment for Windows
- `source venv/bin/activate` Activate Virtual environment for macOS/Linux

---
## 3️⃣ Install Dependencies
- `pip install --upgrade pip `
- `pip install -r requirements.txt`

---
## 4️⃣ Apply Migrations
- `python manage.py makemigrations`
- `python manage.py migrate` This will apply migrations

## 5️⃣ Seed Sample Data
- `python manage.py seed_data` This will initally seed data

This command will:

- Create instructors

- Create fitness classes (Yoga, Zumba, HIIT)

- Create clients

- Create bookings for clients

- Automatically decrement available slots for booked classes

---
## 6️⃣ Run the Development Server
- `python manage.py runserver` This starts the server
- The server is available at `http://127.0.0.1:8000/`

## 🔹 API Endpoints
- ## API Endpoints

| Method | Endpoint       | Description |
|--------|----------------|------------|
| GET    | /classes/get-all-classes/      | List all upcoming fitness classes |
| POST   | /classes/create-class/      | Create a new fitness class |
| GET    | /bookings/get-all-bookings/     | List all bookings for a client (`?email_address=<email>`) |
| POST   | /bookings/create-booking/         | Create a booking for a client |
| POST   | /instructors/create-instructor/  | Add a new instructor |

- ### Detailed Endpoint Examples
**Description:** Fetch all upcoming fitness classes.  

**Request:**  
- `GET /classes/get-all-classes/`
  - cURL `curl -X GET http://127.0.0.1:8000/classes/get-all-classes/`
  - Success Response (200 OK):

    ```{
        "message": "Fetched all upcoming classes successfully!",
        "status": true,
        "data": [
            {
                "id": 1,
                "class_name": "YOGA",
                "instructor": {
                    "id": 1,
                    "instructor_name": "John Doe"
                },
                "available_slots": 10,
                "scheduled_at": "2025-09-01T07:00:00+05:30"
            }
        ]
    }
  - Error Response(400 Bad Request):
       ```{
    "message": "No classes found.",
    "status": false,
    "data": []
    }
- `POST /classes/create-class/` Description: Create a new fitness class.
  
    - cURL:
      ```
      curl -X POST http://127.0.0.1:8000/classes/create-class/ \
      -H "Content-Type: application/json" \
      -d '{
          "class_name": "ZUMBA",
          "instructor_id": 2,
          "available_slots": 15,
          "scheduled_at": "2025-08-30T10:30:00Z"
      }

    - Request Body:
        ```
        {
        "class_name": "ZUMBA",
        "instructor_id": 2,
        "available_slots": 15,
        "scheduled_at": "2025-08-30T10:30:00Z"
      }
    - Success Response (201 Created):
       ```
         {
          "message": "Fitness class created successfully!",
          "status": true,
          "data": {
              "id": 2,
              "class_name": "ZUMBA",
              "instructor": {
                  "id": 2,
                  "instructor_name": "Jane Smith"
              },
              "available_slots": 15,
              "scheduled_at": "2025-08-30T10:30:00+00:00"
            }
       }
    - Error Response (400 Bad request):
        ```
         {
          "message": "Invalid data",
          "status": false,
          "errors": {
              "class_name": ["This field is required."],
              "scheduled_at": ["Invalid datetime format."]
          },
          "data": []
      }
- `GET /bookings/get-all-bookings/?email=email@email.com/` Description: Fetch all bookings for a client using email_address query param.
    - cURL `curl -X GET "http://127.0.0.1:8000/bookings/get-all-bookings/?email_address=anne.gold@gmail.com"`
    - Request Body:
        ```
          GET /bookings/get-all-bookings/?email_address=anne.gold@gmail.com
    - Success Response(200 OK):
        ```
        {
          "message": "Success",
          "status": true,
          "data": [
              {
                  "id": 1,
                  "client": {
                      "first_name": "Anne",
                      "last_name": "Gold",
                      "email_address": "anne.gold@gmail.com",
                      "phone_number": "7777777777"
                  },
                  "fitness_class": {
                      "id": 2,
                      "class_name": "ZUMBA"
                  },
                  "booked_at": "2025-08-20T12:00:00+05:30"
              }
          ]
        }
    - Error Response(400 Bad Request):
       ```
       {
          "message": "No booking exists with email: anne.gold@gmail.com",
          "status": false,
          "data": []
      }
- `POST /bookings/create-booking/` Description: Create a booking for a client.

   - cURL:
      ```
      curl -X POST http://127.0.0.1:8000/bookings/create-booking/ \
      -H "Content-Type: application/json" \
      -d '{
          "class_id": 2,
          "first_name": "Anne",
          "last_name": "Gold",
          "email_address": "anne.gold@gmail.com"
      }'
   - Request Body:
      ```
      {
        "class_id": 2,
        "first_name": "Anne",
        "last_name": "Gold",
        "email_address": "anne.gold@gmail.com"
     }
   - Success Response (201 Created):
      ```
      {
          "message": "Booking created successfully.",
          "status": true,
          "data": {
              "id": 1,
              "client": {
                  "first_name": "Anne",
                  "last_name": "Gold",
                  "email_address": "anne.gold@gmail.com",
                  "phone_number": null
              },
              "fitness_class": {
                  "id": 2,
                  "class_name": "ZUMBA"
              },
              "booked_at": "2025-08-20T12:00:00+05:30"
          }
      }
    - Error Response (400 Bad Request):
       ```
       {
          "message": "Booking failed. Class might be full or invalid data provided.",
          "status": false,
          "errors": {
              "class_id": ["Invalid class ID or no slots available."]
          },
          "data": []
      }
- `POST /instructors/create-instructor/` Description: Create a new instructor.

    - cURL:
        ```
        curl -X POST http://127.0.0.1:8000/instructors/create-instructor/ \
      -H "Content-Type: application/json" \
      -d '{
          "instructor_name": "Michael Johnson"
      }'
    - Request Body:
       ```
       {
          "instructor_name": "Michael Johnson"
      }
    - Success Response (201 Created):
       ```
       {
          "message": "Instructor created successfully",
          "status": true,
          "data": {
              "id": 3,
              "instructor_name": "Michael Johnson"
          }
      }
    - Error Response (400 Bad Request):
        ```
        {
          "message": "Instructor name is required",
          "status": false,
          "data": []
      }


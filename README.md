
# Meeting Room Booking System (Microservices)

A Meeting Room Booking System built using **FastAPI microservices architecture**.
This system allows users to **book meeting rooms, manage rooms, and receive booking notifications**.

The application uses **Docker, PostgreSQL, MongoDB, Kafka, and JWT authentication**.


## Project Architecture
The project is divided into multiple microservices:


| Service        | Port      |       Description    |
| -------------   | ------------ |--------------|
| `user-service`        | 8001 | Handles user registration and authentication
| `room-service`        | 8002 | Manages meeting rooms
| `booking-service`     | 8003 | Handles room booking logic
| `notification-service`|8004  | Sends booking notifications and email.


## Tech Stack
Backend
- FastAPI
- Python

Databases
- PostgreSQL (Users, Rooms, Bookings)
- MongoDB (Notifications)

Messaging
- Apache Kafka

Authentication
- JWT (JSON Web Token)

Containerization
- Docker
- Docker Compose

## Features

User Features
- User registration
- User login
- JWT authentication

Room Features
- Admin can create rooms
- List available rooms
- Manage room capacity

Booking Features
- Book meeting rooms
- Prevent double booking
- View booking details

Notification Features
- Booking confirmation notifications
- Kafka-based event messaging
- Notifications stored in MongoDB

## Project Structure

```
bt-meeting-room/
│
├── user-service/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── room-service/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── booking-service/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── notification-service/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
|
├── venv/
|
├── requirements.txt
├── .env
├── docker-compose.yml
└── README.md
```
## System Workflow
  1. User registers or logs in using **user-service**
  2. User receives **JWT token**
  3. Admin creates meeting rooms using **room-service**
  4. User books a room using **booking-service**
  5. Booking event is sent to **Kafka**
  6. **notification-service** consumes the event
  7. Notification is stored in **MongoDB**
  8. Real Time Meeting Room Booking shows.
   
  ## API Documentation
Swagger documentation is available for each service:


| Service        | Port      |   
| -------------   | ------------ |
| User Service        | http://localhost:8001/docs 
| Room Service        | http://localhost:8002/docs 
| Booking Service     | http://localhost:8003/docs 
| Notification Service|http://localhost:8004/docs  

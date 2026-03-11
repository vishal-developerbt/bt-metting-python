
# Meeting Room Booking System (Microservices)

A Meeting Room Booking System built using **FastAPI microservices architecture**.
This system allows users to **register, login, view available meeting rooms, book rooms, and receive real-time notifications.**.

The application is designed using **scalable microservices** with **Kafka messaging, Docker containerization, and an API Gateway**.

## System Architecture

This project follows a **Microservices Architecture** where each service runs independently and communicates via **REST APIs and Kafka events**.

Client → API Gateway → Microservices → Databases

Services communicate through:
- REST APIs
- Kafka Event Streaming
- WebSocket Notifications

## Service Overview


| Service        | Port      |       Description    |
| -------------   | ------------ |--------------|
| `api-gateway`         | 8000 | Nginx gateway routing requests to microservices
| `user-service`        | 8001 | Handles user registration and authentication
| `room-service`        | 8002 | Manages meeting rooms
| `booking-service`     | 8003 | Handles room booking logic
| `notification-service`|8004  | Sends booking notifications and email.


## API Gateway

The system uses **Nginx as an API Gateway** to route all client requests to the appropriate microservice.

Instead of calling services directly:

    http://localhost:8001
    http://localhost:8002
    http://localhost:8003

Clients call the gateway:

    http://localhost:8080/users
    http://localhost:8080/rooms
    http://localhost:8080/bookings

Gateway Responsibilities:
- Request routing
- Microservice abstraction
- Centralized entry point
- Future load balancing support



## Tech Stack
Backend
- FastAPI
- Python

Databases
- PostgreSQL (Users, Rooms, Bookings)
- MongoDB (Notifications)

Messaging
- Apache Kafka
- Zookeeper

Authentication
- JWT (JSON Web Token)

Real-Time Communication
- WebSockets

Containerization
- Docker
- Docker Compose

API Gateway
- Nginx

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
- Real-time updates using WebSocket

## Project Structure

```
bt-meeting-room/
│
├── api-gateway/
│   ├── ngnix.conf
│   └── Dockerfile
|
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
  8. WebSocket pushes real-time notification to users
   
  ## API Documentation
Swagger documentation is available for each service:

 ### Direct service URLs

| Service        | Port      |   
| -------------   | ------------ |
| User Service        | http://localhost:8001/docs 
| Room Service        | http://localhost:8002/docs 
| Booking Service     | http://localhost:8003/docs 
| Notification Service|http://localhost:8004/docs  

 ### Through API Gateway

| Service        | Port      |   
| -------------   | ------------ |
| User Service        | http://localhost:8080/users/docs 
| Room Service        | http://localhost:8080/rooms/docs
| Booking Service     | http://localhost:8080/bookings/docs

## Environment Variables

Example .env file:

    DATABASE_URL=postgresql://postgres:password@postgres:5432/meetingdb
    SECRET_KEY=your-secret-key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    KAFKA_BOOTSTRAP_SERVERS=kafka:9092
    MONGO_URL=mongodb://mongo:27017

## Running the Project
### Clone the Repository
    git clone https://github.com/vishal-developerbt/bt-metting-python.git
    cd bt-metting-python

### Start All Services
    docker compose up --build

### Stop Services
    docker compose down

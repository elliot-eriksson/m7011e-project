# Project Overview: Budgeting Service

The Budgeting Service is a backend system designed to help users efficiently manage their finances. Built on a **microservices architecture**, this project provides a secure and scalable solution for budget tracking, transaction management, and user collaboration. It integrates **RabbitMQ** for asynchronous messaging and **SendGrid** for email notifications, ensuring seamless communication between services.

---

## Key Features

1. **Budget Management**:
   - Create, update, delete, and view budgets.
   - Assign roles to users (Owner, Admin, Member) with role-based permissions.

2. **Transaction Tracking**:
   - Record income and expense transactions.
   - Automatically update budgets based on transaction data.

3. **Collaboration**:
   - Share budgets with other users.
   - Invite users via email with configurable roles.

4. **Notifications**:
   - Send email invitations using **SendGrid**.

5. **Microservices Architecture**:
   - Decoupled services for handling budgets, transactions, and notifications.
   - **RabbitMQ** for asynchronous communication between services.

6. **Security**:
   - Environment-specific configurations for sensitive credentials.
   - Role-based access control to restrict unauthorized actions.
---

## Microservices Breakdown

1. **Budget Service**:
   - Manages budgets and associated permissions.
   - Role-based access to ensure secure operations.

2. **OAuth2 Service**:
   - Manages user authentication and authorization.
   - Handles user-related logic such as token validation and session management.
   - Provides secure access for users across all services.

3. **Email Service**:
   - Sends email invitations and notifications using SendGrid.
   - Handles user role invitations and budget-sharing communication.

---

## Prerequisites

1. **RabbitMQ**:
   - Either a local RabbitMQ instance or a cloud-based solution like **CloudAMQP**.
   - For CloudAMQP, visit [CloudAMQP](https://www.cloudamqp.com/) to create an instance.

2. **SendGrid**:
   - A verified SendGrid account.
   - Visit [SendGrid](https://sendgrid.com/) to create an account and generate an API key.
   - Ensure you have a verified sender email address.

3. **Docker and Docker Compose**:
   - Docker version 20.x or higher.
   - Docker Compose version 1.29 or higher.
   - Install from [docker.com](https://www.docker.com/).


## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/elliot-eriksson/m7011e-project.git
cd M7011E-project 
```
### 2. Set Up a CloudAMQP Instance
1. Visit [CloudAMQP](https://www.cloudamqp.com/) and sign up or log in.
2. Create a new RabbitMQ instance:
   - Choose a free plan (e.g., "Little Lemur") or select a suitable paid plan based on your needs.
   - Name your instance and select a region.
3. Once created, go to the **Details** page of your instance.
4. Copy the **AMQP URL** (e.g., `amqps://<username>:<password>@<host>/<vhost>`).

### 3. Set Up SendGrid
1. Visit [SendGrid](https://sendgrid.com/) and sign up or log in.
2. Navigate to the **API Keys** section:
   - Go to **Settings** > **API Keys**.
   - Click **Create API Key**.
   - Provide a name for your API key (e.g., "Budgeting Service").
   - Assign the appropriate permissions (e.g., "Full Access").
   - Click **Create & View** to generate the key.
3. Copy the generated API key.

### 4. Add the API key and the RabbitMQ URL to your `.env` file
- For the **email_service** microservice:
    - Add both the SendGrid API key and the RabbitMQ URL to the `.env` file:
    ```env
    ### RABBITMQ
    RABBITMQ_URL=amqps://your_rabbitmq_url

    ### SENDGRID
    SENDGRID_API_KEY=your_sendgrid_api_key
    SECRET_KEY=your_django_secret_key
    DEBUG=True
    DATABASE_URL=sqlite:///db.sqlite3
    SENDGRID_FROM_EMAIL = "your_sendgrid_mail"
    ```

- For all other microservices:
    - Only the RabbitMQ URL is required in the `.env` file:
    ```env
    RABBITMQ_URL=amqps://<username>:<password>@<host>/<vhost>
    ```
### 5. Run the Application
Use Docker Compose to build and run the microservices.

- To build and run the application:
```bash
docker-compose build
docker-compose up
```
- Alternatively, you can combine the commands:
```bash color
docker-compose up --build
```
This will start all the microservices, ensuring that the configurations (RabbitMQ and SendGrid) are loaded properly.

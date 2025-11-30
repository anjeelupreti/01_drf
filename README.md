# **Django REST Project - User Management & Audit System**

A comprehensive Django REST API with role-based authentication, user
management, project CRUD operations, and automatic audit logging.

## **Features**

-   **JWT Authentication**: Secure token-based authentication

-   **Role-Based Access Control**: Super Admin, Country Admin, Member
    roles

-   **User Management**: Create users with country and role restrictions

-   **Project CRUD**: Full project management with permissions

-   **Audit Logging**: Automatic tracking of all changes using Django
    Signals

-   **PostgreSQL**: Production-ready database

-   **RESTful API**: Clean, well-structured API endpoints

## **System Architecture**

### **User Roles & Permissions**

-   **Super Admin**: Full system access, can create any user for any
    country

-   **Country Admin**: Can create members only for their assigned
    country

-   **Member**: Basic access, can only manage their own projects

### **Audit Logging**

-   **Automatic Tracking**: Django signals automatically log all create,
    update, delete operations

-   **Comprehensive Data**: Tracks user, action type, timestamp, and
    changes

-   **Role-Based Access**: Users can only see audit logs they\'re
    permitted to view

## **Prerequisites**

-   Python 3.8+

-   PostgreSQL

-   pip (Python package manager)

## **Installation & Setup**

### **1. Clone and Setup Environment**

\# Clone the repository

git clone \<repository-url\>

cd drf_task

\# Create virtual environment

python -m venv venv

source venv/bin/activate \# On Windows: venv\\Scripts\\activate

\# Install dependencies

pip install -r requirements.txt

### **2. Database Setup**

\# Login to PostgreSQL

sudo -u postgres psql

\# Create database and user

CREATE DATABASE django_rest_project;

CREATE USER django_user WITH PASSWORD \'securepassword123\';

GRANT ALL PRIVILEGES ON DATABASE django_rest_project TO django_user;

\\q

### **3. Configuration**

Update core/settings.py with your database credentials:

DATABASES = {

\'default\': {

\'ENGINE\': \'django.db.backends.postgresql\',

\'NAME\': \'django_rest_project\',

\'USER\': \'django_user\',

\'PASSWORD\': \'securepassword123\',

\'HOST\': \'localhost\',

\'PORT\': \'5432\',

}

}

### **4. Run Migrations**

python manage.py makemigrations

python manage.py migrate

### **5. Create Superuser**

python manage.py createsuperuser

\# Follow prompts to create initial super admin

### **6. Start Development Server**

python manage.py runserver

The API will be available at http://localhost:8000/

## **Authentication Endpoints**

### **Login**

**POST** /users/api/auth/login/

curl -X POST http://localhost:8000/users/api/auth/login/ \\

-H \"Content-Type: application/json\" \\

-d \'{

\"email\": \"superadmin@company.com\",

\"password\": \"yourpassword\"

}\'

**Response:**

{

\"access\": \"eyJhbGciOiJIUz\...\",

\"refresh\": \"eyJhbGciOiJIUz\...\",

\"user\": {

\"id\": 1,

\"email\": \"superadmin@company.com\",

\"role\": \"super_admin\",

\"first_name\": \"Super\",

\"last_name\": \"Admin\"

}

}

### **Refresh Token**

**POST** /users/api/auth/token/refresh/

curl -X POST http://localhost:8000/users/api/auth/token/refresh/ \\

-H \"Content-Type: application/json\" \\

-d \'{

\"refresh\": \"your-refresh-token\"

}\'

## **User Management Endpoints**

### **List Users**

**GET** /users/api/auth/users/

curl -X GET http://localhost:8000/users/api/auth/users/ \\

-H \"Authorization: Bearer \<access-token\>\"

### **Create User**

**POST** /users/api/auth/users/create/

curl -X POST http://localhost:8000/users/api/auth/users/create/ \\

-H \"Authorization: Bearer \<access-token\>\" \\

-H \"Content-Type: application/json\" \\

-d \'{

\"email\": \"newuser@company.com\",

\"password\": \"Password123!\",

\"password_confirm\": \"Password123!\",

\"first_name\": \"John\",

\"last_name\": \"Doe\",

\"role\": \"member\",

\"country_id\": 1

}\'

**Role Restrictions:**

-   **Super Admin**: Can create any role (super_admin, country_admin,
    member)

-   **Country Admin**: Can only create members for their country

-   **Member**: Cannot create users

### **Get User Details**

**GET** /users/api/auth/users/{id}/

curl -X GET http://localhost:8000/users/api/auth/users/1/ \\

-H \"Authorization: Bearer \<access-token\>\"

### **List Countries**

**GET** /users/api/auth/countries/

curl -X GET http://localhost:8000/users/api/auth/countries/ \\

-H \"Authorization: Bearer \<access-token\>\"

## **Project Management Endpoints**

### **List Projects**

**GET** /projects/api/

curl -X GET http://localhost:8000/projects/api/ \\

-H \"Authorization: Bearer \<access-token\>\"

### **Create Project**

**POST** /projects/api/

curl -X POST http://localhost:8000/projects/api/ \\

-H \"Authorization: Bearer \<access-token\>\" \\

-H \"Content-Type: application/json\" \\

-d \'{

\"title\": \"New Project\",

\"description\": \"Project description\",

\"status\": \"planning\",

\"country_id\": 1

}\'

### **Get Project Details**

**GET** /projects/api/{id}/

curl -X GET http://localhost:8000/projects/api/1/ \\

-H \"Authorization: Bearer \<access-token\>\"

### **Update Project**

**PUT/PATCH** /projects/api/{id}/update/

curl -X PATCH http://localhost:8000/projects/api/1/update/ \\

-H \"Authorization: Bearer \<access-token\>\" \\

-H \"Content-Type: application/json\" \\

-d \'{

\"status\": \"in_progress\"

}\'

### **Delete Project**

**DELETE** /projects/api/{id}/delete/

curl -X DELETE http://localhost:8000/projects/api/1/delete/ \\

-H \"Authorization: Bearer \<access-token\>\"

## **Audit Log Endpoints**

### **List All Audit Logs**

**GET** /audits/api/logs/

curl -X GET http://localhost:8000/audits/api/logs/ \\

-H \"Authorization: Bearer \<access-token\>\"

**Access Control:**

-   **Super Admin**: Sees all logs

-   **Country Admin**: Sees logs from users in their country

-   **Member**: Sees only their own logs

### **My Activities**

**GET** /audits/api/logs/my_activities/

curl -X GET http://localhost:8000/audits/api/logs/my_activities/ \\

-H \"Authorization: Bearer \<access-token\>\"

### **Filter by Model**

**GET** /audits/api/logs/by_model/?model=User

curl -X GET
\"http://localhost:8000/audits/api/logs/by_model/?model=User\" \\

-H \"Authorization: Bearer \<access-token\>\"

### **Filter by Action**

**GET** /audits/api/logs/by_action/?action=create

curl -X GET
\"http://localhost:8000/audits/api/logs/by_action/?action=create\" \\

-H \"Authorization: Bearer \<access-token\>\"

## **Testing the System**

### **Complete Test Flow**

1.  **Login as Super Admin**

curl -X POST http://localhost:8000/users/api/auth/login/ \\

-H \"Content-Type: application/json\" \\

-d \'{\"email\": \"superadmin@company.com\", \"password\":
\"yourpassword\"}\'

2.  **Create a Country Admin**

curl -X POST http://localhost:8000/users/api/auth/users/create/ \\

-H \"Authorization: Bearer \<token\>\" \\

-H \"Content-Type: application/json\" \\

-d \'{

\"email\": \"countryadmin@company.com\",

\"password\": \"Admin123!\",

\"password_confirm\": \"Admin123!\",

\"first_name\": \"Country\",

\"last_name\": \"Admin\",

\"role\": \"country_admin\",

\"country_id\": 1

}\'

3.  **Create a Project**

curl -X POST http://localhost:8000/projects/api/ \\

-H \"Authorization: Bearer \<token\>\" \\

-H \"Content-Type: application/json\" \\

-d \'{

\"title\": \"Test Project\",

\"description\": \"Testing audit system\",

\"status\": \"planning\",

\"country_id\": 1

}\'

4.  **Check Audit Logs**

curl -X GET http://localhost:8000/audits/api/logs/ \\

-H \"Authorization: Bearer \<token\>\"

## **Technical Implementation**

### **Custom User Model**

-   Uses email instead of username for authentication

-   Custom UserManager for email-based user creation

-   Role-based permissions with country assignment

### **Permission Classes**

-   IsSuperAdmin: Full system access

-   IsCountryAdminOrSuperAdmin: Country-restricted access

-   CanAccessProject: Object-level project permissions

-   CanCreateProject: Project creation permissions

-   CanEditProject: Project modification permissions

### **Audit Logging with Signals**

The system uses Django signals for automatic audit logging:

**Signals Implementation:**

\# audits/signals.py

\@receiver(post_save, sender=User)

\@receiver(post_save, sender=Project)

def log_create_update(sender, instance, created, \*\*kwargs):

\# Automatically logs all create/update operations

pass

\@receiver(post_delete, sender=User)

\@receiver(post_delete, sender=Project)

def log_delete(sender, instance, \*\*kwargs):

\# Automatically logs all delete operations

pass

**AuditLog Model Fields:**

-   user: Who performed the action

-   action: create, update, delete

-   model_name: Affected model (User, Project)

-   object_id: ID of affected object

-   changes: JSON field with change details

-   timestamp: When the action occurred

### **User Attachment Pattern**

Views attach the current user to instances for audit tracking:

def perform_create(self, serializer):

instance = serializer.save()

instance.\_audit_user = self.request.user \# For audit logging

## **Project Structure**

drf_task/

├── core/ \# Project settings

├── users/ \# Authentication & user management

│ ├── models.py \# Custom User and Country models

│ ├── views.py \# User management views

│ ├── serializers.py \# User serializers

│ └── permissions.py \# Role-based permissions

├── projects/ \# Project CRUD operations

│ ├── models.py \# Project model

│ ├── views.py \# Project views

│ └── serializers.py \# Project serializers

├── audits/ \# Audit logging system

│ ├── models.py \# AuditLog model

│ ├── signals.py \# Signal handlers

│ ├── views.py \# Audit log API

│ └── serializers.py \# Audit log serializers

└── manage.py

## **Troubleshooting**

### **Common Issues**

1.  **Database Connection Error**

    -   Verify PostgreSQL is running

    -   Check database credentials in settings.py

2.  **Authentication Failed**

    -   Ensure user exists and is active

    -   Check email/password combination

3.  **Permission Denied**

    -   Verify user has appropriate role for the operation

    -   Check country restrictions for Country Admins

4.  **Audit Logs Not Created**

    -   Verify signals are connected in audits/apps.py

    -   Check that \_audit_user is attached in views

### **Debug Commands**

\# Check system health

python manage.py check

\# Test specific app

python manage.py test users

python manage.py test projects

python manage.py test audits

\# View all URLs

python manage.py show_urls

## **API Response Examples**

### **Successful User Creation**

{

\"id\": 2,

\"email\": \"newuser@company.com\",

\"first_name\": \"John\",

\"last_name\": \"Doe\",

\"role\": \"member\",

\"country\": {

\"id\": 1,

\"name\": \"United States\",

\"code\": \"US\"

}

}

### **Audit Log Entry**

{

\"id\": 1,

\"action\": \"create\",

\"user\": 1,

\"user_email\": \"superadmin@company.com\",

\"user_role\": \"super_admin\",

\"model_name\": \"User\",

\"object_id\": 2,

\"object_repr\": \"newuser@company.com (Member)\",

\"changes\": {

\"action\": \"create\",

\"note\": \"User was created\"

},

\"timestamp\": \"2024-01-15T10:30:00Z\"

}

## **Success Indicators**

The system is working correctly when:

-   Users can login and receive JWT tokens

-   Role-based permissions restrict access appropriately

-   User creation follows role and country rules

-   Projects can be created, updated, and deleted

-   Audit logs are automatically created for all operations

-   Audit API returns filtered logs based on user role

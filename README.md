# Medhashaala School ERP System

A comprehensive school management system with Django backend and React frontend.

## Project Overview

Medhashaala is a full-featured School Enterprise Resource Planning (ERP) system designed to streamline educational institution management. The system provides a robust platform for managing students, teachers, classes, attendance, and academic performance.

### Key Components

- **Django REST API Backend**: Provides secure, scalable API endpoints for all system operations
- **PostgreSQL Database**: Stores all system data with relational integrity
- **React Frontend**: Delivers a responsive, modern user interface
- **Token-based Authentication**: Ensures secure access to system resources

### Target Users

- **School Administrators**: For managing the entire school operations
- **Teachers**: For tracking student attendance, recording grades, and managing classes
- **Students**: For accessing their academic information and performance
- **Parents**: For monitoring their children's progress and attendance

## Project Structure

- `back-end/`: Django REST API backend
- `front-end/`: React frontend application

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd back-end
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
   - You'll be prompted to enter an email, first name, last name, and password
   - This user will have admin privileges

6. Start the development server:
   ```
   python manage.py runserver
   ```
   - The server will start at http://localhost:8000/
   - Admin interface is available at http://localhost:8000/admin/

7. Load dummy data (optional but recommended for testing):
   ```
   python create_dummy_data.py
   ```
   - This will create sample students, teachers, classes, and attendance records
   - It's useful for testing the API endpoints and frontend functionality

8. Test API endpoints:
   ```
   python test_api.py
   ```
   - This script tests all API endpoints and verifies authentication
   - Make sure the server is running before executing this script

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd front-end
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

## API Authentication

The API uses token-based authentication. To authenticate:

1. Obtain a token by sending a POST request to `/api-token-auth/` with your email and password:
   ```
   curl -X POST http://localhost:8000/api-token-auth/ \
     -H "Content-Type: application/json" \
     -d '{"email": "your.email@example.com", "password": "your_password"}'
   ```

2. The response will include a token:
   ```json
   {
     "token": "your_auth_token_here",
     "user_id": 1,
     "email": "your.email@example.com"
   }
   ```

3. Include the token in the Authorization header of subsequent requests:
   ```
   Authorization: Token your_auth_token_here
   ```

4. You can also use the test_api.py script to verify authentication works correctly.

## Testing API Connection

You can test the API connection using the provided test utilities:

### Backend API Testing

Use the provided Python script to test all API endpoints:
```
cd back-end
python test_api.py
```

### Frontend API Testing

To test the connection from the frontend:
1. Open your browser console
2. Import and run the test function:
   ```javascript
   import testApiConnection from './src/api/apiTest';
   testApiConnection();
   ```

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Verify PostgreSQL is running: `pg_isready`
   - Check database credentials in settings.py
   - Ensure the database exists: `psql -l`

2. **API Authentication Issues**
   - Verify you're using the correct token format: `Token your_token_here`
   - Check that your token hasn't expired
   - Ensure you're using the correct email/password combination

3. **Migration Errors**
   - Try resetting migrations: `python manage.py migrate --fake-initial`
   - Check for conflicting migrations

4. **Frontend Connection Issues**
   - Verify the backend server is running
   - Check for CORS issues in browser console
   - Ensure API base URL is correctly configured in frontend

## Features

### User Management
- Role-based authentication (Admin, Teacher, Student, Parent)
- Token-based API authentication
- User profile management
- Secure password handling

### Student Management
- Complete student profiles with personal and academic details
- Student admission process
- Parent/guardian information
- Class assignment
- Academic history tracking

### Teacher Management
- Teacher profiles with qualifications and specializations
- Department and designation assignment
- Class teacher allocation
- Experience and expertise tracking

### Academic Management
- Academic year configuration
- Class and section management
- Subject management
- Curriculum planning

### Attendance System
- Daily attendance tracking
- Attendance reports by class, subject, or date
- Absence notifications
- Attendance statistics

### Examination & Grading
- Exam type configuration
- Grade recording and management
- Performance analytics
- Report card generation

## API Endpoints

The following API endpoints are available:

### User Management
- `GET /api/users/me/` - Get current user details
- `GET /api/users/` - List all users (admin only)
- `POST /api/users/` - Create a new user (admin only)
- `GET /api/users/{id}/` - Get user details by ID (admin only)
- `PUT /api/users/{id}/` - Update user details (admin only)
- `DELETE /api/users/{id}/` - Delete a user (admin only)

### Student Management
- `GET /api/students/` - List all students
- `POST /api/students/` - Create a new student
- `GET /api/students/{id}/` - Get student details by ID
- `PUT /api/students/{id}/` - Update student details
- `DELETE /api/students/{id}/` - Delete a student

### Teacher Management
- `GET /api/teachers/` - List all teachers
- `POST /api/teachers/` - Create a new teacher
- `GET /api/teachers/{id}/` - Get teacher details by ID
- `PUT /api/teachers/{id}/` - Update teacher details
- `DELETE /api/teachers/{id}/` - Delete a teacher

### Attendance Management
- `GET /api/attendance/` - List all attendance records
- `POST /api/attendance/` - Create a new attendance record
- `GET /api/attendance/{id}/` - Get attendance details by ID
- `PUT /api/attendance/{id}/` - Update attendance details
- `DELETE /api/attendance/{id}/` - Delete an attendance record

### Course Management
- `GET /api/classes/` - List all classes
- `GET /api/subjects/` - List all subjects
- `GET /api/academic-years/` - List all academic years

### Grades Management
- `GET /api/exams/` - List all exams
- `GET /api/exam-types/` - List all exam types
- `GET /api/grades/` - List all grades

## Database Configuration

The project uses PostgreSQL as the database. Here's how to configure it:

1. Install PostgreSQL on your system if not already installed

2. Create a database for the project:
   ```sql
   CREATE DATABASE medhashaala;
   CREATE USER medhashaala_user WITH PASSWORD 'your_password';
   ALTER ROLE medhashaala_user SET client_encoding TO 'utf8';
   ALTER ROLE medhashaala_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE medhashaala_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE medhashaala TO medhashaala_user;
   ```

3. Update the database settings in `back-end/medhashaala/settings.py` if needed:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'medhashaala',
           'USER': 'medhashaala_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## Deployment

For production deployment, follow these steps:

1. Set `DEBUG = False` in `back-end/medhashaala/settings.py`

2. Configure proper `ALLOWED_HOSTS` in settings.py:
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

3. Set up a production-ready web server like Nginx or Apache

4. Use Gunicorn or uWSGI as the WSGI server:
   ```
   pip install gunicorn
   gunicorn medhashaala.wsgi:application --bind 0.0.0.0:8000
   ```

5. Set up a proper database backup strategy

6. Consider using environment variables for sensitive information

## License

MIT
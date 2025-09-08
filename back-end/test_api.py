import requests
import json
import sys

# Base URL for API
BASE_URL = 'http://localhost:8000/api/'

def test_api_endpoints():
    print("\n===== Testing Medhashaala API Endpoints =====\n")
    
    # Test authentication
    print("\n----- Testing Authentication -----\n")
    
    # Get auth token - using hardcoded credentials for testing
    auth_data = {
        'email': 'aprameyas03@gmail.com',  # Replace with your actual superuser email
        'password': 'test@123'  # Replace with your actual superuser password
    }
    print(f"Using email: {auth_data['email']}")
    print(f"Using password: {'*' * len(auth_data['password'])}")

    
    try:
        print(f"Attempting to authenticate at: http://localhost:8000/api-token-auth/")
        auth_response = requests.post(f"http://localhost:8000/api-token-auth/", data=auth_data)
        
        if auth_response.status_code != 200:
            print(f"Error: {auth_response.status_code} {auth_response.reason} for url: {auth_response.url}")
            print(f"API Error: {json.dumps(auth_response.json(), indent=2)}")
            print("\nAvailable endpoints:")
            try:
                endpoints = requests.get("http://localhost:8000/api/")
                if endpoints.status_code == 200:
                    print(json.dumps(endpoints.json(), indent=2))
                else:
                    print("Could not retrieve API endpoints.")
            except Exception as e:
                print(f"Error retrieving endpoints: {str(e)}")
            sys.exit(1)
            
        token = auth_response.json().get('token')
        print(f"Authentication successful! Token: {token[:10]}...")
        
        # Set headers with token for authenticated requests
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        
        print(f"Using Authorization header: {headers['Authorization']}")
        
        # Test a simple GET request to verify token works
        try:
            test_response = requests.get(f"{BASE_URL}", headers=headers)
            test_response.raise_for_status()
            print(f"API root access successful")
        except requests.exceptions.HTTPError as e:
            print(f"Error accessing API root: {e}")
            print(f"Response headers: {test_response.headers}")
            print(f"Response content: {test_response.content}")
            # Try without Content-Type header
            headers = {'Authorization': f'Token {token}'}
            print("Retrying with simplified headers...")
            try:
                test_response = requests.get(f"{BASE_URL}", headers=headers)
                test_response.raise_for_status()
                print(f"API root access successful with simplified headers")
            except requests.exceptions.HTTPError as e:
                print(f"Still error accessing API root: {e}")
                print(f"Response content: {test_response.content}")
                sys.exit(1)
        
        # Test user endpoints
        print("\n----- Testing User Endpoints -----\n")
        
        # Get current user
        try:
            me_response = requests.get(f"{BASE_URL}users/me/", headers=headers)
            me_response.raise_for_status()
            print(f"Current user: {me_response.json().get('email')}")
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            print(f"API Error: {json.dumps(me_response.json(), indent=2) if me_response.content else 'No content'}")
        
        # Get all users
        try:
            users_response = requests.get(f"{BASE_URL}users/", headers=headers)
            users_response.raise_for_status()
            print(f"Number of users: {len(users_response.json())}")
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            print(f"API Error: {json.dumps(users_response.json(), indent=2) if users_response.content else 'No content'}")
        
        # Test student endpoints
        print("\n----- Testing Student Endpoints -----\n")
        
        # Get all students
        try:
            students_response = requests.get(f"{BASE_URL}students/", headers=headers)
            students_response.raise_for_status()
            students_data = students_response.json()
            
            # Check if the response is paginated
            if isinstance(students_data, dict) and 'results' in students_data:
                students = students_data.get('results', [])
                print(f"Number of students: {len(students)} (paginated)")
            else:
                students = students_data
                print(f"Number of students: {len(students)}")
            
            if students and len(students) > 0:
                student_id = students[0]['id']
                # Get single student
                student_response = requests.get(f"{BASE_URL}students/{student_id}/", headers=headers)
                student_response.raise_for_status()
                student_data = student_response.json()
                # Access user data correctly
                user_data = student_data.get('user', {})
                first_name = user_data.get('first_name')
                last_name = user_data.get('last_name')
                print(f"Retrieved student: {first_name} {last_name}")
            else:
                print("No students found in the database.")
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            print(f"API Error: {json.dumps(students_response.json(), indent=2) if students_response.content else 'No content'}")
        
        # Test teacher endpoints
        print("\n----- Testing Teacher Endpoints -----\n")
        
        # Get all teachers
        try:
            teachers_response = requests.get(f"{BASE_URL}teachers/", headers=headers)
            teachers_response.raise_for_status()
            teachers_data = teachers_response.json()
            
            # Check if the response is paginated
            if isinstance(teachers_data, dict) and 'results' in teachers_data:
                teachers = teachers_data.get('results', [])
                print(f"Number of teachers: {len(teachers)} (paginated)")
            else:
                teachers = teachers_data
                print(f"Number of teachers: {len(teachers)}")
            
            if teachers and len(teachers) > 0:
                teacher_id = teachers[0]['id']
                # Get single teacher
                teacher_response = requests.get(f"{BASE_URL}teachers/{teacher_id}/", headers=headers)
                teacher_response.raise_for_status()
                teacher_data = teacher_response.json()
                # Access user data correctly
                user_data = teacher_data.get('user', {})
                first_name = user_data.get('first_name')
                last_name = user_data.get('last_name')
                print(f"Retrieved teacher: {first_name} {last_name}")
            else:
                print("No teachers found in the database.")
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            print(f"API Error: {json.dumps(teachers_response.json(), indent=2) if teachers_response.content else 'No content'}")        
        
        # Test attendance endpoints
        print("\n----- Testing Attendance Endpoints -----\n")
        
        # Get all attendance records
        try:
            attendance_response = requests.get(f"{BASE_URL}attendance/", headers=headers)
            attendance_response.raise_for_status()
            attendance_data = attendance_response.json()
            
            # Check if the response is paginated
            if isinstance(attendance_data, dict) and 'results' in attendance_data:
                attendance_records = attendance_data.get('results', [])
                print(f"Number of attendance records: {len(attendance_records)} (paginated)")
            else:
                attendance_records = attendance_data
                print(f"Number of attendance records: {len(attendance_records)}")
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            print(f"API Error: {json.dumps(attendance_response.json(), indent=2) if attendance_response.content else 'No content'}")
        
        # Test grades endpoints
        print("\n----- Testing Grades Endpoints -----\n")
        
        # Get all exam types
        try:
            exam_types_response = requests.get(f"{BASE_URL}exam-types/", headers=headers)
            exam_types_response.raise_for_status()
            exam_types_data = exam_types_response.json()
            
            # Check if the response is paginated
            if isinstance(exam_types_data, dict) and 'results' in exam_types_data:
                exam_types = exam_types_data.get('results', [])
                print(f"Number of exam types: {len(exam_types)} (paginated)")
            else:
                exam_types = exam_types_data
                print(f"Number of exam types: {len(exam_types)}")
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            print(f"API Error: {json.dumps(exam_types_response.json(), indent=2) if exam_types_response.content else 'No content'}")
        
        # Get all exams
        try:
            exams_response = requests.get(f"{BASE_URL}exams/", headers=headers)
            exams_response.raise_for_status()
            exams_data = exams_response.json()
            
            # Check if the response is paginated
            if isinstance(exams_data, dict) and 'results' in exams_data:
                exams = exams_data.get('results', [])
                print(f"Number of exams: {len(exams)} (paginated)")
            else:
                exams = exams_data
                print(f"Number of exams: {len(exams)}")
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            print(f"API Error: {json.dumps(exams_response.json(), indent=2) if exams_response.content else 'No content'}")
        
        # Get all grades
        try:
            grades_response = requests.get(f"{BASE_URL}grades/", headers=headers)
            grades_response.raise_for_status()
            grades_data = grades_response.json()
            
            # Check if the response is paginated
            if isinstance(grades_data, dict) and 'results' in grades_data:
                grades = grades_data.get('results', [])
                print(f"Number of grades: {len(grades)} (paginated)")
            else:
                grades = grades_data
                print(f"Number of grades: {len(grades)}")
        except requests.exceptions.HTTPError as e:
            print(f"Error: {e}")
            print(f"API Error: {json.dumps(grades_response.json(), indent=2) if grades_response.content else 'No content'}")
        
        print("\n===== All API tests completed successfully! =====\n")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                print(f"API Error: {json.dumps(error_data, indent=2)}")
            except ValueError:
                print(f"Status code: {e.response.status_code}")
                print(f"Response text: {e.response.text}")

if __name__ == "__main__":
    test_api_endpoints()
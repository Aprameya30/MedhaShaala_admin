import os
import sys
import django
import random
from datetime import datetime, timedelta
from faker import Faker

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medhashaala_erp.settings')
django.setup()

# Import models
from django.contrib.auth import get_user_model
from students.models import Student
from teachers.models import Teacher
from courses.models import AcademicYear, Class, Subject
from attendance.models import Attendance

User = get_user_model()
fake = Faker()

# Helper function to create a user with complete information
def create_user(email, first_name, last_name, user_type, phone_number=None, address=None, password='password123'):
    try:
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            phone_number=phone_number or fake.phone_number()[:15],
            address=address or fake.address()
        )
        print(f"Created user: {user}")
        return user
    except Exception as e:
        print(f"Error creating user {email}: {e}")
        return None

# Create academic year
def create_academic_year():
    try:
        academic_year = AcademicYear.objects.create(
            name="2023-2024",
            start_date=datetime(2023, 6, 1),
            end_date=datetime(2024, 4, 30),
            is_active=True
        )
        print(f"Created academic year: {academic_year}")
        return academic_year
    except Exception as e:
        print(f"Error creating academic year: {e}")
        # Try to get existing academic year
        try:
            return AcademicYear.objects.get(name="2023-2024")
        except:
            return None

# Create subjects
def create_subjects():
    subjects = [
        {"name": "Mathematics", "code": "MATH101"},
        {"name": "Science", "code": "SCI101"},
        {"name": "English", "code": "ENG101"},
        {"name": "Social Studies", "code": "SOC101"},
        {"name": "Computer Science", "code": "CS101"}
    ]
    
    created_subjects = []
    for subject_data in subjects:
        try:
            subject, created = Subject.objects.get_or_create(
                code=subject_data["code"],
                defaults={"name": subject_data["name"]}
            )
            if created:
                print(f"Created subject: {subject}")
            else:
                print(f"Subject already exists: {subject}")
            created_subjects.append(subject)
        except Exception as e:
            print(f"Error creating subject {subject_data['name']}: {e}")
    
    return created_subjects

# Create teachers with comprehensive data
def create_teachers(num_teachers=10):
    departments = ["Mathematics", "Science", "English", "Social Studies", "Physical Education", 
                  "Arts", "Music", "Computer Science", "Languages", "Administration"]
    
    specializations = {
        "Mathematics": ["Algebra", "Geometry", "Calculus", "Statistics"],
        "Science": ["Physics", "Chemistry", "Biology", "Environmental Science"],
        "English": ["Literature", "Grammar", "Creative Writing"],
        "Social Studies": ["History", "Geography", "Civics", "Economics"],
        "Physical Education": ["Sports", "Health Education", "Yoga"],
        "Arts": ["Drawing", "Painting", "Craft"],
        "Music": ["Vocal", "Instrumental", "Theory"],
        "Computer Science": ["Programming", "Web Development", "IT"],
        "Languages": ["Hindi", "Sanskrit", "French"],
        "Administration": ["Management", "Coordination"]
    }
    
    designations = ["Senior Teacher", "Junior Teacher", "Head of Department", "Subject Coordinator", 
                   "Vice Principal", "Principal", "Assistant Teacher"]
    
    qualifications = ["B.Ed", "M.Ed", "B.A. B.Ed", "M.A. B.Ed", "M.Sc. B.Ed", "Ph.D", "M.Phil"]
    
    created_teachers = []
    for i in range(num_teachers):
        first_name = fake.first_name()
        last_name = fake.last_name()
        department = random.choice(departments)
        
        user = create_user(
            email=f"{first_name.lower()}.{last_name.lower()}@medhashaala.edu",
            first_name=first_name,
            last_name=last_name,
            user_type="teacher",
            phone_number=fake.phone_number()[:15],
            address=fake.address()
        )
        
        if user:
            try:
                teacher = Teacher.objects.create(
                    user=user,
                    employee_id=f"T{i+1:03d}",
                    date_of_joining=fake.date_between(start_date='-5y', end_date='today'),
                    designation=random.choice(designations),
                    department=department,
                    qualification=random.choice(qualifications),
                    experience=random.randint(1, 20),
                    specialization=random.choice(specializations.get(department, ["General"])),
                    date_of_birth=fake.date_of_birth(minimum_age=25, maximum_age=60),
                    gender=random.choice(["male", "female", "other"]),
                    is_active=random.choice([True, True, True, False]),  # 75% active
                    is_class_teacher=random.choice([True, False]),
                    remarks=fake.sentence() if random.choice([True, False]) else ""
                )
                print(f"Created teacher: {teacher}")
                created_teachers.append(teacher)
            except Exception as e:
                print(f"Error creating teacher for {user}: {e}")
    
    return created_teachers

# Create classes
def create_classes(academic_year, teachers):
    class_data = [
        {"name": "Grade 1", "sections": "A,B"},
        {"name": "Grade 2", "sections": "A,B"},
        {"name": "Grade 3", "sections": "A,B"}
    ]
    
    created_classes = []
    for i, data in enumerate(class_data):
        try:
            class_obj, created = Class.objects.get_or_create(
                name=data["name"],
                academic_year=academic_year,
                defaults={
                    "sections": data["sections"],
                    "class_teacher": teachers[i % len(teachers)] if teachers else None
                }
            )
            if created:
                print(f"Created class: {class_obj}")
            else:
                print(f"Class already exists: {class_obj}")
            created_classes.append(class_obj)
        except Exception as e:
            print(f"Error creating class {data['name']}: {e}")
    
    return created_classes

# Create students with comprehensive data including realistic parent information
def create_students(num_students=50, classes=None):
    blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    sections = ["A", "B", "C", "D"]
    grades = ["Kindergarten", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    
    # Create some families with multiple children
    families = []
    for i in range(15):  # 15 families
        parent_first = fake.first_name()
        parent_last = fake.last_name()
        families.append({
            "parent_name": f"{parent_first} {parent_last}",
            "parent_phone": fake.phone_number()[:15],
            "parent_email": f"{parent_first.lower()}.{parent_last.lower()}@gmail.com",
            "children_count": random.choice([1, 1, 1, 2, 2, 3])  # Most families have 1-2 children
        })
    
    created_students = []
    family_index = 0
    children_in_current_family = 0
    
    for i in range(num_students):
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        # Assign to family
        current_family = families[family_index % len(families)]
        if children_in_current_family >= current_family["children_count"]:
            family_index += 1
            children_in_current_family = 0
            current_family = families[family_index % len(families)]
        
        user = create_user(
            email=f"{first_name.lower()}.{last_name.lower()}@student.medhashaala.edu",
            first_name=first_name,
            last_name=last_name,
            user_type="student",
            phone_number=fake.phone_number()[:15] if random.choice([True, False]) else None,
            address=fake.address()
        )
        
        if user:
            try:
                # Assign grade and section
                grade = random.choice(grades)
                section = random.choice(sections)
                
                student = Student.objects.create(
                    user=user,
                    admission_number=f"S{i+1:04d}",
                    roll_number=f"{grade}-{section}-{random.randint(1, 40):02d}",
                    date_of_admission=fake.date_between(start_date='-3y', end_date='today'),
                    date_of_birth=fake.date_of_birth(minimum_age=4, maximum_age=18),
                    gender=random.choice(["male", "female", "other"]),
                    blood_group=random.choice(blood_groups),
                    parent_name=current_family["parent_name"],
                    parent_phone=current_family["parent_phone"],
                    parent_email=current_family["parent_email"],
                    is_active=random.choice([True, True, True, True, False]),  # 80% active
                    current_class=classes[0] if classes else None,  # Assign to first class for now
                    current_section=section,
                    previous_school=fake.company() + " School" if random.choice([True, False]) else None,
                    remarks=fake.sentence() if random.choice([True, False, False]) else ""
                )
                print(f"Created student: {student}")
                created_students.append(student)
                children_in_current_family += 1
            except Exception as e:
                print(f"Error creating student for {user}: {e}")
    
    return created_students

# Create attendance records
def create_attendance_records(students, num_days=5):
    created_records = []
    for student in students:
        for day in range(num_days):
            date = datetime.now() - timedelta(days=day)
            try:
                attendance, created = Attendance.objects.get_or_create(
                    student=student,
                    date=date,
                    defaults={
                        "status": random.choice(["present", "absent", "late"]),
                        "remarks": "Auto-generated attendance record"
                    }
                )
                if created:
                    print(f"Created attendance record: {attendance}")
                else:
                    print(f"Attendance record already exists: {attendance}")
                created_records.append(attendance)
            except Exception as e:
                print(f"Error creating attendance record for {student} on {date}: {e}")
    
    return created_records

# Create staff members with comprehensive data
def create_staff_members(num_staff=15):
    departments = ["Administration", "Accounts", "IT Support", "Library", "Maintenance", 
                  "Security", "Transport", "Cafeteria", "Medical", "Counseling"]
    
    designations = {
        "Administration": ["Office Manager", "Administrative Assistant", "Receptionist", "Data Entry Clerk"],
        "Accounts": ["Accountant", "Finance Manager", "Accounts Assistant", "Cashier"],
        "IT Support": ["IT Administrator", "Network Engineer", "Technical Support", "System Admin"],
        "Library": ["Librarian", "Library Assistant", "Cataloger"],
        "Maintenance": ["Maintenance Supervisor", "Electrician", "Plumber", "Janitor"],
        "Security": ["Security Guard", "Security Supervisor"],
        "Transport": ["Driver", "Transport Coordinator"],
        "Cafeteria": ["Chef", "Kitchen Assistant", "Cafeteria Manager"],
        "Medical": ["School Nurse", "Medical Assistant"],
        "Counseling": ["Counselor", "Psychologist"]
    }
    
    created_staff = []
    for i in range(num_staff):
        first_name = fake.first_name()
        last_name = fake.last_name()
        department = random.choice(departments)
        designation = random.choice(designations.get(department, ["Staff Member"]))
        
        user = create_user(
            email=f"{first_name.lower()}.{last_name.lower()}@medhashaala.edu",
            first_name=first_name,
            last_name=last_name,
            user_type="admin",  # Using admin type for staff since there's no staff type in USER_TYPE_CHOICES
            phone_number=fake.phone_number()[:15],
            address=fake.address()
        )
        
        if user:
            # Add additional fields to user for staff information
            user.department = department
            user.designation = designation
            user.employee_id = f"ST{i+1:03d}"
            user.role = "staff"
            user.status = random.choice(["Active", "Active", "Active", "Inactive"])
            user.save()
            
            print(f"Created staff member: {user}")
            created_staff.append(user)
    
    return created_staff

# Main function to create all dummy data
def create_dummy_data():
    print("\n===== Creating Dummy Data for Medhashaala ERP =====\n")
    
    # Create academic year
    academic_year = create_academic_year()
    if not academic_year:
        print("Failed to create academic year. Exiting.")
        return
    
    # Create subjects
    subjects = create_subjects()
    
    # Create teachers
    teachers = create_teachers(num_teachers=10)
    
    # Create classes
    classes = create_classes(academic_year, teachers)
    
    # Create students
    students = create_students(num_students=50, classes=classes)
    
    # Create staff members
    staff = create_staff_members(num_staff=15)
    
    # Create attendance records
    attendance_records = create_attendance_records(students, num_days=10)
    
    print("\n===== Dummy Data Creation Complete =====\n")
    print(f"Created {len(subjects)} subjects")
    print(f"Created {len(teachers)} teachers")
    print(f"Created {len(classes)} classes")
    print(f"Created {len(students)} students")
    print(f"Created {len(staff)} staff members")
    print(f"Created {len(attendance_records)} attendance records")

if __name__ == "__main__":
    create_dummy_data()

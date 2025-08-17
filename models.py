"""
Data models for the Student Management System using in-memory storage.
All data is stored in Python dictionaries and lists for simplicity.
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class DataStore:
    """Simple in-memory data store using dictionaries"""
    
    def __init__(self):
        self.students: Dict[int, Dict] = {}
        self.courses: Dict[int, Dict] = {}
        self.enrollments: Dict[int, Dict] = {}
        self.grades: Dict[int, Dict] = {}
        
        # Auto-incrementing IDs
        self.next_student_id = 1
        self.next_course_id = 1
        self.next_enrollment_id = 1
        self.next_grade_id = 1

# Global data store instance
data_store = DataStore()

class Student:
    """Student model with CRUD operations"""
    
    @staticmethod
    def create(name: str, email: str, phone: str, address: str) -> Dict:
        """Create a new student record"""
        student_id = data_store.next_student_id
        data_store.next_student_id += 1
        
        student = {
            'id': student_id,
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        data_store.students[student_id] = student
        return student
    
    @staticmethod
    def get(student_id: int) -> Optional[Dict]:
        """Get a student by ID"""
        return data_store.students.get(student_id)
    
    @staticmethod
    def get_all() -> List[Dict]:
        """Get all students"""
        return list(data_store.students.values())
    
    @staticmethod
    def update(student_id: int, name: str, email: str, phone: str, address: str) -> Optional[Dict]:
        """Update a student record"""
        if student_id not in data_store.students:
            return None
        
        student = data_store.students[student_id]
        student.update({
            'name': name,
            'email': email,
            'phone': phone,
            'address': address,
            'updated_at': datetime.now().isoformat()
        })
        
        return student
    
    @staticmethod
    def delete(student_id: int) -> bool:
        """Delete a student record"""
        if student_id not in data_store.students:
            return False
        
        # Also delete related enrollments and grades
        Enrollment.delete_by_student(student_id)
        Grade.delete_by_student(student_id)
        
        del data_store.students[student_id]
        return True
    
    @staticmethod
    def search(query: str) -> List[Dict]:
        """Search students by name or email"""
        if not query:
            return Student.get_all()
        
        query = query.lower()
        results = []
        
        for student in data_store.students.values():
            if (query in student['name'].lower() or 
                query in student['email'].lower()):
                results.append(student)
        
        return results
    
    @staticmethod
    def calculate_gpa(student_id: int) -> float:
        """Calculate GPA for a student"""
        student_grades = Grade.get_by_student(student_id)
        
        if not student_grades:
            return 0.0
        
        total_points = 0
        total_credits = 0
        
        for grade in student_grades:
            course = Course.get(grade['course_id'])
            if course:
                grade_points = Grade.letter_to_points(grade['letter_grade'])
                credits = course['credits']
                total_points += grade_points * credits
                total_credits += credits
        
        if total_credits == 0:
            return 0.0
        
        return round(total_points / total_credits, 2)

class Course:
    """Course model with CRUD operations"""
    
    @staticmethod
    def create(code: str, name: str, description: str, credits: int) -> Dict:
        """Create a new course"""
        course_id = data_store.next_course_id
        data_store.next_course_id += 1
        
        course = {
            'id': course_id,
            'code': code,
            'name': name,
            'description': description,
            'credits': credits,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        data_store.courses[course_id] = course
        return course
    
    @staticmethod
    def get(course_id: int) -> Optional[Dict]:
        """Get a course by ID"""
        return data_store.courses.get(course_id)
    
    @staticmethod
    def get_all() -> List[Dict]:
        """Get all courses"""
        return list(data_store.courses.values())
    
    @staticmethod
    def update(course_id: int, code: str, name: str, description: str, credits: int) -> Optional[Dict]:
        """Update a course record"""
        if course_id not in data_store.courses:
            return None
        
        course = data_store.courses[course_id]
        course.update({
            'code': code,
            'name': name,
            'description': description,
            'credits': credits,
            'updated_at': datetime.now().isoformat()
        })
        
        return course
    
    @staticmethod
    def delete(course_id: int) -> bool:
        """Delete a course record"""
        if course_id not in data_store.courses:
            return False
        
        # Also delete related enrollments and grades
        Enrollment.delete_by_course(course_id)
        Grade.delete_by_course(course_id)
        
        del data_store.courses[course_id]
        return True

class Enrollment:
    """Enrollment model linking students to courses"""
    
    @staticmethod
    def create(student_id: int, course_id: int) -> Dict:
        """Create a new enrollment"""
        # Check if enrollment already exists
        for enrollment in data_store.enrollments.values():
            if enrollment['student_id'] == student_id and enrollment['course_id'] == course_id:
                return enrollment
        
        enrollment_id = data_store.next_enrollment_id
        data_store.next_enrollment_id += 1
        
        enrollment = {
            'id': enrollment_id,
            'student_id': student_id,
            'course_id': course_id,
            'enrolled_at': datetime.now().isoformat()
        }
        
        data_store.enrollments[enrollment_id] = enrollment
        return enrollment
    
    @staticmethod
    def get(enrollment_id: int) -> Optional[Dict]:
        """Get an enrollment by ID"""
        return data_store.enrollments.get(enrollment_id)
    
    @staticmethod
    def get_all() -> List[Dict]:
        """Get all enrollments"""
        return list(data_store.enrollments.values())
    
    @staticmethod
    def get_by_student(student_id: int) -> List[Dict]:
        """Get all enrollments for a student"""
        return [e for e in data_store.enrollments.values() if e['student_id'] == student_id]
    
    @staticmethod
    def get_by_course(course_id: int) -> List[Dict]:
        """Get all enrollments for a course"""
        return [e for e in data_store.enrollments.values() if e['course_id'] == course_id]
    
    @staticmethod
    def delete(enrollment_id: int) -> bool:
        """Delete an enrollment"""
        if enrollment_id not in data_store.enrollments:
            return False
        
        enrollment = data_store.enrollments[enrollment_id]
        # Also delete related grades
        Grade.delete_by_student_course(enrollment['student_id'], enrollment['course_id'])
        
        del data_store.enrollments[enrollment_id]
        return True
    
    @staticmethod
    def delete_by_student(student_id: int):
        """Delete all enrollments for a student"""
        to_delete = [eid for eid, e in data_store.enrollments.items() if e['student_id'] == student_id]
        for eid in to_delete:
            del data_store.enrollments[eid]
    
    @staticmethod
    def delete_by_course(course_id: int):
        """Delete all enrollments for a course"""
        to_delete = [eid for eid, e in data_store.enrollments.items() if e['course_id'] == course_id]
        for eid in to_delete:
            del data_store.enrollments[eid]

class Grade:
    """Grade model for tracking student performance"""
    
    GRADE_POINTS = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'D-': 0.7,
        'F': 0.0
    }
    
    @staticmethod
    def create(student_id: int, course_id: int, letter_grade: str, points: Optional[float] = None) -> Dict:
        """Create or update a grade"""
        # Check if grade already exists for this student-course combination
        for grade_id, grade in data_store.grades.items():
            if grade['student_id'] == student_id and grade['course_id'] == course_id:
                # Update existing grade
                grade.update({
                    'letter_grade': letter_grade,
                    'points': points or Grade.letter_to_points(letter_grade),
                    'updated_at': datetime.now().isoformat()
                })
                return grade
        
        # Create new grade
        grade_id = data_store.next_grade_id
        data_store.next_grade_id += 1
        
        grade = {
            'id': grade_id,
            'student_id': student_id,
            'course_id': course_id,
            'letter_grade': letter_grade,
            'points': points or Grade.letter_to_points(letter_grade),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        data_store.grades[grade_id] = grade
        return grade
    
    @staticmethod
    def get(grade_id: int) -> Optional[Dict]:
        """Get a grade by ID"""
        return data_store.grades.get(grade_id)
    
    @staticmethod
    def get_all() -> List[Dict]:
        """Get all grades"""
        return list(data_store.grades.values())
    
    @staticmethod
    def get_by_student(student_id: int) -> List[Dict]:
        """Get all grades for a student"""
        return [g for g in data_store.grades.values() if g['student_id'] == student_id]
    
    @staticmethod
    def get_by_course(course_id: int) -> List[Dict]:
        """Get all grades for a course"""
        return [g for g in data_store.grades.values() if g['course_id'] == course_id]
    
    @staticmethod
    def get_by_student_course(student_id: int, course_id: int) -> Optional[Dict]:
        """Get grade for specific student-course combination"""
        for grade in data_store.grades.values():
            if grade['student_id'] == student_id and grade['course_id'] == course_id:
                return grade
        return None
    
    @staticmethod
    def delete(grade_id: int) -> bool:
        """Delete a grade"""
        if grade_id not in data_store.grades:
            return False
        del data_store.grades[grade_id]
        return True
    
    @staticmethod
    def delete_by_student(student_id: int):
        """Delete all grades for a student"""
        to_delete = [gid for gid, g in data_store.grades.items() if g['student_id'] == student_id]
        for gid in to_delete:
            del data_store.grades[gid]
    
    @staticmethod
    def delete_by_course(course_id: int):
        """Delete all grades for a course"""
        to_delete = [gid for gid, g in data_store.grades.items() if g['course_id'] == course_id]
        for gid in to_delete:
            del data_store.grades[gid]
    
    @staticmethod
    def delete_by_student_course(student_id: int, course_id: int):
        """Delete grade for specific student-course combination"""
        to_delete = [gid for gid, g in data_store.grades.items() 
                    if g['student_id'] == student_id and g['course_id'] == course_id]
        for gid in to_delete:
            del data_store.grades[gid]
    
    @staticmethod
    def letter_to_points(letter_grade: str) -> float:
        """Convert letter grade to grade points"""
        return Grade.GRADE_POINTS.get(letter_grade, 0.0)

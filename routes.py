"""
Routes for the Student Management System
"""

from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app
from models import Student, Course, Enrollment, Grade

@app.route('/')
def index():
    """Dashboard with summary statistics"""
    stats = {
        'total_students': len(Student.get_all()),
        'total_courses': len(Course.get_all()),
        'total_enrollments': len(Enrollment.get_all()),
        'total_grades': len(Grade.get_all())
    }
    return render_template('index.html', stats=stats)

# Student Routes
@app.route('/students')
def students():
    """List all students with search functionality"""
    search_query = request.args.get('search', '')
    if search_query:
        students_list = Student.search(search_query)
    else:
        students_list = Student.get_all()
    
    # Add GPA to each student
    for student in students_list:
        student['gpa'] = Student.calculate_gpa(student['id'])
    
    return render_template('students.html', students=students_list, search_query=search_query)

@app.route('/students/new')
def new_student():
    """Show form to create new student"""
    return render_template('student_form.html', student=None)

@app.route('/students/create', methods=['POST'])
def create_student():
    """Create a new student"""
    try:
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        phone = request.form['phone'].strip()
        address = request.form['address'].strip()
        
        # Basic validation
        if not all([name, email, phone, address]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('new_student'))
        
        # Check for duplicate email
        existing_students = Student.get_all()
        for student in existing_students:
            if student['email'].lower() == email.lower():
                flash('A student with this email already exists.', 'danger')
                return redirect(url_for('new_student'))
        
        student = Student.create(name, email, phone, address)
        flash(f'Student {name} created successfully!', 'success')
        return redirect(url_for('students'))
        
    except Exception as e:
        flash(f'Error creating student: {str(e)}', 'danger')
        return redirect(url_for('new_student'))

@app.route('/students/<int:student_id>/edit')
def edit_student(student_id):
    """Show form to edit student"""
    student = Student.get(student_id)
    if not student:
        flash('Student not found.', 'danger')
        return redirect(url_for('students'))
    return render_template('student_form.html', student=student)

@app.route('/students/<int:student_id>/update', methods=['POST'])
def update_student(student_id):
    """Update a student"""
    try:
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        phone = request.form['phone'].strip()
        address = request.form['address'].strip()
        
        # Basic validation
        if not all([name, email, phone, address]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('edit_student', student_id=student_id))
        
        # Check for duplicate email (excluding current student)
        existing_students = Student.get_all()
        for student in existing_students:
            if student['id'] != student_id and student['email'].lower() == email.lower():
                flash('A student with this email already exists.', 'danger')
                return redirect(url_for('edit_student', student_id=student_id))
        
        student = Student.update(student_id, name, email, phone, address)
        if student:
            flash(f'Student {name} updated successfully!', 'success')
        else:
            flash('Student not found.', 'danger')
        
        return redirect(url_for('students'))
        
    except Exception as e:
        flash(f'Error updating student: {str(e)}', 'danger')
        return redirect(url_for('edit_student', student_id=student_id))

@app.route('/students/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    """Delete a student"""
    try:
        student = Student.get(student_id)
        if not student:
            flash('Student not found.', 'danger')
        elif Student.delete(student_id):
            flash(f'Student {student["name"]} deleted successfully!', 'success')
        else:
            flash('Error deleting student.', 'danger')
    except Exception as e:
        flash(f'Error deleting student: {str(e)}', 'danger')
    
    return redirect(url_for('students'))

# Course Routes
@app.route('/courses')
def courses():
    """List all courses"""
    courses_list = Course.get_all()
    
    # Add enrollment count to each course
    for course in courses_list:
        enrollments = Enrollment.get_by_course(course['id'])
        course['enrollment_count'] = len(enrollments)
    
    return render_template('courses.html', courses=courses_list)

@app.route('/courses/new')
def new_course():
    """Show form to create new course"""
    return render_template('course_form.html', course=None)

@app.route('/courses/create', methods=['POST'])
def create_course():
    """Create a new course"""
    try:
        code = request.form['code'].strip().upper()
        name = request.form['name'].strip()
        description = request.form['description'].strip()
        credits = int(request.form['credits'])
        
        # Basic validation
        if not all([code, name, description]) or credits <= 0:
            flash('All fields are required and credits must be positive.', 'danger')
            return redirect(url_for('new_course'))
        
        # Check for duplicate course code
        existing_courses = Course.get_all()
        for course in existing_courses:
            if course['code'] == code:
                flash('A course with this code already exists.', 'danger')
                return redirect(url_for('new_course'))
        
        course = Course.create(code, name, description, credits)
        flash(f'Course {code} created successfully!', 'success')
        return redirect(url_for('courses'))
        
    except ValueError:
        flash('Credits must be a valid number.', 'danger')
        return redirect(url_for('new_course'))
    except Exception as e:
        flash(f'Error creating course: {str(e)}', 'danger')
        return redirect(url_for('new_course'))

@app.route('/courses/<int:course_id>/edit')
def edit_course(course_id):
    """Show form to edit course"""
    course = Course.get(course_id)
    if not course:
        flash('Course not found.', 'danger')
        return redirect(url_for('courses'))
    return render_template('course_form.html', course=course)

@app.route('/courses/<int:course_id>/update', methods=['POST'])
def update_course(course_id):
    """Update a course"""
    try:
        code = request.form['code'].strip().upper()
        name = request.form['name'].strip()
        description = request.form['description'].strip()
        credits = int(request.form['credits'])
        
        # Basic validation
        if not all([code, name, description]) or credits <= 0:
            flash('All fields are required and credits must be positive.', 'danger')
            return redirect(url_for('edit_course', course_id=course_id))
        
        # Check for duplicate course code (excluding current course)
        existing_courses = Course.get_all()
        for course in existing_courses:
            if course['id'] != course_id and course['code'] == code:
                flash('A course with this code already exists.', 'danger')
                return redirect(url_for('edit_course', course_id=course_id))
        
        course = Course.update(course_id, code, name, description, credits)
        if course:
            flash(f'Course {code} updated successfully!', 'success')
        else:
            flash('Course not found.', 'danger')
        
        return redirect(url_for('courses'))
        
    except ValueError:
        flash('Credits must be a valid number.', 'danger')
        return redirect(url_for('edit_course', course_id=course_id))
    except Exception as e:
        flash(f'Error updating course: {str(e)}', 'danger')
        return redirect(url_for('edit_course', course_id=course_id))

@app.route('/courses/<int:course_id>/delete', methods=['POST'])
def delete_course(course_id):
    """Delete a course"""
    try:
        course = Course.get(course_id)
        if not course:
            flash('Course not found.', 'danger')
        elif Course.delete(course_id):
            flash(f'Course {course["code"]} deleted successfully!', 'success')
        else:
            flash('Error deleting course.', 'danger')
    except Exception as e:
        flash(f'Error deleting course: {str(e)}', 'danger')
    
    return redirect(url_for('courses'))

# Enrollment Routes
@app.route('/enrollments')
def enrollments():
    """List all enrollments"""
    enrollments_list = Enrollment.get_all()
    
    # Enhance with student and course data
    for enrollment in enrollments_list:
        student = Student.get(enrollment['student_id'])
        course = Course.get(enrollment['course_id'])
        enrollment['student_name'] = student['name'] if student else 'Unknown'
        enrollment['course_code'] = course['code'] if course else 'Unknown'
        enrollment['course_name'] = course['name'] if course else 'Unknown'
    
    return render_template('enrollments.html', enrollments=enrollments_list)

@app.route('/enrollments/new')
def new_enrollment():
    """Show form to create new enrollment"""
    students_list = Student.get_all()
    courses_list = Course.get_all()
    
    if not students_list:
        flash('No students available. Please add students first.', 'warning')
        return redirect(url_for('enrollments'))
    
    if not courses_list:
        flash('No courses available. Please add courses first.', 'warning')
        return redirect(url_for('enrollments'))
    
    return render_template('enrollment_form.html', 
                         students=students_list, 
                         courses=courses_list, 
                         enrollment=None)

@app.route('/enrollments/create', methods=['POST'])
def create_enrollment():
    """Create a new enrollment"""
    try:
        student_id = int(request.form['student_id'])
        course_id = int(request.form['course_id'])
        
        # Validate student and course exist
        student = Student.get(student_id)
        course = Course.get(course_id)
        
        if not student:
            flash('Selected student not found.', 'danger')
            return redirect(url_for('new_enrollment'))
        
        if not course:
            flash('Selected course not found.', 'danger')
            return redirect(url_for('new_enrollment'))
        
        enrollment = Enrollment.create(student_id, course_id)
        flash(f'{student["name"]} enrolled in {course["code"]} successfully!', 'success')
        return redirect(url_for('enrollments'))
        
    except ValueError:
        flash('Invalid student or course selection.', 'danger')
        return redirect(url_for('new_enrollment'))
    except Exception as e:
        flash(f'Error creating enrollment: {str(e)}', 'danger')
        return redirect(url_for('new_enrollment'))

@app.route('/enrollments/<int:enrollment_id>/delete', methods=['POST'])
def delete_enrollment(enrollment_id):
    """Delete an enrollment"""
    try:
        enrollment = Enrollment.get(enrollment_id)
        if not enrollment:
            flash('Enrollment not found.', 'danger')
        elif Enrollment.delete(enrollment_id):
            student = Student.get(enrollment['student_id'])
            course = Course.get(enrollment['course_id'])
            flash(f'Enrollment deleted successfully!', 'success')
        else:
            flash('Error deleting enrollment.', 'danger')
    except Exception as e:
        flash(f'Error deleting enrollment: {str(e)}', 'danger')
    
    return redirect(url_for('enrollments'))

# Grade Routes
@app.route('/grades')
def grades():
    """List all grades"""
    grades_list = Grade.get_all()
    
    # Enhance with student and course data
    for grade in grades_list:
        student = Student.get(grade['student_id'])
        course = Course.get(grade['course_id'])
        grade['student_name'] = student['name'] if student else 'Unknown'
        grade['course_code'] = course['code'] if course else 'Unknown'
        grade['course_name'] = course['name'] if course else 'Unknown'
    
    return render_template('grades.html', grades=grades_list)

@app.route('/grades/new')
def new_grade():
    """Show form to create new grade"""
    enrollments_list = Enrollment.get_all()
    
    if not enrollments_list:
        flash('No enrollments available. Students must be enrolled in courses first.', 'warning')
        return redirect(url_for('grades'))
    
    # Enhance enrollments with student and course data
    for enrollment in enrollments_list:
        student = Student.get(enrollment['student_id'])
        course = Course.get(enrollment['course_id'])
        enrollment['student_name'] = student['name'] if student else 'Unknown'
        enrollment['course_code'] = course['code'] if course else 'Unknown'
        enrollment['course_name'] = course['name'] if course else 'Unknown'
    
    return render_template('grade_form.html', 
                         enrollments=enrollments_list, 
                         grade=None,
                         grade_options=list(Grade.GRADE_POINTS.keys()))

@app.route('/grades/create', methods=['POST'])
def create_grade():
    """Create a new grade"""
    try:
        student_id = int(request.form['student_id'])
        course_id = int(request.form['course_id'])
        letter_grade = request.form['letter_grade']
        
        # Validate inputs
        if letter_grade not in Grade.GRADE_POINTS:
            flash('Invalid grade selected.', 'danger')
            return redirect(url_for('new_grade'))
        
        # Check if enrollment exists
        enrollments = Enrollment.get_by_student(student_id)
        enrolled_courses = [e['course_id'] for e in enrollments]
        
        if course_id not in enrolled_courses:
            flash('Student is not enrolled in the selected course.', 'danger')
            return redirect(url_for('new_grade'))
        
        grade = Grade.create(student_id, course_id, letter_grade)
        student = Student.get(student_id)
        course = Course.get(course_id)
        
        if student and course:
            flash(f'Grade {letter_grade} assigned to {student["name"]} for {course["code"]}!', 'success')
        else:
            flash('Grade assigned successfully!', 'success')
        return redirect(url_for('grades'))
        
    except ValueError:
        flash('Invalid input provided.', 'danger')
        return redirect(url_for('new_grade'))
    except Exception as e:
        flash(f'Error creating grade: {str(e)}', 'danger')
        return redirect(url_for('new_grade'))

@app.route('/grades/<int:grade_id>/edit')
def edit_grade(grade_id):
    """Show form to edit grade"""
    grade = Grade.get(grade_id)
    if not grade:
        flash('Grade not found.', 'danger')
        return redirect(url_for('grades'))
    
    # Get enrollment info
    student = Student.get(grade['student_id'])
    course = Course.get(grade['course_id'])
    
    return render_template('grade_form.html', 
                         grade=grade,
                         student=student,
                         course=course,
                         grade_options=list(Grade.GRADE_POINTS.keys()))

@app.route('/grades/<int:grade_id>/update', methods=['POST'])
def update_grade(grade_id):
    """Update a grade"""
    try:
        letter_grade = request.form['letter_grade']
        
        if letter_grade not in Grade.GRADE_POINTS:
            flash('Invalid grade selected.', 'danger')
            return redirect(url_for('edit_grade', grade_id=grade_id))
        
        grade = Grade.get(grade_id)
        if not grade:
            flash('Grade not found.', 'danger')
            return redirect(url_for('grades'))
        
        updated_grade = Grade.create(grade['student_id'], grade['course_id'], letter_grade)
        student = Student.get(grade['student_id'])
        course = Course.get(grade['course_id'])
        
        if student and course:
            flash(f'Grade updated to {letter_grade} for {student["name"]} in {course["code"]}!', 'success')
        else:
            flash('Grade updated successfully!', 'success')
        return redirect(url_for('grades'))
        
    except Exception as e:
        flash(f'Error updating grade: {str(e)}', 'danger')
        return redirect(url_for('edit_grade', grade_id=grade_id))

@app.route('/grades/<int:grade_id>/delete', methods=['POST'])
def delete_grade(grade_id):
    """Delete a grade"""
    try:
        grade = Grade.get(grade_id)
        if not grade:
            flash('Grade not found.', 'danger')
        elif Grade.delete(grade_id):
            flash('Grade deleted successfully!', 'success')
        else:
            flash('Error deleting grade.', 'danger')
    except Exception as e:
        flash(f'Error deleting grade: {str(e)}', 'danger')
    
    return redirect(url_for('grades'))

# Reports Routes
@app.route('/reports')
def reports():
    """Show reports dashboard"""
    students_list = Student.get_all()
    courses_list = Course.get_all()
    enrollments_list = Enrollment.get_all()
    grades_list = Grade.get_all()
    
    # Calculate additional statistics
    total_credits = sum(course['credits'] for course in courses_list)
    avg_gpa = 0.0
    
    if students_list:
        gpas = [Student.calculate_gpa(student['id']) for student in students_list]
        gpas = [gpa for gpa in gpas if gpa > 0]  # Filter out 0.0 GPAs (no grades)
        if gpas:
            avg_gpa = round(sum(gpas) / len(gpas), 2)
    
    # Course enrollment stats
    course_stats = []
    for course in courses_list:
        enrollments = Enrollment.get_by_course(course['id'])
        grades = Grade.get_by_course(course['id'])
        
        course_stats.append({
            'course': course,
            'enrollments': len(enrollments),
            'grades_assigned': len(grades)
        })
    
    # Student performance stats
    student_stats = []
    for student in students_list:
        enrollments = Enrollment.get_by_student(student['id'])
        grades = Grade.get_by_student(student['id'])
        gpa = Student.calculate_gpa(student['id'])
        
        student_stats.append({
            'student': student,
            'enrollments': len(enrollments),
            'grades_received': len(grades),
            'gpa': gpa
        })
    
    stats = {
        'total_students': len(students_list),
        'total_courses': len(courses_list),
        'total_enrollments': len(enrollments_list),
        'total_grades': len(grades_list),
        'total_credits': total_credits,
        'average_gpa': avg_gpa
    }
    
    return render_template('reports.html', 
                         stats=stats,
                         course_stats=course_stats,
                         student_stats=student_stats)

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('base.html', 
                         page_title='Page Not Found',
                         content='<div class="text-center"><h1>404</h1><p>The page you are looking for does not exist.</p></div>'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('base.html', 
                         page_title='Internal Server Error',
                         content='<div class="text-center"><h1>500</h1><p>An internal server error occurred.</p></div>'), 500

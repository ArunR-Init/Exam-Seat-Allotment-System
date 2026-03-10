#!/usr/bin/env python3
"""
Test script to verify Django backend functionality.
Tests all API endpoints and business logic.
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000/api"
session = requests.Session()

def print_test(name):
    """Print test name."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)

def print_result(success, message):
    """Print test result."""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {message}")

def test_health_check():
    """Test if server is running."""
    print_test("Health Check")
    try:
        response = session.get(f"{BASE_URL}/auth/me")
        success = response.status_code == 200
        print_result(success, f"Server responded with status {response.status_code}")
        return success
    except Exception as e:
        print_result(False, f"Server not reachable: {e}")
        return False

def test_student_registration():
    """Test student registration."""
    print_test("Student Registration")
    
    data = {
        "username": "TEST_S001",
        "name": "Test Student",
        "password": "testpass123",
        "confirmPassword": "testpass123"
    }
    
    response = session.post(f"{BASE_URL}/auth/register-student", json=data)
    
    if response.status_code == 201:
        result = response.json()
        success = (
            result['username'] == data['username'] and
            result['name'] == data['name'] and
            result['role'] == 'student'
        )
        print_result(success, f"Student registered: {result}")
        return success
    else:
        print_result(False, f"Registration failed: {response.status_code} - {response.text}")
        return False

def test_duplicate_registration():
    """Test duplicate registration prevention."""
    print_test("Duplicate Registration Prevention")
    
    data = {
        "username": "TEST_S001",  # Same as above
        "name": "Duplicate Student",
        "password": "testpass123",
        "confirmPassword": "testpass123"
    }
    
    response = session.post(f"{BASE_URL}/auth/register-student", json=data)
    success = response.status_code == 400
    
    if success:
        result = response.json()
        print_result(success, f"Correctly rejected duplicate: {result.get('message')}")
    else:
        print_result(False, f"Should have rejected duplicate but got: {response.status_code}")
    
    return success

def test_password_mismatch():
    """Test password confirmation validation."""
    print_test("Password Mismatch Validation")
    
    data = {
        "username": "TEST_S002",
        "name": "Test Student 2",
        "password": "testpass123",
        "confirmPassword": "different"
    }
    
    response = session.post(f"{BASE_URL}/auth/register-student", json=data)
    success = response.status_code == 400
    
    if success:
        result = response.json()
        print_result(success, f"Correctly rejected mismatched passwords: {result.get('message')}")
    else:
        print_result(False, f"Should have rejected mismatched passwords but got: {response.status_code}")
    
    return success

def test_admin_login():
    """Test admin login."""
    print_test("Admin Login")
    
    data = {
        "username": "admin",
        "password": "adminpassword",
        "role": "admin"
    }
    
    response = session.post(f"{BASE_URL}/auth/login", json=data)
    
    if response.status_code == 200:
        result = response.json()
        success = result['role'] == 'admin'
        print_result(success, f"Admin logged in: {result}")
        return success
    else:
        print_result(False, f"Login failed: {response.status_code} - {response.text}")
        return False

def test_wrong_role_login():
    """Test login with wrong role."""
    print_test("Wrong Role Login Prevention")
    
    data = {
        "username": "admin",
        "password": "adminpassword",
        "role": "student"  # Wrong role
    }
    
    response = session.post(f"{BASE_URL}/auth/login", json=data)
    success = response.status_code == 401
    
    if success:
        print_result(success, "Correctly rejected wrong role login")
    else:
        print_result(False, f"Should have rejected wrong role but got: {response.status_code}")
    
    return success

def test_get_current_user():
    """Test getting current user."""
    print_test("Get Current User")
    
    response = session.get(f"{BASE_URL}/auth/me")
    
    if response.status_code == 200:
        result = response.json()
        success = result['username'] == 'admin' and result['role'] == 'admin'
        print_result(success, f"Current user: {result}")
        return success
    else:
        print_result(False, f"Failed to get current user: {response.status_code}")
        return False

def test_add_teacher():
    """Test adding a teacher."""
    print_test("Add Teacher (Admin)")
    
    data = {
        "username": "TEST_T001",
        "name": "Test Teacher",
        "password": "teacherpass123"
    }
    
    response = session.post(f"{BASE_URL}/admin/teachers", json=data)
    
    if response.status_code == 201:
        result = response.json()
        success = (
            result['username'] == data['username'] and
            result['role'] == 'teacher'
        )
        print_result(success, f"Teacher added: {result}")
        return success
    else:
        print_result(False, f"Failed to add teacher: {response.status_code} - {response.text}")
        return False

def test_get_students():
    """Test getting all students."""
    print_test("Get All Students (Admin)")
    
    response = session.get(f"{BASE_URL}/admin/students")
    
    if response.status_code == 200:
        result = response.json()
        success = isinstance(result, list)
        print_result(success, f"Retrieved {len(result)} students")
        return success
    else:
        print_result(False, f"Failed to get students: {response.status_code}")
        return False

def test_get_teachers():
    """Test getting all teachers."""
    print_test("Get All Teachers (Admin)")
    
    response = session.get(f"{BASE_URL}/admin/teachers")
    
    if response.status_code == 200:
        result = response.json()
        success = isinstance(result, list)
        print_result(success, f"Retrieved {len(result)} teachers")
        return success
    else:
        print_result(False, f"Failed to get teachers: {response.status_code}")
        return False

def test_allotment():
    """Test room allotment."""
    print_test("Room Allotment (Admin)")
    
    response = session.post(f"{BASE_URL}/admin/allot")
    
    if response.status_code == 200:
        result = response.json()
        success = (
            'roomsCreated' in result and
            'studentsAllotted' in result
        )
        print_result(success, f"Allotment: {result}")
        return success
    else:
        error = response.json()
        print_result(False, f"Allotment failed: {error.get('message', response.text)}")
        return False

def test_student_login():
    """Test student login."""
    print_test("Student Login")
    
    data = {
        "username": "TEST_S001",
        "password": "testpass123",
        "role": "student"
    }
    
    response = session.post(f"{BASE_URL}/auth/login", json=data)
    
    if response.status_code == 200:
        result = response.json()
        success = result['role'] == 'student'
        print_result(success, f"Student logged in: {result}")
        return success
    else:
        print_result(False, f"Login failed: {response.status_code}")
        return False

def test_student_allotment():
    """Test student viewing their allotment."""
    print_test("Student View Allotment")
    
    response = session.get(f"{BASE_URL}/student/allotment")
    
    if response.status_code == 200:
        result = response.json()
        if result is None:
            print_result(True, "Student not yet allotted (expected)")
            return True
        else:
            success = 'room' in result and 'allotment' in result
            print_result(success, f"Allotment details: {result}")
            return success
    else:
        print_result(False, f"Failed to get allotment: {response.status_code}")
        return False

def test_teacher_login():
    """Test teacher login."""
    print_test("Teacher Login")
    
    data = {
        "username": "TEST_T001",
        "password": "teacherpass123",
        "role": "teacher"
    }
    
    response = session.post(f"{BASE_URL}/auth/login", json=data)
    
    if response.status_code == 200:
        result = response.json()
        success = result['role'] == 'teacher'
        print_result(success, f"Teacher logged in: {result}")
        return success
    else:
        print_result(False, f"Login failed: {response.status_code}")
        return False

def test_teacher_room():
    """Test teacher viewing their room."""
    print_test("Teacher View Room")
    
    response = session.get(f"{BASE_URL}/teacher/room")
    
    if response.status_code == 200:
        result = response.json()
        if result is None:
            print_result(True, "Teacher not yet assigned (expected)")
            return True
        else:
            success = 'room' in result and 'students' in result
            print_result(success, f"Room details: {json.dumps(result, indent=2)}")
            return success
    else:
        print_result(False, f"Failed to get room: {response.status_code}")
        return False

def test_logout():
    """Test logout."""
    print_test("Logout")
    
    response = session.post(f"{BASE_URL}/auth/logout")
    success = response.status_code == 200
    
    print_result(success, "Logged out successfully" if success else "Logout failed")
    return success

def test_unauthorized_access():
    """Test accessing protected endpoint without auth."""
    print_test("Unauthorized Access Prevention")
    
    response = session.get(f"{BASE_URL}/admin/students")
    success = response.status_code == 401
    
    print_result(success, "Correctly rejected unauthorized access" if success else f"Should have rejected but got: {response.status_code}")
    return success

def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("DJANGO BACKEND TEST SUITE")
    print("="*60)
    print(f"Testing: {BASE_URL}")
    
    tests = [
        test_health_check,
        test_student_registration,
        test_duplicate_registration,
        test_password_mismatch,
        test_admin_login,
        test_wrong_role_login,
        test_get_current_user,
        test_add_teacher,
        test_get_students,
        test_get_teachers,
        test_allotment,
        test_student_login,
        test_student_allotment,
        test_teacher_login,
        test_teacher_room,
        test_logout,
        test_unauthorized_access,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print_result(False, f"Test crashed: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total:  {passed + failed}")
    print(f"📈 Success Rate: {(passed / (passed + failed) * 100):.1f}%")
    print("="*60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

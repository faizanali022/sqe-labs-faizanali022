"""Existing LMS authentication tests."""
import auth

def test_valid_login_with_correct_credentials():
    result = auth.validate_login("student@uni.edu", "ValidPass1")
    assert result["success"] is True
    assert result["user_id"] == "STU-001"

def test_account_lockout_after_3_failed_attempts():
    assert auth.check_lockout("student@uni.edu", attempt_count=3) is False
    assert auth.is_locked("student@uni.edu") is True

def test_password_reset_email_send():
    result = auth.send_reset_email("student@uni.edu")
    assert result["sent"] is True

def test_session_expires_after_30_min():
    auth.create_session("student@uni.edu", idle_minutes=31)
    assert auth.is_session_valid("student@uni.edu") is False

def test_login_requests_empty_password():
    result = auth.validate_login("student@uni.edu", "")
    assert result["success"] is False
    assert result["error"] == "Email and password are required"

def test_login_requests_invalid_email_format():
    result = auth.validate_login("student-at-uni.edu", "ValidPass1")
    assert result["success"] is False
    assert result["error"] == "Invalid email format"

def test_login_requests_wrong_password():
    result = auth.validate_login("student@uni.edu", "WrongPass9")
    assert result["success"] is False
    assert result["error"] == "Invalid credentials"
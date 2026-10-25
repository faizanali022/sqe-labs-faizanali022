"""New tests added in Lab 7 to cover baseline gaps."""

import auth


# Target: verify_reset_token() valid token returns True
def test_verify_reset_token_accepts_valid_token():
    token = auth.generate_reset_token("student@uni.edu")
    assert auth.verify_reset_token(token) is True


# Target: verify_reset_token() unknown token returns False
def test_verify_reset_token_rejects_unknown_token():
    assert auth.verify_reset_token("no-such-token") is False


# Target: verify_reset_token() expired token returns False
def test_verify_reset_token_rejects_expired_token():
    token = auth.generate_reset_token(
        "student@uni.edu", hours_ago=2
    )
    assert auth.verify_reset_token(token) is False


# Target: verify_reset_token() used token returns False
def test_verify_reset_token_rejects_used_token():
    token = auth.generate_reset_token("student@uni.edu")
    auth.mark_token_used(token)
    assert auth.verify_reset_token(token) is False


# Target: check_lockout() locked account returns False
def test_check_lockout_blocks_already_locked_account():
    auth.lock_account("student@uni.edu")
    assert auth.check_lockout(
        "student@uni.edu", attempt_count=0
    ) is False


# Target: check_lockout() fewer than three attempts returns True
def test_check_lockout_allows_two_failed_attempts():
    assert auth.check_lockout(
        "student@uni.edu", attempt_count=2
    ) is True
    assert auth.is_locked("student@uni.edu") is False


# Target: check_lockout() unknown user returns False
def test_check_lockout_blocks_unknown_account_at_three_attempts():
    assert auth.check_lockout(
        "nobody@uni.edu", attempt_count=3
    ) is False


# Target: validate_login() unregistered email is rejected
def test_validate_login_rejects_unregistered_email():
    result = auth.validate_login(
        "ghost@uni.edu", "ValidPass1"
    )
    assert result["success"] is False
    assert result["user_id"] is None
    assert result["error"] == "Invalid credentials"


# Target: validate_login() locked account is refused
def test_validate_login_refuses_locked_account():
    auth.lock_account("student@uni.edu")
    result = auth.validate_login(
        "student@uni.edu", "ValidPass1"
    )
    assert result["success"] is False
    assert result["error"] == "Account is locked"


# Target: validate_login() three wrong passwords lock account
def test_validate_login_locks_account_after_three_wrong_passwords():
    for _ in range(3):
        auth.validate_login(
            "student@uni.edu", "WrongPass9"
        )
    assert auth.is_locked("student@uni.edu") is True
    # Target: is_session_valid() returns False when no session exists
def test_session_invalid_when_no_session_exists():
    assert auth.is_session_valid("STU-001") is False


# Target: is_session_valid() returns True for a valid session
def test_session_valid_when_session_exists():
    auth.create_session("STU-001")
    assert auth.is_session_valid("STU-001") is True


# Target: destroy_session() removes an existing session
def test_destroy_session_removes_session():
    auth.create_session("STU-001")
    auth.destroy_session("STU-001")
    assert auth.is_session_valid("STU-001") is False


# Target: handle_session() handles a user with no session
def test_handle_session_without_existing_session():
    result = auth.handle_session("STU-001")
    assert result is True

# Target: update_session_activity() updates an existing session
def test_update_session_activity():
    auth.create_session("STU-001")
    result = auth.update_session_activity("STU-001")
    assert result is None
    
from unittest.mock import patch


# Target: unlock_account() unlocks account and resets attempts
def test_unlock_account_resets_attempts():
    auth.lock_account("student@uni.edu")
    auth.unlock_account("student@uni.edu")
    assert auth.is_locked("student@uni.edu") is False
    assert auth.auth_store.users["student@uni.edu"]["attempt_count"] == 0


# Target: is_locked() returns False for an unknown account
def test_is_locked_unknown_account():
    assert auth.is_locked("unknown@uni.edu") is False


# Target: reset_attempt_count() resets failed attempts
def test_reset_attempt_count():
    auth.validate_login("student@uni.edu", "WrongPass9")
    auth.reset_attempt_count("student@uni.edu")
    assert auth.auth_store.users["student@uni.edu"]["attempt_count"] == 0


# Target: is_session_valid() rejects an expired session
def test_expired_session_is_invalid():
    auth.create_session("STU-001", idle_minutes=31)
    assert auth.is_session_valid("STU-001") is False


# Target: handle_session() rejects an expired existing session
def test_handle_session_rejects_expired_session():
    auth.create_session("STU-001", idle_minutes=31)
    assert auth.handle_session("STU-001") is False


# Target: mark_token_used() marks an existing token as used
def test_mark_token_used():
    token = auth.generate_reset_token("student@uni.edu")
    auth.mark_token_used(token)
    assert auth.verify_reset_token(token) is False


# Target: send_reset_email() rejects an unknown email
def test_send_reset_email_unknown_email():
    result = auth.send_reset_email("unknown@uni.edu")
    assert result["sent"] is False
    assert result["error"] == "Email address not found"


# Target: send_reset_email() rejects email after rate limit
def test_send_reset_email_rate_limit():
    auth.auth_store.reset_email_attempts["student@uni.edu"] = auth.MAX_RESET_EMAILS
    result = auth.send_reset_email("student@uni.edu")
    assert result["sent"] is False
    assert result["error"] == "Rate limit exceeded"


# Target: send_reset_email() handles token generation failure
def test_send_reset_email_token_generation_failure():
    with patch("auth.generate_reset_token", side_effect=Exception("test error")):
        result = auth.send_reset_email("student@uni.edu")
    assert result["sent"] is False
    assert "Token generation failed" in result["error"]


# Target: send_reset_email() handles SMTP connection failure
def test_send_reset_email_smtp_failure():
    with patch("auth._deliver_email", side_effect=ConnectionError("connection failed")):
        result = auth.send_reset_email("student@uni.edu")
    assert result["sent"] is False
    assert "SMTP error" in result["error"]

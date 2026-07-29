import sys
import os

# Ensure backend root is on sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.utils.sanitizer import PIISanitizer

def test_email_sanitization():
    raw_text = "Looking for UI/UX designer. Reach out to hr_manager@company.com or recruiter.test@gmail.co.in."
    sanitized = PIISanitizer.sanitize_text(raw_text)

    assert "hr_manager@company.com" not in sanitized
    assert "recruiter.test@gmail.co.in" not in sanitized
    assert "[Contact Via Application Link]" in sanitized
    print("[PASS] Email sanitization test passed")


def test_indian_phone_sanitization():
    raw_text = "Call hiring team at +91 9876543210 or 9876543210 for immediate interview."
    sanitized = PIISanitizer.sanitize_text(raw_text)

    assert "+91 9876543210" not in sanitized
    assert "9876543210" not in sanitized
    assert "[Contact Via Application Link]" in sanitized
    print("[PASS] Indian phone sanitization test passed")

def test_clean_text_unchanged():
    raw_text = "Hiring Senior Product Designer in Bengaluru. Figma knowledge required."
    sanitized = PIISanitizer.sanitize_text(raw_text)

    assert sanitized == raw_text
    print("[PASS] Clean text test passed")


if __name__ == "__main__":
    test_email_sanitization()
    test_indian_phone_sanitization()
    test_clean_text_unchanged()
    print("\nAll DPDP PII Sanitizer tests passed successfully!")

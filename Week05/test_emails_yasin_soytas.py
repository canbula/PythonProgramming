import pytest
from emails_yasin_soytas import Emails


def test_class_exists():
    assert Emails is not None


def test_is_subclass_of_list():
    assert issubclass(Emails, list)


def test_empty_constructor():
    e = Emails()
    assert isinstance(e, list)
    assert len(e) == 0


def test_valid_emails_added():
    emails = Emails(["test@example.com", "user@mail.com"])
    assert "test@example.com" in emails
    assert "user@mail.com" in emails
    assert len(emails) == 2


def test_emails_lowercase():
    emails = Emails(["TEST@EXAMPLE.COM"])
    assert "test@example.com" in emails


def test_no_duplicates():
    emails = Emails(["test@example.com", "TEST@EXAMPLE.COM"])
    assert len(emails) == 1


def test_invalid_emails_not_added():
    emails = Emails(["testexample.com", 123, None, "hello"])
    assert len(emails) == 0


def test_mixed_input():
    emails = Emails([
        "A@A.COM",
        "b@b.com",
        "invalid",
        42,
        "a@a.com"
    ])
    assert emails == ["a@a.com", "b@b.com"]



def test_instance_type():
    emails = Emails(["x@y.com"])
    assert isinstance(emails, Emails)

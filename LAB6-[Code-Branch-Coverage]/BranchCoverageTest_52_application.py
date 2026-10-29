
import pytest

from visa_application import (
    visa_fee,
    documents_complete,
    application_status,
)


@pytest.mark.parametrize(
    "visa_type,entries,speed,group,expected",
    [
        ("tourist", 1, "normal", "B", 0),
        ("tourist", 2, "normal", "B", 40),
        ("tourist", 2, "express", "B", 100),
        ("tourist", 2, "normal", "A", 0),
        ("student", 3, "normal", "A", 40),
        ("business", 4, "normal", "B", 40),
        ("tourist", 7, "normal", "B", 360),
        ("tourist", 7, "express", "B", 780),
    ],
)
def test_visa_fee_branches(
    visa_type, entries, speed, group, expected
):
    assert visa_fee(visa_type, entries, speed, group) == expected


@pytest.mark.parametrize(
    "visa_type,entries,message",
    [
        ("unknown", 1, "unknown visa type"),
        ("tourist", -1, "invalid entries"),
    ],
)
def test_visa_fee_errors(visa_type, entries, message):
    with pytest.raises(ValueError, match=message):
        visa_fee(visa_type, entries, "normal", "B")


@pytest.mark.parametrize(
    "forms,photos,renewal,expected",
    [
        (1, 0, True, True),
        (0, 5, True, False),
        (3, 2, False, True),
        (2, 2, False, False),
        (3, 1, False, False),
        (3, 3, False, True),
    ],
)
def test_document_branches(forms, photos, renewal, expected):
    assert documents_complete(forms, photos, renewal) is expected


@pytest.mark.parametrize(
    "days,express,peak,expected",
    [
        (30, False, False, "open"),
        (29, False, False, "closing"),
        (14, False, False, "closed"),
        (10, True, False, "open"),
        (9, True, False, "closing"),
        (-6, True, False, "closed"),
        (45, False, True, "open"),
        (30, False, True, "closing"),
        (29, False, True, "closed"),
        (25, True, True, "open"),
        (10, True, True, "closing"),
        (9, True, True, "closed"),
    ],
)
def test_application_status_branches(days, express, peak, expected):
    assert application_status(days, express, peak) == expected

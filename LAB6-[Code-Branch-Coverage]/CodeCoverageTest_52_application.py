import pytest

from visa_application import (
    visa_fee,
    documents_complete,
    application_status,
)


# --------------------------------------------------
# VISA FEE TESTS
# --------------------------------------------------

def test_within_included_entries():
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_unknown_visa_type():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("work", 1, "normal", "B")


def test_negative_entries():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_nationality_group_a_extra_included_entry():
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_student_does_not_get_group_a_extra_entry():
    assert visa_fee("student", 3, "normal", "A") == 40


def test_normal_speed_extra_entry():
    assert visa_fee("tourist", 2, "normal", "B") == 40


def test_express_speed_extra_entry():
    assert visa_fee("tourist", 2, "express", "B") == 100


def test_more_than_five_extra_entries_normal():
    assert visa_fee("tourist", 7, "normal", "B") == 360


def test_more_than_five_extra_entries_express():
    assert visa_fee("tourist", 7, "express", "B") == 780


# --------------------------------------------------
# DOCUMENT COMPLETENESS TESTS
# --------------------------------------------------

def test_complete_regular_application():
    assert documents_complete(3, 2, False) is True


def test_regular_application_with_too_few_forms():
    assert documents_complete(2, 2, False) is False


def test_regular_application_with_too_few_photos():
    assert documents_complete(3, 1, False) is False


def test_renewal_with_at_least_one_form():
    assert documents_complete(1, 0, True) is True


def test_renewal_without_forms():
    assert documents_complete(0, 5, True) is False


# --------------------------------------------------
# APPLICATION STATUS TESTS
# --------------------------------------------------

def test_normal_non_peak_open():
    assert application_status(30, False, False) == "open"


def test_normal_non_peak_closing():
    assert application_status(29, False, False) == "closing"


def test_normal_non_peak_closed():
    assert application_status(14, False, False) == "closed"


def test_express_non_peak_open():
    assert application_status(10, True, False) == "open"


def test_peak_season_open():
    assert application_status(45, False, True) == "open"


def test_peak_season_closing():
    assert application_status(30, False, True) == "closing"


def test_express_peak_season_closed():
    assert application_status(9, True, True) == "closed"

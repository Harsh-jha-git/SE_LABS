import pytest
from self_storage import rent_due, access_allowed, payment_status


def test_within_deposit_months():
    assert rent_due("small", 1, False, False) == 0


def test_unknown_unit_size():
    with pytest.raises(ValueError):
        rent_due("huge", 1, False, False)


def test_negative_months():
    with pytest.raises(ValueError):
        rent_due("small", -1, False, False)


def test_member_climate_long_stay():
    # member small -> covered 2, extra 8, climate: (120 - 10 - 5) * 8
    assert rent_due("small", 10, True, True) == 840


def test_access_allowed():
    assert access_allowed(12, 1, False) is True


def test_access_owner():
    assert access_allowed(3, 4, True) is True


def test_access_off_hours():
    assert access_allowed(3, 1, False) is False


def test_payment_current():
    assert payment_status(10, False, False) == "current"


def test_payment_grace():
    assert payment_status(2, False, False) == "grace"


def test_payment_lien():
    assert payment_status(-20, False, True) == "lien"

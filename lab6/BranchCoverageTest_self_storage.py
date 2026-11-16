import pytest
from self_storage import rent_due, access_allowed, payment_status


# ---------- rent_due ----------
def test_within_deposit_months():
    assert rent_due("small", 1, False, False) == 0


def test_unknown_unit_size():
    with pytest.raises(ValueError):
        rent_due("huge", 1, False, False)


def test_negative_months():
    with pytest.raises(ValueError):
        rent_due("small", -1, False, False)


def test_member_gets_extra_covered_month():
    assert rent_due("medium", 3, False, True) == 0


def test_large_member_no_bonus_month():
    assert rent_due("large", 4, False, True) == 80


def test_non_member_non_climate_rate():
    assert rent_due("small", 2, False, False) == 80


def test_climate_rate():
    assert rent_due("small", 2, True, False) == 120


def test_long_stay_boundary_not_discounted():
    # extra == 6 -> no discount
    assert rent_due("small", 8, False, True) == 480


def test_long_stay_non_climate_discount():
    assert rent_due("small", 8, False, False) == 7 * 70


def test_long_stay_climate_discount():
    assert rent_due("small", 8, True, False) == 7 * 105


# ---------- access_allowed ----------
def test_access_owner_ok():
    assert access_allowed(3, 4, True) is True


def test_access_owner_too_many():
    assert access_allowed(12, 5, True) is False


def test_access_too_early():
    assert access_allowed(5, 1, False) is False


def test_access_too_late():
    assert access_allowed(23, 1, False) is False


def test_access_normal_hours_ok():
    assert access_allowed(12, 2, False) is True


def test_access_hour_boundaries_ok():
    assert access_allowed(6, 1, False) is True
    assert access_allowed(22, 1, False) is True


def test_access_too_many_visitors():
    assert access_allowed(12, 3, False) is False


# ---------- payment_status ----------
def test_payment_current_manual():
    assert payment_status(5, False, False) == "current"


def test_payment_current_autopay():
    assert payment_status(0, True, False) == "current"


def test_payment_grace_manual():
    assert payment_status(4, False, False) == "grace"


def test_payment_grace_boundary():
    assert payment_status(-10, False, False) == "grace"


def test_payment_lien():
    assert payment_status(-11, False, False) == "lien"


def test_payment_prior_late_raises_cutoff():
    assert payment_status(10, True, True) == "current"
    assert payment_status(9, True, True) == "grace"

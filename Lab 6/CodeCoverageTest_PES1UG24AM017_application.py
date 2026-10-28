import pytest
from electricity_bill import energy_charge, late_fee, subsidy


# ---------- energy_charge ----------
def test_low_usage_domestic():
    assert energy_charge(50, "domestic") == 200

def test_mid_usage_domestic():
    assert energy_charge(200, "domestic") == 850

def test_high_usage_domestic():
    assert energy_charge(400, "domestic") == 2150

def test_low_usage_commercial():
    assert energy_charge(50, "commercial") == 450

def test_unknown_connection():
    with pytest.raises(ValueError):
        energy_charge(10, "industrial")

def test_negative_units():
    with pytest.raises(ValueError):
        energy_charge(-1, "domestic")


# ---------- late_fee ----------
def test_paid_on_time():
    assert late_fee(500, 0) == 0

def test_late_within_15_days():
    assert late_fee(500, 10) == 50

def test_late_over_15_days_small_bill():
    assert late_fee(1000, 20) == 100

def test_late_over_15_days_large_bill():
    assert late_fee(4000, 20) == 300


# ---------- subsidy ----------
def test_senior_low_usage():
    assert subsidy(50, True, False) == 50

def test_solar_only():
    assert subsidy(150, False, True) == 100

def test_solar_high_usage_cancels_subsidy():
    assert subsidy(400, True, True) == 0
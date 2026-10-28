import pytest
from electricity_bill import energy_charge, late_fee, subsidy


# ---------- energy_charge: validation branches ----------
def test_unknown_connection():
    with pytest.raises(ValueError):
        energy_charge(10, "industrial")

def test_negative_units():
    with pytest.raises(ValueError):
        energy_charge(-1, "domestic")

def test_zero_units():
    assert energy_charge(0, "domestic") == 50


# ---------- energy_charge: slab boundaries ----------
def test_slab1_upper_boundary():
    assert energy_charge(100, "domestic") == 350

def test_slab2_lower_boundary():
    assert energy_charge(101, "domestic") == 355

def test_slab2_upper_boundary():
    assert energy_charge(300, "domestic") == 1350

def test_slab3_lower_boundary():
    assert energy_charge(301, "domestic") == 1358

def test_low_usage_domestic():
    assert energy_charge(50, "domestic") == 200


# ---------- energy_charge: connection type branch ----------
def test_commercial_slab1():
    assert energy_charge(50, "commercial") == 450

def test_commercial_slab2():
    assert energy_charge(200, "commercial") == 1750

def test_commercial_slab3():
    assert energy_charge(400, "commercial") == 4350

def test_domestic_slab3_no_doubling():
    assert energy_charge(400, "domestic") == 2150


# ---------- late_fee ----------
def test_paid_on_time():
    assert late_fee(500, 0) == 0

def test_negative_days_late():
    assert late_fee(500, -5) == 0

def test_late_one_day():
    assert late_fee(500, 1) == 50

def test_late_15_days_boundary():
    assert late_fee(500, 15) == 50

def test_late_16_days_boundary_small_bill():
    assert late_fee(500, 16) == 100

def test_late_bill_exactly_2000():
    assert late_fee(2000, 16) == 100

def test_late_bill_just_over_2000():
    assert late_fee(2001, 16) == 200

def test_late_large_bill():
    assert late_fee(4000, 20) == 300


# ---------- subsidy: senior branch ----------
def test_senior_low_usage():
    assert subsidy(50, True, False) == 50

def test_senior_100_units_boundary():
    assert subsidy(100, True, False) == 50

def test_senior_just_over_100_units():
    assert subsidy(101, True, False) == 0

def test_not_senior_low_usage():
    assert subsidy(50, False, False) == 0

def test_senior_high_usage():
    assert subsidy(150, True, False) == 0


# ---------- subsidy: solar branch ----------
def test_solar_only_low_usage():
    assert subsidy(150, False, True) == 100

def test_solar_300_units_boundary():
    assert subsidy(300, False, True) == 100

def test_solar_over_300_units_cancels():
    assert subsidy(301, False, True) == 0

def test_senior_and_solar_low_usage():
    assert subsidy(50, True, True) == 150

def test_senior_and_solar_high_usage():
    assert subsidy(400, True, True) == 0

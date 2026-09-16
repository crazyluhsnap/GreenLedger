from app.sector import get_sector_adjustment


def test_manufacturing_fossil_fuel_has_higher_environmental_impact():
    adjustment = get_sector_adjustment(
        "MANUFACTURING",
        "FOSSIL_FUEL",
    )

    assert adjustment["environmental"] == 1.25


def test_energy_fossil_fuel_has_high_environmental_impact():
    adjustment = get_sector_adjustment(
        "ENERGY",
        "FOSSIL_FUEL",
    )

    assert adjustment["environmental"] == 1.5


def test_financial_services_compliance_has_governance_relevance():
    adjustment = get_sector_adjustment(
        "FINANCIAL_SERVICES",
        "COMPLIANCE",
    )

    assert adjustment["governance"] == 1.25


def test_unknown_sector_uses_neutral_adjustment():
    adjustment = get_sector_adjustment(
        "UNKNOWN",
        "FOSSIL_FUEL",
    )

    assert adjustment == {
        "environmental": 1.0,
        "social": 1.0,
        "governance": 1.0,
    }
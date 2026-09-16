from app.scoring import calculate_esg_score


def test_positive_environmental_transaction():
    result = calculate_esg_score(
        "Solar panel procurement",
        "MANUFACTURING",
    )

    assert result["environmental_score"] > 50
    assert result["overall_score"] > 50
    assert "RENEWABLE_ENERGY" in result["signals"]


def test_fossil_fuel_transaction_reduces_environmental_score():
    result = calculate_esg_score(
        "Diesel transportation",
        "MANUFACTURING",
    )

    assert result["environmental_score"] < 50
    assert "FOSSIL_FUEL" in result["signals"]


def test_employee_welfare_improves_social_score():
    result = calculate_esg_score(
        "Employee safety training",
        "MANUFACTURING",
    )

    assert result["social_score"] > 50
    assert "EMPLOYEE_WELFARE" in result["signals"]


def test_corruption_reduces_governance_score():
    result = calculate_esg_score(
        "Government official bribery payment",
        "MANUFACTURING",
    )

    assert result["governance_score"] < 50
    assert "CORRUPTION" in result["signals"]


def test_unknown_transaction_is_neutral():
    result = calculate_esg_score(
        "Office stationery purchase",
        "MANUFACTURING",
    )

    assert result["environmental_score"] == 50
    assert result["social_score"] == 50
    assert result["governance_score"] == 50
    assert result["overall_score"] == 50
    
    
def test_scoring_supports_unseen_nlp_wording():
    result = calculate_esg_score(
        "Installation of photovoltaic generation equipment",
        "MANUFACTURING",
    )

    assert result["environmental_score"] > 50
    assert "RENEWABLE_ENERGY" in result["signals"]
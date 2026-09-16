from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


TRAINING_DATA = [
    # Renewable energy
    (
        "solar panel procurement",
        "RENEWABLE_ENERGY",
    ),
    (
        "solar power installation",
        "RENEWABLE_ENERGY",
    ),
    (
        "wind energy equipment",
        "RENEWABLE_ENERGY",
    ),
    (
        "wind power installation",
        "RENEWABLE_ENERGY",
    ),
    (
        "renewable energy installation",
        "RENEWABLE_ENERGY",
    ),
    (
        "photovoltaic power equipment",
        "RENEWABLE_ENERGY",
    ),
    (
        "clean energy infrastructure",
        "RENEWABLE_ENERGY",
    ),
    (
        "green energy project",
        "RENEWABLE_ENERGY",
    ),
    
    (
    "photovoltaic generation equipment",
    "RENEWABLE_ENERGY",
    ),
    (
    "photovoltaic generation system",
    "RENEWABLE_ENERGY",
    ),
    (
    "installation of photovoltaic equipment",
    "RENEWABLE_ENERGY",
    ),
    (
    "photovoltaic solar generation",
    "RENEWABLE_ENERGY",
    ),
    (
    "clean electricity generation equipment",
    "RENEWABLE_ENERGY",
    ),
    

    # Fossil fuel
    (
        "diesel fuel procurement",
        "FOSSIL_FUEL",
    ),
    (
        "diesel transportation expense",
        "FOSSIL_FUEL",
    ),
    (
        "petrol purchase",
        "FOSSIL_FUEL",
    ),
    (
        "petroleum fuel procurement",
        "FOSSIL_FUEL",
    ),
    (
        "coal transportation",
        "FOSSIL_FUEL",
    ),
    (
        "coal procurement",
        "FOSSIL_FUEL",
    ),
    (
        "gasoline fuel expense",
        "FOSSIL_FUEL",
    ),
    (
        "conventional fuel purchase",
        "FOSSIL_FUEL",
    ),
    
    (
    "petroleum products",
    "FOSSIL_FUEL",
    ),
    (
    "petroleum procurement",
    "FOSSIL_FUEL",
    ),
    (
    "petroleum products for vehicles",
    "FOSSIL_FUEL",
    ),
    (
    "petroleum based fuel",
    "FOSSIL_FUEL",
    ),

    # Employee welfare
    (
        "employee safety training",
        "EMPLOYEE_WELFARE",
    ),
    (
        "worker welfare program",
        "EMPLOYEE_WELFARE",
    ),
    (
        "employee health insurance",
        "EMPLOYEE_WELFARE",
    ),
    (
        "workplace safety program",
        "EMPLOYEE_WELFARE",
    ),
    (
        "employee development program",
        "EMPLOYEE_WELFARE",
    ),

    # Labor risk
    (
        "child labor violation",
        "LABOR_RISK",
    ),
    (
        "forced labor investigation",
        "LABOR_RISK",
    ),
    (
        "unsafe working conditions",
        "LABOR_RISK",
    ),
    (
        "worker exploitation complaint",
        "LABOR_RISK",
    ),

    # Corruption
    (
        "government official bribery",
        "CORRUPTION",
    ),
    (
        "bribe payment",
        "CORRUPTION",
    ),
    (
        "corruption payment",
        "CORRUPTION",
    ),
    (
        "illegal payment to official",
        "CORRUPTION",
    ),
    (
        "improper payment to government official",
        "CORRUPTION",
    ),
]

_texts = [item[0] for item in TRAINING_DATA]
_labels = [item[1] for item in TRAINING_DATA]

_vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
)

_X = _vectorizer.fit_transform(_texts)

_model = LogisticRegression(
    max_iter=1000,
)

_model.fit(_X, _labels)


def classify_with_nlp(description: str) -> dict:
    vector = _vectorizer.transform([description])

    prediction = _model.predict(vector)[0]
    probabilities = _model.predict_proba(vector)[0]

    confidence = float(max(probabilities))

    return {
        "signal": prediction,
        "confidence": confidence,
    }
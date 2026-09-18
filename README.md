# GreenLedger

GreenLedger is an explainable prototype ESG intelligence platform for financial transactions.

It analyzes transaction descriptions and financial activity to infer Environmental, Social, and Governance (ESG) signals, calculate prototype ESG scores, detect anomalies, generate recommendations, produce company-level reports, and provide an evidence-backed RAG assistant.

> **Important:** GreenLedger is a prototype analytics system. Its ESG scores, classifications, anomaly detection, and recommendations are not regulatory, investment, accounting, or professional ESG ratings.

---

## Features

### Transaction Analysis
- Validate financial transaction data with Pydantic.
- Classify transactions into ESG-related signals.
- Detect positive, negative, and neutral ESG impact.
- Calculate Environmental, Social, Governance, and overall scores.
- Apply sector-specific scoring adjustments.

### Hybrid ESG Classification
GreenLedger combines:
- **Rule-based classification** for known ESG keywords and patterns.
- **TF-IDF + Logistic Regression NLP classification** for unseen wording.
- A confidence threshold to avoid accepting low-confidence NLP predictions.

### Anomaly Detection
Detect potentially concerning transactions based on:
- Corruption-related signals.
- Labor-risk signals.
- High-value fossil-fuel transactions.

### Company Analytics
For each company, GreenLedger provides:
- Transaction count and total transaction volume.
- Environmental, Social, Governance, and overall scores.
- Impact distribution.
- Anomaly statistics.
- Monthly ESG trends.
- Key ESG signals.

### Reports
Company reports contain:
- Executive summary.
- ESG scores.
- Transaction and volume statistics.
- Impact distribution.
- Key signals.
- Detected anomalies.
- Recommendations.
- Trend information.

### RAG ESG Assistant
GreenLedger indexes company reports into a vector store and retrieves relevant evidence before generating answers.

The assistant:
- Uses retrieved ESG evidence as context.
- Avoids inventing facts.
- Returns supporting evidence.
- Can answer questions about company ESG performance, trends, signals, anomalies, and recommendations.

### CSV Upload
Users can upload transaction datasets through the dashboard.

The system:
1. Validates the CSV.
2. Converts rows into transaction models.
3. Stores the transactions.
4. Discovers affected companies.
5. Generates company reports.
6. Indexes report chunks for RAG.
7. Makes the companies available through the dashboard selector.

---

## Architecture

```text
                         ┌──────────────────────┐
                         │    Transaction CSV   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Validation / Ingest  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   ESG Classification │
                         │  Rules + NLP Hybrid  │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              ┌──────────┐   ┌────────────┐   ┌─────────────┐
              │ ESG Score│   │  Anomaly   │   │   Trends /  │
              │  Engine  │   │ Detection  │   │   Analysis  │
              └────┬─────┘   └─────┬──────┘   └──────┬──────┘
                   │               │                  │
                   └───────────────┼──────────────────┘
                                   ▼
                         ┌──────────────────────┐
                         │ Company Report Engine│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Report Chunk Indexing│
                         │   Chroma Vector DB   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      RAG Assistant   │
                         │     Groq LLM         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    React Dashboard   │
                         │ Dashboard / Analytics │
                         │ Reports / Assistant   │
                         └──────────────────────┘
```

---

## Project Structure

```text
greenledger/
│
├── backend/
│   ├── app/
│   │   ├── tests/
│   │   ├── analysis.py
│   │   ├── anomaly.py
│   │   ├── assistant.py
│   │   ├── company.py
│   │   ├── csv_loader.py
│   │   ├── embeddings.py
│   │   ├── esg.py
│   │   ├── features.py
│   │   ├── hybrid.py
│   │   ├── indexer.py
│   │   ├── ingestion.py
│   │   ├── llm.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── nlp.py
│   │   ├── portfolio.py
│   │   ├── recommendations.py
│   │   ├── report.py
│   │   ├── report_chunks.py
│   │   ├── risk.py
│   │   ├── scoring.py
│   │   ├── sector.py
│   │   ├── store.py
│   │   ├── trends.py
│   │   ├── vector_store.py
│   │   └── ...
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── services/
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- Pandas
- scikit-learn
- ChromaDB
- Sentence Transformers
- Groq API
- pytest

### Frontend
- React
- Vite
- JavaScript / JSX
- Recharts
- React Markdown
- CSS

---

## ESG Taxonomy

The prototype currently recognizes signals including:

### Environmental
- Renewable energy
- Fossil fuel
- Recycling

### Social
- Employee welfare
- Labor risk

### Governance
- Corruption
- Compliance

Transactions without a recognized signal are classified as `UNCLASSIFIED`.

The taxonomy is implemented as a prototype rule set and should not be interpreted as a complete ESG taxonomy.

---

## Prototype Scoring

GreenLedger starts each ESG dimension at a neutral baseline of `50`.

Signal-specific adjustments are then applied.

Example prototype signal adjustments include:

```text
RENEWABLE_ENERGY   +25 Environmental
FOSSIL_FUEL        -25 Environmental
RECYCLING          +20 Environmental

EMPLOYEE_WELFARE   +25 Social
LABOR_RISK         -30 Social

CORRUPTION         -35 Governance
COMPLIANCE         +20 Governance
```

Sector multipliers can increase or decrease the effect of selected signals.

The overall score is the arithmetic mean of the Environmental, Social, and Governance scores.

All scores are clamped to the range `0–100`.

These values are prototype assumptions designed for demonstration and experimentation.

---

## Anomaly Detection

The current prototype identifies selected high-risk patterns.

Examples:

- Corruption-related transactions are flagged as high severity.
- Labor-risk transactions are flagged as high severity.
- Fossil-fuel transactions above `1,000,000` are flagged as high severity.

Anomaly detection is intentionally rule-based in this prototype.

---

## API Endpoints

### Health

```http
GET /health
```

### Analyze a Transaction

```http
POST /transactions/analyze
```

### Analyze Multiple Transactions

```http
POST /transactions/analyze/batch
```

### Upload CSV

```http
POST /transactions/upload-csv
```

### List Transactions

```http
GET /transactions
```

### Company Profile

```http
GET /companies/{company_id}/profile
```

### Company Trends

```http
GET /companies/{company_id}/trends
```

### Company Report

```http
GET /companies/{company_id}/report
```

### Company ESG Assistant

```http
POST /companies/{company_id}/chat
```

---

## CSV Format

The CSV should contain the following columns:

```text
transaction_id
timestamp
company_id
vendor_id
amount
currency
description
sector
```

Example:

```csv
transaction_id,timestamp,company_id,vendor_id,amount,currency,description,sector
TX001,2026-05-10T10:30:00,COMP001,V001,250000,USD,Purchase of solar panels,ENERGY
TX002,2026-05-12T12:00:00,COMP001,V002,150000,USD,Diesel fuel purchase,MANUFACTURING
```

---

## Running the Backend

Navigate to the backend:

```bash
cd backend
```

Create and activate a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

```env
GROQ_API_KEY=your_groq_api_key
```

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

---

## Running the Frontend

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Vite will display the local frontend URL in the terminal.

---

## Testing

Run the complete backend test suite:

```bash
cd backend
python -m pytest
```

The completed prototype currently passes:

```text
112 passed
```

There are currently two dependency deprecation warnings related to the Starlette/httpx and AnyIO testing stack.

---

## Frontend Build

To create a production build:

```bash
cd frontend
npm run build
```

The production build completes successfully.

Vite may report a warning about a JavaScript chunk exceeding the recommended size threshold. This does not prevent the build from completing.

---

## RAG Pipeline

The RAG workflow is:

```text
Company Transactions
        ↓
ESG Analysis
        ↓
Company Report
        ↓
Report Sections / Chunks
        ↓
Sentence Transformer Embeddings
        ↓
ChromaDB
        ↓
Similarity Search
        ↓
Retrieved Evidence
        ↓
Groq LLM
        ↓
Evidence-backed Answer
```

The assistant is instructed to answer only from retrieved ESG evidence and clearly state when the available evidence is insufficient.

---

## Environment Variables

The backend expects:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit the `.env` file or expose the API key in source control.

---

## Current Storage Model

The current prototype uses in-memory storage for transactions.

This means:

- Uploaded transactions are available while the backend process is running.
- Restarting the backend clears the in-memory transaction store.
- ChromaDB is currently configured as an in-memory client for the prototype.

A production implementation would replace these components with persistent storage.

---

## Design Notes and Limitations

GreenLedger is intentionally implemented as an explainable prototype.

### ESG Data Limitations

Transaction descriptions alone cannot provide a complete ESG assessment of a company.

A production system would require richer sources such as:
- Supplier information.
- Emissions data.
- Workforce data.
- Regulatory records.
- Corporate governance information.
- External ESG disclosures.
- Industry-specific datasets.

### Scoring Limitations

The scoring weights and sector multipliers are prototype assumptions.

They are not based on a recognized regulatory ESG rating methodology.

### NLP Limitations

The NLP classifier is trained on a small synthetic dataset intended for demonstration.

It should not be treated as a production-grade ESG language model.

### Anomaly Detection Limitations

The current anomaly engine uses deterministic rules rather than a trained anomaly-detection model.

### RAG Limitations

The assistant can only reason over the evidence retrieved from the indexed company reports.

### Persistence Limitations

Transaction and vector storage are currently in memory.

---

## Example Questions for the Assistant

```text
What are the main ESG risks for this company?

Which transactions contributed to environmental risk?

How did the company's ESG performance change over time?

What anomalies were detected?

What governance-related signals were found?

What recommendations are associated with the detected risks?

Why is the environmental score lower than the social score?
```

---

## Development Status

GreenLedger v1 includes:

- [x] Transaction validation
- [x] ESG taxonomy
- [x] Rule-based ESG classification
- [x] NLP classification
- [x] Hybrid classification
- [x] ESG scoring
- [x] Sector adjustments
- [x] Anomaly detection
- [x] Company analytics
- [x] Trend analysis
- [x] Recommendations
- [x] Report generation
- [x] CSV upload
- [x] Multi-company dashboard
- [x] ChromaDB indexing
- [x] RAG retrieval
- [x] Groq LLM assistant
- [x] React dashboard
- [x] Analytics page
- [x] Reports page
- [x] Assistant interface
- [x] Backend test suite
- [x] Frontend production build

---

## Future Improvements

Potential next steps include:

- Persistent PostgreSQL transaction storage.
- Persistent vector database.
- Larger and domain-specific ESG training data.
- Transformer-based ESG classification.
- More sophisticated anomaly detection.
- External ESG and regulatory data integration.
- Authentication and authorization.
- Role-based access control.
- Background indexing jobs.
- Better model evaluation and monitoring.
- More comprehensive ESG taxonomies.
- Production deployment and observability.

---

## Disclaimer

GreenLedger is an educational and hackathon-oriented prototype demonstrating explainable ESG analytics, transaction analysis, anomaly detection, report generation, retrieval-augmented generation, and LLM-assisted analysis.

It is not intended to provide regulatory, investment, accounting, legal, or professional ESG advice.
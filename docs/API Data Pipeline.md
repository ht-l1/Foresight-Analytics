# API Data Pipeline

## Overview
This document describes the architecture and flow of the API data pipeline for the backend. It covers how data is fetched from the Financial Modeling Prep (FMP) API, processed, stored, and exposed via RESTful endpoints. The structure is modular, maintainable, and ready for production and future scaling.

---

## High-Level Data Flow

1. **User/API Call** → 2. **FastAPI Route** → 3. **Business Service** → 4. **FMPClient** → 5. **CRUD** → 6. **Database** → 7. **Response to User**

---

## Directory Structure (Key Backend Folders)

```
backend/app/
├── api/           # API route definitions (HTTP only)
├── core/          # Config, DB setup, exceptions
├── crud/          # CRUD logic by domain (DB only)
├── models/        # SQLAlchemy models by domain
├── schemas/       # Pydantic schemas for FMP API validation
├── services/      # Business logic and FMP client
├── main.py        # FastAPI app entrypoint
```

---

## Summary Table: File Responsibilities & Connections

| Layer/Folder         | File/Function                | Purpose/Responsibility                                                                 | Example Call/Usage                                 | Connects To                        |
|----------------------|-----------------------------|----------------------------------------------------------------------------------------|----------------------------------------------------|-------------------------------------|
| **API**              | `api/routes.py`             | Defines REST endpoints, returns data; HTTP-only, no business logic                     | `/company/AAPL`, `/financials/AAPL/income-statements` | business_service, models           |
| **Service**          | `services/business_service.py`| Business logic, data retrieval, orchestrates FMP sync                                | `get_company_profile(symbol)`, `sync_income_statements()` | crud, fmp_client, models          |
|                      | `services/fmp_client.py`    | Async client for FMP API, fetches and validates data                                   | `get_company_profile('AAPL')`, `get_income_statement('AAPL')` | schemas, business_service         |
| **CRUD**             | `crud/crud_company.py`      | Company DB operations                                                                  | `create_company_from_profile(...)`, `get_company_by_symbol()` | models, business_service          |
|                      | `crud/crud_financials.py`   | Income statements DB operations                                                        | `upsert_income_statements(...)`                    | models, business_service            |
| **Models**           | `models/company.py`         | Company SQLAlchemy model with timestamps                                               | `Company`                                         | DB, crud, business_service, routes  |
|                      | `models/financials.py`      | IncomeStatement SQLAlchemy model with relationships                                     | `IncomeStatement`                                 | DB, crud, business_service, routes  |
| **Schemas**          | `schemas/fmp_schemas.py`    | Pydantic schemas for FMP API data validation and field mapping                         | `CompanyProfile`, `IncomeStatement`                | fmp_client, business_service        |
| **Config**           | `core/config.py`            | Central config with database URLs, API keys, FAANG symbols, rate limits                | `settings.fmp_api_key`, `settings.FAANG_SYMBOLS`  | All services and clients           |
| **Database**         | `core/database.py`          | SQLAlchemy setup, session management, database connection                              | `get_db()`, `engine`, `SessionLocal`              | All DB operations                   |

---

## Current API Endpoints

### **Data Query Endpoints**
- `GET /company/{symbol}` — Get company profile from database
- `GET /financials/{symbol}/income-statements` — Get paginated income statements

### **Route Configuration**
- Uses FastAPI with dependency injection for database sessions
- Enum-based data type validation (`FinancialDataType`)
- Pagination support with configurable skip/limit parameters
- Service mapping via `DATA_TYPE_TO_SERVICE` dictionary

---

## Data Pipeline Flow (Example: Getting Company Income Statements)

1. **GET** `/financials/AAPL/income-statements?skip=0&limit=20` →
2. **routes.py** validates path parameters and calls `get_income_statements` service →
3. **business_service.py** queries database via CRUD layer →
4. **crud_financials.py** executes paginated SQLAlchemy query →
5. **models/financials.py** defines the database schema and relationships →
6. **Response** returned with paginated results, total count, and pagination metadata

---

## Sync Process (Background Data Collection)

The sync process is handled by the `sync_income_statements` function in `business_service.py`:

1. **FMP Client** fetches data asynchronously from Financial Modeling Prep API
2. **Company Creation** - Gets existing company or creates new one with profile data
3. **Data Validation** - Uses Pydantic schemas to validate FMP API responses
4. **Data Transformation** - Converts API data to database format
5. **Upsert Operation** - Updates existing records or creates new ones
6. **Error Handling** - Logs errors and continues with next symbol

---

## Key Features & Architecture Decisions

### **Async FMP Client**
- Uses `aiohttp` for async HTTP requests
- Context manager pattern for session management
- Built-in rate limiting and error handling
- Pydantic validation for API responses

### **Database Design**
- PostgreSQL with SQLAlchemy ORM
- Neon cloud database with local fallback
- Timestamp mixins for audit trails
- Unique constraints to prevent duplicates
- Proper foreign key relationships

### **Configuration Management**
- Environment-based settings with Pydantic
- FAANG symbols predefined for free tier limits
- API rate limiting configured for free FMP tier
- Flexible database URL configuration

### **Error Handling**
- HTTPException for API errors
- Comprehensive logging throughout
- Fallback company creation when profile fetch fails
- Validation error handling for malformed data

---

## Current Limitations & Next Steps

### **What's Currently Implemented**
- Company profiles and income statements only
- FAANG companies focus (free tier constraint)
- Basic pagination support
- Async data fetching from FMP

### **Not Yet Implemented**
- Key metrics and financial ratios endpoints
- News articles endpoint
- Revenue Product/Geo Segment Endpoint
- Status/health check endpoints
- Background task scheduling

---

For further details, see the code comments.
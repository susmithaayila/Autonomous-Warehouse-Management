# Autonomous Warehouse Management System (AWMS)
## 24CYS401 – Secure Software Engineering End Semester Laboratory Examination

---

### 🚀 Quick Start Guide

#### 1. Start Application Server
The FastAPI backend server serves both the REST API and the Web Dashboard UI:
```bash
# Set PYTHONPATH and launch server
$env:PYTHONPATH="."
.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

#### 2. Access Systems
- **Web Dashboard UI:** [http://127.0.0.1:8000/app](http://127.0.0.1:8000/app)
- **API Health Check:** [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)
- **Swagger Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### 3. Test Demo Accounts
- **Administrator:** `admin` / `AdminPass123!`
- **Warehouse Operator:** `operator` / `OperatorPass123!`
- **Customer:** `customer` / `CustomerPass123!`
- **Security Auditor:** `auditor` / `AuditorPass123!`

---

### 🧪 Running Automated Security & Testing Tools

#### Run Pytest Suite (Unit, Integration, E2E, Fuzzing)
```bash
$env:PYTHONPATH="."
.venv\Scripts\python.exe -m pytest -v tests/
```

#### Run Bandit Static Code Security Analysis
```bash
.venv\Scripts\bandit.exe -r backend/ -f txt
```

#### Run pip-audit Dependency Vulnerability Scan
```bash
.venv\Scripts\pip-audit.exe
```

---

### 📦 Container & Kubernetes Commands

#### Docker Build & Run
```bash
docker build -t awms:v1.0 -f docker/Dockerfile .
docker-compose -f docker/docker-compose.yml up -d
```

#### Kubernetes Minikube Deployment
```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secret.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

---

### 📊 Examination Deliverables Index
- **Final Report:** `reports/AWMS_Final_Secure_Software_Engineering_Report.md`
- **Traceability Matrix:** `Traceability_Matrix.xlsx`
- **Excel Workbooks (14):** Located in `excel/` directory
- **Draw.io Diagrams (9):** Located in `diagrams/` directory
- **Evidence Directories (16):** Located in `evidence/P01_Agile` through `evidence/P16_FinalReview`

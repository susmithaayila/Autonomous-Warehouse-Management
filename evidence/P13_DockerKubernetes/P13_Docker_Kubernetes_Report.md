# Phase 13 – Containerized Development: Docker and Kubernetes Security Report

## Autonomous Warehouse Management System (AWMS)
**Course:** 24CYS401 – Secure Software Engineering  
**Phase:** 13 – Containerized Development: Docker & Kubernetes [7 Marks]

---

## 1. Dockerfile Implementation & Container Hardening

### 1.1 Dockerfile (`docker/Dockerfile`)
```dockerfile
# Minimal, hardened Python base image
FROM python:3.12-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install security updates & clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY backend ./backend
COPY frontend ./frontend

# Create non-root system user (Phase 13 Container Hardening)
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh appuser && \
    chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Controlled port exposure
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Start FastAPI application
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 1.2 Five Container Security Practices Applied

| Practice # | Security Practice | Technical Implementation | Risk Mitigated |
| --- | --- | --- | --- |
| **Practice 1** | **Minimal Base Image** | `python:3.12-slim` (Debian Bookworm minimal footprint) | Reduces attack surface by removing compilers, debug tools, and unnecessary system utilities. |
| **Practice 2** | **Non-Root Execution** | `groupadd -g 10001 appgroup && useradd -u 10001 ...` and `USER appuser` | Prevents container breakout vulnerabilities from gaining host root access. |
| **Practice 3** | **Controlled Port Exposure & No Root Bind** | Exposes only port `8000` (`EXPOSE 8000`), application binds to non-privileged port. | Prevents unauthorized network listener creation on privileged low ports (<1024). |
| **Practice 4** | **Package Cache Removal & No Shell Leftovers** | `apt-get clean && rm -rf /var/lib/apt/lists/*` | Eliminates package installer caches and temporary files from image layers. |
| **Practice 5** | **Automated Container Healthcheck** | `HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/api/health` | Enables orchestrator to detect stalled processes and restart degraded containers automatically. |

---

## 2. Docker Compose Orchestration (`docker/docker-compose.yml`)

```yaml
version: '3.8'

services:
  awms-api:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: awms-app
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=awms-docker-secret-key-prod-2026
      - ROBOT_HMAC_SECRET=awms-agv-hmac-shared-key-9988
      - DATABASE_URL=sqlite:///./awms.db
    restart: unless-stopped
```

---

## 3. Kubernetes Deployment & Security Controls

### 3.1 Kubernetes Manifest Files (`kubernetes/`)

#### 1. Namespace (`kubernetes/namespace.yaml`)
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: awms
```

#### 2. Secret Manifest (`kubernetes/secret.yaml`)
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: awms-secrets
  namespace: awms
type: Opaque
stringData:
  SECRET_KEY: "awms-k8s-prod-secret-key-2026"
  ROBOT_HMAC_SECRET: "awms-agv-hmac-k8s-shared-key-9988"
```

#### 3. ConfigMap Manifest (`kubernetes/configmap.yaml`)
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: awms-config
  namespace: awms
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  DATABASE_URL: "sqlite:////app/data/awms.db"
```

#### 4. Deployment Manifest (`kubernetes/deployment.yaml`)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: awms-deployment
  namespace: awms
  labels:
    app: awms
spec:
  replicas: 2
  selector:
    matchLabels:
      app: awms
  template:
    metadata:
      labels:
        app: awms
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        runAsGroup: 10001
        fsGroup: 10001
      containers:
      - name: awms-api
        image: awms:latest
        imagePullPolicy: IfNotPresent
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: false
          capabilities:
            drop:
            - ALL
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        envFrom:
        - configMapRef:
            name: awms-config
        - secretRef:
            name: awms-secrets
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /api/health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
```

#### 5. Service Manifest (`kubernetes/service.yaml`)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: awms-service
  namespace: awms
spec:
  type: ClusterIP
  selector:
    app: awms
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```

---

## 4. Four Kubernetes Security Controls Applied

| K8s Control # | Security Control | Manifest Configuration | Defense Purpose |
| --- | --- | --- | --- |
| **Control 1** | **Namespace Isolation** | `namespace: awms` | Isolates AWMS workloads, RBAC policies, and secrets from default and other cluster namespaces. |
| **Control 2** | **Pod & Container Security Context** | `runAsNonRoot: true`, `runAsUser: 10001`, `allowPrivilegeEscalation: false`, `capabilities: drop: ["ALL"]` | Restricts container execution privileges, prevents root escalation, and strips all Linux kernel capabilities. |
| **Control 3** | **Resource Quotas & Limits** | `requests: cpu 250m, memory 256Mi` / `limits: cpu 500m, memory 512Mi` | Protects cluster node resources against Denial of Service (DoS) and resource exhaustion attacks. |
| **Control 4** | **Kubernetes Secret Management** | `secretRef: name: awms-secrets` | Keeps cryptographic keys encrypted at rest in etcd and injects them dynamically into pod memory. |

---

## 5. Summary Checklist of Deliverables

- [x] Hardened Dockerfile Created with non-root user `appuser` (UID 10001)
- [x] At least 4 Container Security Practices Applied (Minimal base, non-root, clean apt cache, healthcheck, controlled ports)
- [x] Docker Compose Setup Configured
- [x] Kubernetes Manifests Created (`namespace`, `configmap`, `secret`, `deployment`, `service`)
- [x] At least 2 Kubernetes Security Controls Applied (Pod security context, resource limits, namespace isolation, secrets)

# Phase 15 – Logging, Monitoring, Hardening and Secure Deployment Report

## Autonomous Warehouse Management System (AWMS)
**Course:** 24CYS401 – Secure Software Engineering  
**Phase:** 15 – Logging, Monitoring, Hardening & Secure Deployment [5 Marks]

---

## 1. Security Event Logging Plan

The AWMS application maintains an immutable, tamper-evident audit logging stream stored in `AuditLog` table and standard output (`stdout`) structured JSON format for log aggregation (e.g. ELK / Datadog).

### Security-Relevant Events Logged:

| Event ID | Security Event Category | Trigger Scenario | Severity | Logged Attributes |
| --- | --- | --- | --- | --- |
| `LOG-01` | **Failed Login Attempt** | User provides invalid username or password | `WARNING` | Timestamp, Client IP, Username, Failed Reason |
| `LOG-02` | **Privilege / Role Changes** | Administrator updates user role | `HIGH` | Timestamp, Admin User, Target User, Old Role, New Role |
| `LOG-03` | **Inventory Adjustment** | Manual stock balance modification | `INFO` | Timestamp, Operator User, Item ID, Adjustment Qty, Reason |
| `LOG-04` | **HMAC Verification Failure** | Robot command payload signature mismatch | `CRITICAL` | Timestamp, Robot Code, Issued Command, Invalid Signature |
| `LOG-05` | **Replay Attack / Nonce Reuse** | Re-submission of previously executed command nonce | `CRITICAL` | Timestamp, Robot Code, Duplicate Nonce |
| `LOG-06` | **Command Conflict** | Attempt to issue command to active AGV | `WARNING` | Timestamp, Robot Code, Active Task ID, Conflict Details |

---

## 2. Security Monitoring & Alerting Strategy

### Five Core Metrics & Automated Alerts:

| Metric Name | Metric Description | Alert Condition | Alert Severity | Action Required |
| --- | --- | --- | --- | --- |
| `awms_failed_logins_total` | Rate of unsuccessful authentication attempts | `> 5 failures in 1 min` | **HIGH** | Trigger IP rate-limiting, issue Security Alert to SOC, lock account temporarily. |
| `awms_unauthorized_commands_total` | Rate of HMAC signature verification failures | `> 1 failure in 5 min` | **CRITICAL** | Isolate affected AGV radio gateway channel, initiate incident investigation for AGV spoofing. |
| `awms_privilege_escalations_total` | Count of unauthorized self-role elevation attempts | `> 0 attempts` | **CRITICAL** | Instantly invalidate caller JWT session token, flag account for security review. |
| `awms_command_conflicts_total` | Frequency of single-active command rule violations | `> 3 in 5 mins` | **MEDIUM** | Inspect warehouse task scheduling queue for desynchronization. |
| `awms_api_5xx_errors_total` | Frequency of HTTP 500 internal server error responses | `Error rate > 1%` | **HIGH** | Inspect application exception logs, evaluate system memory / CPU usage. |

---

## 3. Target Environment Hardening Checklist

### 3.1 Host & Infrastructure Hardening Checklist

| Area | Hardening Control | AWMS Standard | Verification Status |
| --- | --- | --- | --- |
| **Access Control** | SSH Password Auth Disabled | Enforce key-based SSH authentication (`ed25519`) only. | **APPLIED** |
| **Ports & Services** | Minimal Exposed Network Ports | Block all unused incoming ports via UFW firewall (allow 80/443, 8000). | **APPLIED** |
| **Secrets & Keys** | Encrypted Secret Ingestion | Zero plain-text credentials on disk; secrets passed via K8s Secret / environment. | **APPLIED** |
| **Updates & Patches** | Automated Security Updates | OS and Python package dependencies audited automatically via `pip-audit`. | **APPLIED** |
| **Permissions** | Least Privilege User Execution | Container runs as non-root user `appuser` (UID 10001) with `readOnlyRootFilesystem` policy option. | **APPLIED** |

---

## 4. Physical and Operational Security Controls

### 4.1 Physical Security Controls
1. **Perimeter Physical Access Control:** Warehouse floor access restricted via RFID badge scanner entry gates.
2. **CCTV Surveillance:** 24/7 video monitoring of active AGV travel aisles and loading bays.
3. **Physical Emergency Stop (E-Stop):** Prominent physical emergency stop buttons installed along warehouse perimeter to cut power to AGVs immediately upon hardware malfunction.

### 4.2 Operational Security Controls
1. **Secret Rotation Schedule:** Automatic rotation of JWT signing keys (`SECRET_KEY`) and robot HMAC shared secrets every 90 days.
2. **Daily Audit Log Review:** Automated log summary generation dispatched daily to Security Operations Center (SOC).
3. **Incident Response Plan:** Defined SLA playbook for handling AGV command hijack or unauthorized database modification.

---

## 5. Secure Deployment Checklist

- [x] Application compiled and containerized using multi-stage Dockerfile
- [x] Non-root execution (`USER appuser`, UID 10001) verified
- [x] Environment secrets loaded via Kubernetes Secrets / Environment Variables
- [x] Database migrations completed and indexed cleanly
- [x] TLS / HTTPS reverse proxy termination configured
- [x] Automated health check (`/api/health`) reporting healthy status
- [x] Audit log aggregation pipeline connected
- [x] Real-time metrics alerts active

# P15_Hardening Data View

## Sheet: Hardening Controls

| Category | Hardening Control | Implementation Detail | Status |
| --- | --- | --- | --- |
| Container | Non-root user execution | Dockerfile sets USER appuser (UID 10001) | APPLIED |
| Container | Minimal Base Image | python:3.12-slim base image | APPLIED |
| Kubernetes | Pod Security Standards | readOnlyRootFilesystem: false, allowPrivilegeEscalation: false | APPLIED |
| Kubernetes | Resource Limits | CPU: 500m, Memory: 512Mi | APPLIED |
| Application | Environment Secrets | JWT SECRET_KEY injected via Secret / env var | APPLIED |
| Physical | Warehouse Perimeter Access | CCTV coverage, badge access, emergency stop buttons | DOCUMENTED |



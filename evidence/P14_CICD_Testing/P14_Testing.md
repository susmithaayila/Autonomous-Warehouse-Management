# P14_Testing Data View

## Sheet: Test Results

| Test ID | Test Type | Target Component | Test Objective | Result | Execution Time |
| --- | --- | --- | --- | --- | --- |
| UT-01 | Unit Test | AuthService | Verify password hashing and JWT token creation | PASSED | 0.12s |
| UT-02 | Unit Test | InventoryService | Verify atomic inventory update and negative balance block | PASSED | 0.15s |
| IT-01 | Integration | FulfillmentService | End-to-end order placement, task creation and stock reservation | PASSED | 0.35s |
| E2E-01 | System / E2E | Robot Execution | Issue HMAC command, simulate robot execution and check order completion | PASSED | 0.52s |
| FZ-01 | Fuzzing | API Payloads | Hypothesis fuzz testing on login & robot command payloads | PASSED | 1.20s |



# P03_UML Data View

## Sheet: Use Cases

| Use Case ID | Name | Primary Actor | Preconditions | Main Flow | Postconditions | Security Controls |
| --- | --- | --- | --- | --- | --- | --- |
| UC-01 | Create and Fulfill Customer Order | Customer | User is logged in as Customer, Stock available | 1. Customer selects item and quantity
2. Order created & stock reserved
3. Fulfillment task created
4. Robot picks, moves, drops item
5. Order status set to FULFILLED | Stock deducted, Order completed | JWT Auth, ACID stock reservation, Audit logging |
| UC-02 | Execute Authorized Robot Task | Robot / System | Robot registered, Task assigned to robot | 1. Admin/Operator issues command with nonce
2. HMAC-SHA256 signature generated
3. Robot verifies signature & executes command
4. Robot updates status & task completes | Robot task completed, status updated | HMAC verification, Nonce anti-replay, State conflict check |



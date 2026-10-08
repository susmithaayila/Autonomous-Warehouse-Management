# P12_Secure_Coding Data View

## Sheet: Code Refactoring

| Module | Weakness | Threat Vector | Secure Refactored Code Feature | Verification Status |
| --- | --- | --- | --- | --- |
| CommandAuthService | Unauthenticated command execution | Unauthorized robot control | HMAC-SHA256 verification + Nonce checking | VERIFIED |
| InventoryService | Direct non-atomic stock subtraction | Inventory race conditions & negative stock | SQLAlchemy row-level with_for_update() locking | VERIFIED |
| UserService | Missing self-role check | Privilege escalation to Admin | Server-side check rejecting current_user.id == target.id | VERIFIED |



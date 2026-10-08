# P08_Attack_Tree Data View

## Sheet: Attack Tree

| Node ID | Node Type | Goal / Sub-goal | Attacker Vector | Security Control |
| --- | --- | --- | --- | --- |
| ROOT | GOAL | Unauthorized Robot Operation & Movement | Exploit AWMS to move physical goods maliciously | Defense-in-Depth Security Controls |
| N1 | OR Branch | Compromise User Account | Credential stuffing / brute-force login | Bcrypt hashing, Account lockout after 5 attempts |
| N2 | OR Branch | Compromise Robot Identity | Spoofing robot network headers | HMAC-SHA256 signature validation with shared secret |
| N3 | OR Branch | Exploit Privilege Escalation | Modifying user role parameter in API | Server-side RBAC & self-escalation check (SR-04) |
| N4 | OR Branch | Replay Robot Command | Sniffing past valid command payloads | UUID Nonce tracking & single-use command verification |
| N5 | OR Branch | Exploit Race Condition | Simultaneous concurrent order submissions | Row locking with_for_update() in SQLite transaction |



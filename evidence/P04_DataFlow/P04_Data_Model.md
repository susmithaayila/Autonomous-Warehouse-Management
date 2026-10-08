# P04_Data_Model Data View

## Sheet: ER Entities

| Entity | Attributes | Primary Key | Foreign Keys | Relationships |
| --- | --- | --- | --- | --- |
| User | id, username, hashed_password, role_id, is_active, failed_login_attempts | id | role_id -> Role.id | One-to-Many with CustomerOrder, AuditLog |
| Role | id, name, description | id | None | One-to-Many with User |
| Robot | id, robot_code, name, status, battery_level, current_location, secret_key | id | None | One-to-Many with RobotCommand, WarehouseTask |
| InventoryItem | id, sku, name, location, quantity, reserved_quantity, unit_price | id | None | One-to-Many with OrderItem, InventoryTransaction |
| CustomerOrder | id, order_number, customer_id, status, created_at, updated_at | id | customer_id -> User.id | One-to-Many with OrderItem, WarehouseTask |
| WarehouseTask | id, task_code, order_id, item_id, quantity, pickup_location, drop_location, assigned_robot_id, status | id | order_id, item_id, assigned_robot_id | One-to-Many with RobotCommand |
| RobotCommand | id, command_id, task_id, robot_id, command_type, payload, status, nonce, signature | id | task_id, robot_id | None |
| AuditLog | id, timestamp, actor_username, actor_role, action, resource, result, severity, ip_address, details | id | None | None |



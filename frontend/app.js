const API_BASE = '/api';
let token = localStorage.getItem('awms_token') || null;
let currentUser = null;

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initAuth();
    loadDashboardData();
    loadInventoryData();
    loadRobotsData();
    loadTasksData();
    loadOrdersData();
    loadSecurityData();
    loadDockerData();
    loadCICDData();

    // Auto refresh every 10s
    setInterval(() => {
        if (token) {
            loadDashboardData();
            loadRobotsData();
            loadTasksData();
            loadSecurityData();
            loadDockerData();
            loadCICDData();
        }
    }, 10000);
});

function initNavigation() {
    const navBtns = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    navBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');
            navBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

function showToast(msg, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerText = msg;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
}

function initAuth() {
    const modal = document.getElementById('login-modal');
    const authBtn = document.getElementById('auth-btn');
    const closeModal = document.querySelector('.close-modal');
    const loginForm = document.getElementById('login-form');

    authBtn.addEventListener('click', () => {
        if (token) {
            // Logout
            token = null;
            currentUser = null;
            localStorage.removeItem('awms_token');
            updateUIForAuth();
            showToast('Successfully logged out', 'info');
        } else {
            modal.style.display = 'flex';
        }
    });

    closeModal.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const u = document.getElementById('username').value;
        const p = document.getElementById('password').value;

        try {
            const res = await fetch(`${API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: u, password: p })
            });

            if (!res.ok) {
                const err = await res.json();
                throw new Error(err.detail || 'Login failed');
            }

            const data = await res.json();
            token = data.access_token;
            currentUser = { username: data.username, role: data.role, id: data.user_id };
            localStorage.setItem('awms_token', token);

            modal.style.display = 'none';
            updateUIForAuth();
            showToast(`Welcome ${data.username} (${data.role})!`, 'success');
            refreshAllData();
        } catch (err) {
            showToast(err.message, 'error');
        }
    });

    if (token) {
        fetchMe();
    }
}

function quickFill(user, pass) {
    document.getElementById('username').value = user;
    document.getElementById('password').value = pass;
}

async function fetchMe() {
    try {
        const res = await fetch(`${API_BASE}/auth/me`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
            const data = await res.json();
            currentUser = { username: data.username, role: data.role.name, id: data.id };
            updateUIForAuth();
        } else {
            token = null;
            localStorage.removeItem('awms_token');
        }
    } catch (e) {
        console.error(e);
    }
}

function updateUIForAuth() {
    const badge = document.getElementById('user-badge');
    const authBtn = document.getElementById('auth-btn');

    if (currentUser && token) {
        badge.innerHTML = `<strong>${currentUser.username}</strong> <span class="badge badge-idle">${currentUser.role}</span>`;
        authBtn.innerText = 'Logout';
    } else {
        badge.innerText = 'Not Logged In';
        authBtn.innerText = 'Login';
    }
}

function refreshAllData() {
    loadDashboardData();
    loadInventoryData();
    loadRobotsData();
    loadTasksData();
    loadOrdersData();
    loadSecurityData();
}

// Data Fetchers
async function loadDashboardData() {
    try {
        const invRes = await fetch(`${API_BASE}/inventory`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (invRes.ok) {
            const inv = await invRes.json();
            document.getElementById('dash-total-inventory').innerText = inv.length;
        }

        const rbtRes = await fetch(`${API_BASE}/robots`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (rbtRes.ok) {
            const rbts = await rbtRes.json();
            const activeCount = rbts.filter(r => r.status !== 'OFFLINE').length;
            document.getElementById('dash-active-robots').innerText = activeCount;

            const tbody = document.getElementById('dash-robots-tbody');
            tbody.innerHTML = rbts.map(r => `
                <tr>
                    <td><strong>${r.robot_code}</strong></td>
                    <td>${r.name}</td>
                    <td><span class="badge badge-${r.status.toLowerCase()}">${r.status}</span></td>
                    <td>${r.battery_level}%</td>
                    <td><code>${r.current_location}</code></td>
                </tr>
            `).join('');
        }

        const taskRes = await fetch(`${API_BASE}/tasks`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (taskRes.ok) {
            const tasks = await taskRes.json();
            const pending = tasks.filter(t => t.status === 'PENDING' || t.status === 'ASSIGNED').length;
            document.getElementById('dash-pending-tasks').innerText = pending;
        }

        const ordRes = await fetch(`${API_BASE}/orders`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (ordRes.ok) {
            const orders = await ordRes.json();
            const tbody = document.getElementById('dash-orders-tbody');
            tbody.innerHTML = orders.slice(0, 5).map(o => `
                <tr>
                    <td><strong>${o.order_number}</strong></td>
                    <td><span class="badge badge-${o.status === 'FULFILLED' ? 'idle' : 'pending'}">${o.status}</span></td>
                    <td>${new Date(o.created_at).toLocaleTimeString()}</td>
                </tr>
            `).join('');
        }
    } catch (e) {
        console.error(e);
    }
}

async function loadInventoryData() {
    try {
        const res = await fetch(`${API_BASE}/inventory`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (res.ok) {
            const items = await res.json();
            const tbody = document.getElementById('inventory-tbody');
            tbody.innerHTML = items.map(item => `
                <tr>
                    <td><code>${item.sku}</code></td>
                    <td><strong>${item.name}</strong></td>
                    <td><code>${item.location}</code></td>
                    <td>${item.quantity}</td>
                    <td>${item.reserved_quantity}</td>
                    <td>$${item.unit_price.toFixed(2)}</td>
                    <td>
                        <button class="btn-primary" style="padding:4px 8px;font-size:0.75rem" onclick="updateStock(${item.id})">Adjust Stock</button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (e) {
        console.error(e);
    }
}

async function loadRobotsData() {
    try {
        const res = await fetch(`${API_BASE}/robots`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (res.ok) {
            const robots = await res.json();
            const grid = document.getElementById('robots-cards-grid');
            grid.innerHTML = robots.map(r => `
                <div class="robot-card">
                    <div class="robot-card-header">
                        <span class="robot-code">${r.robot_code}</span>
                        <span class="badge badge-${r.status.toLowerCase()}">${r.status}</span>
                    </div>
                    <div><strong>${r.name}</strong></div>
                    <div>📍 Location: <code>${r.current_location}</code></div>
                    <div>🔋 Battery: ${r.battery_level}%</div>
                    <div>🕒 Heartbeat: ${new Date(r.last_heartbeat).toLocaleTimeString()}</div>
                </div>
            `).join('');
        }
    } catch (e) {
        console.error(e);
    }
}

async function loadTasksData() {
    try {
        const res = await fetch(`${API_BASE}/tasks`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (res.ok) {
            const tasks = await res.json();
            const tbody = document.getElementById('tasks-tbody');
            tbody.innerHTML = tasks.map(t => `
                <tr>
                    <td><code>${t.task_code}</code></td>
                    <td><code>${t.pickup_location}</code></td>
                    <td><code>${t.drop_location}</code></td>
                    <td>${t.assigned_robot_id ? `Robot #${t.assigned_robot_id}` : '<em style="color:#9ca3af">Unassigned</em>'}</td>
                    <td><span class="badge badge-${t.status === 'COMPLETED' ? 'idle' : 'pending'}">${t.status}</span></td>
                    <td>
                        ${!t.assigned_robot_id ? `<button class="btn-primary" style="padding:4px 8px;font-size:0.75rem" onclick="assignTaskPrompt(${t.id})">Assign Robot</button>` : `<button class="btn-primary" style="padding:4px 8px;font-size:0.75rem;background:#8b5cf6" onclick="issueCmdPrompt(${t.id}, ${t.assigned_robot_id})">Issue Cmd</button>`}
                    </td>
                </tr>
            `).join('');
        }

        const cmdRes = await fetch(`${API_BASE}/commands`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (cmdRes.ok) {
            const cmds = await cmdRes.json();
            const tbody = document.getElementById('commands-tbody');
            tbody.innerHTML = cmds.map(c => `
                <tr>
                    <td><code>${c.command_id}</code></td>
                    <td><strong>${c.command_type}</strong></td>
                    <td>Robot #${c.robot_id}</td>
                    <td><code>${c.nonce}</code></td>
                    <td><span class="badge badge-${c.status === 'SUCCESS' ? 'idle' : 'pending'}">${c.status}</span></td>
                </tr>
            `).join('');
        }
    } catch (e) {
        console.error(e);
    }
}

async function loadOrdersData() {
    try {
        const res = await fetch(`${API_BASE}/orders`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (res.ok) {
            const orders = await res.json();
            const tbody = document.getElementById('orders-tbody');
            tbody.innerHTML = orders.map(o => `
                <tr>
                    <td><code>${o.order_number}</code></td>
                    <td>User #${o.customer_id}</td>
                    <td><span class="badge badge-${o.status === 'FULFILLED' ? 'idle' : 'pending'}">${o.status}</span></td>
                    <td>${new Date(o.created_at).toLocaleString()}</td>
                    <td>${new Date(o.updated_at).toLocaleString()}</td>
                </tr>
            `).join('');
        }
    } catch (e) {
        console.error(e);
    }
}

async function loadSecurityData() {
    try {
        const logsRes = await fetch(`${API_BASE}/audit/logs`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (logsRes.ok) {
            const logs = await logsRes.json();
            const tbody = document.getElementById('audit-tbody');
            tbody.innerHTML = logs.map(l => `
                <tr>
                    <td>${new Date(l.timestamp).toLocaleTimeString()}</td>
                    <td><strong>${l.actor_username}</strong></td>
                    <td><span class="badge badge-idle">${l.actor_role}</span></td>
                    <td><code>${l.action}</code></td>
                    <td>${l.resource}</td>
                    <td><span class="badge badge-${l.result === 'SUCCESS' ? 'idle' : 'offline'}">${l.result}</span></td>
                    <td><strong style="color:${l.severity === 'CRITICAL' ? '#ef4444' : '#f59e0b'}">${l.severity}</strong></td>
                    <td><small>${l.details || ''}</small></td>
                </tr>
            `).join('');
        }

        const metricsRes = await fetch(`${API_BASE}/audit/metrics`, { headers: token ? { 'Authorization': `Bearer ${token}` } : {} });
        if (metricsRes.ok) {
            const m = await metricsRes.json();
            document.getElementById('sec-failed-logins').innerText = m.failed_login_count;
            document.getElementById('sec-unauth-cmds').innerText = m.unauthorized_command_count;
            document.getElementById('sec-priv-changes').innerText = m.privilege_changes_count;
            document.getElementById('sec-cmd-conflicts').innerText = m.command_conflict_count;
        }
    } catch (e) {
        console.error(e);
    }
}

// Prompts & Action Handlers
async function updateStock(itemId) {
    if (!token) return showToast('Please login first', 'error');
    const qtyStr = prompt("Enter quantity adjustment (positive or negative):", "10");
    if (!qtyStr) return;
    const qty = parseInt(qtyStr, 10);
    const reason = prompt("Enter reason for stock adjustment:", "Routine replenishment");

    try {
        const res = await fetch(`${API_BASE}/inventory/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ item_id: itemId, quantity_change: qty, reason: reason || 'Adjustment' })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail);
        }
        showToast('Inventory updated successfully', 'success');
        loadInventoryData();
    } catch (e) {
        showToast(e.message, 'error');
    }
}

async function assignTaskPrompt(taskId) {
    if (!token) return showToast('Please login as Admin/Operator', 'error');
    const robotIdStr = prompt("Enter Autonomous Robot ID to assign (e.g. 1, 2, 3):", "1");
    if (!robotIdStr) return;

    try {
        const res = await fetch(`${API_BASE}/tasks/assign`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ task_id: taskId, robot_id: parseInt(robotIdStr, 10) })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail);
        }
        showToast('Robot assigned to task successfully', 'success');
        loadTasksData();
        loadRobotsData();
    } catch (e) {
        showToast(e.message, 'error');
    }
}

async function issueCmdPrompt(taskId, robotId) {
    if (!token) return showToast('Please login first', 'error');
    const cmdType = prompt("Enter Command Type (PICK, MOVE, DROP, STOP):", "PICK").toUpperCase();
    const nonce = "NONCE-" + Math.floor(Math.random() * 1000000);

    try {
        const res = await fetch(`${API_BASE}/commands/issue`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                task_id: taskId,
                robot_id: robotId,
                command_type: cmdType,
                payload: `TargetTask:${taskId}`,
                nonce: nonce
            })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail);
        }
        const cmdData = await res.json();
        showToast(`Command ${cmdData.command_id} issued! Simulating execution...`, 'success');
        loadTasksData();

        // Simulate Robot HMAC Execution
        setTimeout(() => executeCmdSimulated(cmdData), 1500);
    } catch (e) {
        showToast(e.message, 'error');
    }
}

async function executeCmdSimulated(cmdData) {
    try {
        // Robot codes & secrets dictionary for simulation
        const robotCodes = { 1: "ROBOT-01", 2: "ROBOT-02", 3: "ROBOT-03" };
        const rCode = robotCodes[cmdData.robot_id] || "ROBOT-01";
        
        // HMAC compute simulation via API
        const res = await fetch(`${API_BASE}/commands/execute`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                command_id: cmdData.command_id,
                robot_code: rCode,
                signature: cmdData.signature
            })
        });
        if (res.ok) {
            showToast(`Robot ${rCode} executed command ${cmdData.command_type} successfully!`, 'success');
            loadTasksData();
            loadRobotsData();
            loadDashboardData();
        }
    } catch (e) {
        console.error(e);
    }
}

async function openCreateOrderModal() {
    if (!token) return showToast('Please login to place an order', 'error');
    const itemIdStr = prompt("Enter Item ID to purchase (e.g. 1 for Electric Motor, 2 for Controller Board):", "1");
    if (!itemIdStr) return;
    const qtyStr = prompt("Enter Quantity:", "2");
    if (!qtyStr) return;

    try {
        const res = await fetch(`${API_BASE}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                items: [{ item_id: parseInt(itemIdStr, 10), quantity: parseInt(qtyStr, 10) }]
            })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail);
        }
        showToast('Order placed successfully! Task created for fulfillment.', 'success');
        loadOrdersData();
        loadTasksData();
        loadInventoryData();
        loadDashboardData();
    } catch (e) {
        showToast(e.message, 'error');
    }
}

async function loadDockerData() {
    try {
        const res = await fetch(`${API_BASE}/docker/status`);
        if (!res.ok) return;
        const data = await res.json();
        console.log('Docker Operations Status:', data);
    } catch (e) {
        console.error('Docker load error:', e);
    }
}

async function loadCICDData() {
    try {
        const res = await fetch(`${API_BASE}/cicd/status`);
        if (!res.ok) return;
        const data = await res.json();
        console.log('CI/CD Pipeline Status:', data);
    } catch (e) {
        console.error('CI/CD load error:', e);
    }
}

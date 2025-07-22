document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardData();
});

async function fetchDashboardData() {
    try {
        const response = await fetch('http://127.0.0.1:5001/api/dashboard_data');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        renderDashboard(data);
    } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
        // Display an error message to the user on the page
    }
}

function renderDashboard(data) {
    renderSummary(data);
    renderTransactions(data.transactions);
    renderBudgets(data.budgets);
    renderGoals(data.goals);
    renderPortfolioAllocation(data.portfolio.allocation);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
    }).format(amount);
}

function renderSummary(data) {
    // Portfolio
    const portfolio = data.portfolio;
    const pnlPercentage = (portfolio.overall_pnl / portfolio.total_invested) * 100;
    document.getElementById('portfolio-value').textContent = formatCurrency(portfolio.current_value);
    const pnlElement = document.getElementById('portfolio-pnl');
    pnlElement.textContent = `${formatCurrency(portfolio.overall_pnl)} (${pnlPercentage.toFixed(2)}%)`;
    pnlElement.className = portfolio.overall_pnl >= 0 ? 'positive' : 'negative';

    const dayGainElement = document.getElementById('portfolio-day-gain');
    dayGainElement.textContent = `Today: ${formatCurrency(portfolio.day_gain)}`;
    dayGainElement.className = portfolio.day_gain >= 0 ? 'positive' : 'negative';

    // Financial Health
    document.getElementById('health-score').textContent = data.financial_health.score;
    document.getElementById('health-assessment').textContent = data.financial_health.assessment;

    // Monthly Spending
    const totalSpent = data.budgets.reduce((sum, b) => sum + b.spent_amount, 0);
    document.getElementById('total-spent').textContent = formatCurrency(totalSpent);
}


function renderTransactions(transactions) {
    const list = document.getElementById('transaction-list');
    list.innerHTML = '';
    transactions.forEach(tx => {
        const item = document.createElement('li');
        item.className = 'transaction-item';
        item.innerHTML = `
            <div class="transaction-details">
                <span class="transaction-merchant">${tx.merchant}</span>
                <span class="transaction-category">${tx.category}</span>
            </div>
            <span class="transaction-amount negative">${formatCurrency(tx.amount)}</span>
        `;
        list.appendChild(item);
    });
}

function renderBudgets(budgets) {
    const ctx = document.getElementById('budgetChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: budgets.map(b => b.category),
            datasets: [{
                label: 'Spent',
                data: budgets.map(b => b.spent_amount),
                backgroundColor: 'rgba(0, 123, 255, 0.6)',
                borderColor: 'rgba(0, 123, 255, 1)',
                borderWidth: 1
            }, {
                label: 'Budget',
                data: budgets.map(b => b.allocated_amount),
                backgroundColor: 'rgba(230, 230, 230, 0.2)',
                borderColor: 'rgba(230, 230, 230, 0.5)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#a0a0a0' },
                    grid: { color: '#333' }
                },
                x: {
                    ticks: { color: '#a0a0a0' },
                    grid: { display: false }
                }
            },
            plugins: {
                legend: { labels: { color: '#e0e0e0' } }
            }
        }
    });
}

function renderGoals(goals) {
    const container = document.getElementById('goal-list');
    container.innerHTML = '';
    goals.forEach(goal => {
        const percentage = (goal.current_amount / goal.target_amount) * 100;
        const item = document.createElement('div');
        item.className = 'goal-item';
        item.innerHTML = `
            <div class="goal-info">
                <span>${goal.goal_name}</span>
                <span>${formatCurrency(goal.current_amount)} / ${formatCurrency(goal.target_amount)}</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar" style="width: ${percentage}%"></div>
            </div>
        `;
        container.appendChild(item);
    });
}

function renderPortfolioAllocation(allocation) {
    const ctx = document.getElementById('allocationChart').getContext('2d');
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: allocation.map(a => a.name),
            datasets: [{
                data: allocation.map(a => a.value),
                backgroundColor: ['#007bff', '#28a745', '#ffc107', '#17a2b8'],
                borderColor: '#1e1e1e',
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#e0e0e0' }
                }
            }
        }
    });
}


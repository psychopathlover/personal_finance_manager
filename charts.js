// Pie chart - category breakdown
const ctxPie = document.getElementById('categoryPieChart').getContext('2d');
new Chart(ctxPie, {
    type: 'pie',
    data: {
        labels: Object.keys(categoryData),
        datasets: [{
            data: Object.values(categoryData),
            backgroundColor: ['#66bb6a', '#ef5350', '#42a5f5', '#ffca28', '#ab47bc'],
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Category Distribution'
            }
        }
    }
});

// Bar chart - daily breakdown
const ctxBar = document.getElementById('dailyBarChart').getContext('2d');
new Chart(ctxBar, {
    type: 'bar',
    data: {
        labels: Object.keys(dailyData),
        datasets: [{
            label: 'Amount (₹)',
            data: Object.values(dailyData),
            backgroundColor: '#42a5f5',
        }]
    },
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Daily Expenses'
            }
        }
    }
});

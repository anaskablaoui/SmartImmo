const chart_labels = JSON.parse(document.getElementById('chart-labels').textContent);
const chart_data   = JSON.parse(document.getElementById('chart-data').textContent);

const ctx = document.getElementById('revenusChart').getContext('2d');

new Chart(ctx, {
  type: 'line',
  data: {
    labels: chart_labels,
    datasets: [{
      label: 'Revenus mensuels ',
      data: chart_data,
      backgroundColor: 'rgba(45, 122, 95, 0.6)',
      borderColor: 'rgba(45, 122, 95, 1)',
      borderWidth: 1
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: { beginAtZero: true }
    }
  }
});
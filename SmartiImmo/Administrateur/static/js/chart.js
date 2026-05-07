const ctx = document.getElementById('revenusChart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: {{ chart_labels|safe }},
      datasets: [{
        label: 'Revenus mensuels (30%)',
        data: {{ chart_data|safe }},
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
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
// Gráficos individuales (históricos)
const datosGraficos = window.datosGraficos || (typeof datos_graficos_json !== "undefined" ? datos_graficos_json : {});
const container = document.getElementById('graficos-container');
let hayGraficos = false;
if (container) {
  container.innerHTML = '';

  Object.keys(datosGraficos).forEach((tipo, index) => {
    const datosTipo = datosGraficos[tipo];
    if (!datosTipo || !Array.isArray(datosTipo.fechas) || !Array.isArray(datosTipo.ocupaciones)) {
      return;
    }
    if (datosTipo.fechas.length === 0) return;

    hayGraficos = true;
    const chartContainer = document.createElement('div');
    chartContainer.classList.add('bg-white', 'p-6', 'rounded-lg', 'shadow-md', 'w-full', 'mb-8');

    const chartTitle = document.createElement('h3');
    chartTitle.textContent = tipo;
    chartTitle.classList.add('text-xl', 'font-semibold', 'text-gray-800', 'mb-4', 'text-center');
    chartContainer.appendChild(chartTitle);

    const canvas = document.createElement('canvas');
    canvas.id = `chart-${index}`;
    canvas.style.height = '250px';
    canvas.style.width = '100%';
    chartContainer.appendChild(canvas);

    container.appendChild(chartContainer);

    const config = {
      type: 'bar',
      data: {
        labels: datosTipo.fechas,
        datasets: [
          {
            label: 'Ocupaciones',
            data: datosTipo.ocupaciones,
            backgroundColor: 'rgba(25, 118, 210, 0.3)',
            borderColor: '#1976d2',
            borderWidth: 1,
            yAxisID: 'y',
          },
          {
            label: 'Solicitudes',
            data: datosTipo.solicitudes || [],
            backgroundColor: 'rgba(255, 99, 132, 0.3)',
            borderColor: '#ff6384',
            borderWidth: 1,
            yAxisID: 'y1',
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'bottom',
          },
        },
        scales: {
          x: { title: { display: true, text: 'Mes' } },
          y: { title: { display: true, text: 'Ocupaciones' }, beginAtZero: true },
          y1: { title: { display: true, text: 'Solicitudes' }, beginAtZero: true, position: 'right', grid: { drawOnChartArea: false } },
        },
      },
    };

    new Chart(canvas.getContext('2d'), config);
  });

  if (!hayGraficos) {
    const noGraficos = document.getElementById('no-graficos');
    if (noGraficos) noGraficos.style.display = 'block';
  }
}

// Gráfico comparativo
const datosPlazasTodos = window.datosPlazasTodos || (typeof datos_plazas_todos !== "undefined" ? datos_plazas_todos : {});
const tiposComparativa = Object.keys(datosPlazasTodos);
const ocupados = tiposComparativa.map(tipo => {
  const plaza = datosPlazasTodos[tipo];
  return plaza.total > 0 ? Math.round((plaza.ocupadas / plaza.total) * 100) : 0;
});
const disponibles = tiposComparativa.map(tipo => {
  const plaza = datosPlazasTodos[tipo];
  return plaza.total > 0 ? Math.round((plaza.disponibles / plaza.total) * 100) : 0;
});

const graficoComparativo = document.getElementById('graficoComparativo');
if (graficoComparativo) {
  new Chart(graficoComparativo.getContext('2d'), {
    type: 'bar',
    data: {
      labels: tiposComparativa,
      datasets: [
        { label: 'Ocupación (%)', data: ocupados, backgroundColor: 'rgba(220, 38, 38, 0.7)' },
        { label: 'Disponibles (%)', data: disponibles, backgroundColor: 'rgba(22, 163, 74, 0.7)' }
      ]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { position: 'top', labels: { font: { size: 18 } } }
      },
      scales: {
        x: { beginAtZero: true, max: 100, ticks: { callback: value => value + '%', font: { size: 16 } } },
        y: { ticks: { font: { size: 18 }, color: '#222' } }
      }
    }
  });
}

const tiposPlaza = {{ tipos_plaza|tojson }};
const ocupadasPorTipo = {{ ocupadas_por_tipo|tojson }};
const disponiblesPorTipo = {{ disponibles_por_tipo|tojson }};
const labels = tiposPlaza;
const dataOcupadas = labels.map(tipo => ocupadasPorTipo[tipo]);
const dataDisponibles = labels.map(tipo => disponiblesPorTipo[tipo]);
const ctx = document.getElementById('graficoPlazas').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [
            {
                label: 'Ocupadas',
                data: dataOcupadas,
                backgroundColor: 'rgba(220, 38, 38, 0.7)'
            },
            {
                label: 'Disponibles',
                data: dataDisponibles,
                backgroundColor: 'rgba(22, 163, 74, 0.7)'
            }
        ]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { position: 'top' }
        },
        scales: {
            x: { ticks: { color: '#222', font: { size: 14 } } },
            y: { beginAtZero: true, ticks: { color: '#222', font: { size: 14 } } }
        }
    }
});

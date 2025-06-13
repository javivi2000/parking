const STORAGE_KEY = "plazasMatricula";
let plazasMatricula = cargarPlazasMatricula();

function cargarPlazasMatricula() {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
}

function guardarPlazasMatricula() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(plazasMatricula));
}

function getTipoPlaza(plazaId) {
    // Vehículos de Cruz Roja: 42, 43, 57-71
    const cruzRoja = [42, 43, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71];
    // Plaza asignada matrícula: 17,18,19,20,21,44,51,52,53,54,55,56
    const asignada = [17,18,19,20,21,44,51,52,53,54,55,56, 48,49 ];
    if (cruzRoja.includes(plazaId)) return "Vehículos de Cruz Roja";
    if (asignada.includes(plazaId)) return "Plaza asignada matrícula";
    return "";
}

// Intercepta el click en plazas de coche especiales (Cruz Roja, Asignada, M1, M2)
document.querySelectorAll('.parking-space, .moto-space-vertical-small').forEach(btn => {
    btn.addEventListener('click', function(e) {
        let plazaId, plazaNum, tipo;
        if (btn.classList.contains('parking-space')) {
            plazaId = parseInt(this.form.querySelector('input[name="space_id"]').value);
            plazaNum = this.querySelector('.plaza-numero') ? this.querySelector('.plaza-numero').textContent.trim() : "";
        } else {
            plazaId = parseInt(btn.getAttribute('data-moto-id'));
            plazaNum = btn.querySelector('span') ? btn.querySelector('span').textContent.trim() : "";
        }
        tipo = getTipoPlaza(plazaId);

        // Si es plaza especial (incluye M1/M2), pide matrícula al ocupar
        if (tipo) {
            if (btn.classList.contains('occupied')) {
                e.preventDefault();
                desocuparPlaza(plazaId);
                return;
            }
            e.preventDefault();
            mostrarModalMatricula(plazaId, plazaNum, tipo, this);
            return;
        }
        // Si no es ninguna de las anteriores, sigue el flujo normal (para motos normales)
    });
});

// Intercepta el click en plazas de moto normales para alternar estado sin matrícula
document.querySelectorAll('.moto-space-vertical-small').forEach(btn => {
    const plazaId = parseInt(btn.getAttribute('data-moto-id'));
    // Si es M1 o M2, no dejes ocupar sin matrícula 
    if ([48, 49].includes(plazaId)) return;
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        fetch(`/toggle_estado/${plazaId}`, { method: 'POST' })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    btn.classList.toggle('occupied', data.nuevo_estado);
                    btn.classList.toggle('free', !data.nuevo_estado);
                    const img = btn.querySelector('img');
                    if (img) {
                        img.src = data.nuevo_estado
                            ? "/static/bike-occupied.png"
                            : "/static/bike.png";
                        img.alt = data.nuevo_estado ? "Moto Ocupada" : "Moto";
                    }
                }
            });
    });
});

let lastClickedBtn = null;

function mostrarModalMatricula(plazaId, plazaNum, tipo, btn) {
    document.getElementById('matriculaModal').style.display = 'flex';
    document.getElementById('modalPlazaId').value = plazaId;
    document.getElementById('modalPlazaNum').value = plazaNum;
    document.getElementById('matriculaModal').setAttribute('data-tipo', tipo);
    document.getElementById('inputMatricula').value = '';
    document.getElementById('inputMatricula').focus();
    lastClickedBtn = btn; 
}
function cerrarModalMatricula() {
    document.getElementById('matriculaModal').style.display = 'none';
}

document.getElementById('btnGuardarMatricula').onclick = function() {
    const matricula = document.getElementById('inputMatricula').value.trim();
    const plazaNum = document.getElementById('modalPlazaNum').value;
    const plazaId = parseInt(document.getElementById('modalPlazaId').value);
    const tipo = document.getElementById('matriculaModal').getAttribute('data-tipo');
    if (matricula.length < 4) {
        alert('Introduce una matrícula válida');
        return;
    }
    plazasMatricula = plazasMatricula.filter(item => item.plazaId !== plazaId);
    plazasMatricula.push({plazaNum, matricula, tipo, plazaId});
    guardarPlazasMatricula();
    renderTablaPlazasMatricula();

    // Actualiza el estado en la base de datos
    fetch(`/toggle_estado/${plazaId}`, { method: 'POST' })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                marcarPlazaComoOcupada(plazaId);
            }
        });

    cerrarModalMatricula();
};

function marcarPlazaComoOcupada(plazaId) {
    document.querySelectorAll('.parking-space').forEach(btn => {
        const input = btn.form.querySelector('input[name="space_id"]');
        if (input && parseInt(input.value) === plazaId) {
            btn.classList.remove('free');
            btn.classList.add('occupied');
            if (!btn.querySelector('img')) {
                const img = document.createElement('img');
                img.src = carIconUrl();
                img.alt = "Coche";
                img.style = "width:30px; height:30px; display:block; margin:0 auto 4px;";
                btn.insertBefore(img, btn.querySelector('.plaza-numero'));
            }
        }
    });
}

function carIconUrl() {
    const exampleImg = document.querySelector('img[alt="Coche"]');
    return exampleImg ? exampleImg.src : '/static/car.png';
}

function renderTablaPlazasMatricula() {
    const tbody = document.getElementById('tbodyPlazasMatricula');
    tbody.innerHTML = '';
    plazasMatricula.forEach(item => {
        let color = '';
        if (item.tipo === "Vehículos de Cruz Roja") color = 'style="color:#c00;font-weight:bold"';
        if (item.tipo === "Plaza asignada matrícula") color = 'style="color:#e6b800;font-weight:bold"';
        const tr = document.createElement('tr');
        tr.innerHTML = `<td>${item.plazaNum}</td><td>${item.matricula}</td><td ${color}>${item.tipo}</td>`;
        tbody.appendChild(tr);
    });
    const tabla = document.getElementById('tablaPlazasMatricula');
    const nota = document.getElementById('notaMatricula');
    if (plazasMatricula.length) {
        tabla.style.display = 'block';
        if (nota) nota.style.display = 'none';
    } else {
        tabla.style.display = 'none';
        if (nota) nota.style.display = '';
    }
}

// Permite desocupar la plaza manualmente (elimina la matrícula y la deja libre visualmente)
function desocuparPlaza(plazaId) {
    plazaId = parseInt(plazaId);
    plazasMatricula = plazasMatricula.filter(item => parseInt(item.plazaId) !== plazaId);
    guardarPlazasMatricula();
    renderTablaPlazasMatricula();

    // Actualiza el estado en la base de datos
    fetch(`/toggle_estado/${plazaId}`, { method: 'POST' })
        .then(r => r.json())
        .then(data => {
            if (data.success) {
                marcarPlazaComoLibre(plazaId);
            }
        });
}

function marcarPlazaComoLibre(plazaId) {
    document.querySelectorAll('.parking-space').forEach(btn => {
        const input = btn.form.querySelector('input[name="space_id"]');
        if (input && parseInt(input.value) === plazaId) {
            btn.classList.remove('occupied');
            btn.classList.add('free');
            const img = btn.querySelector('img');
            if (img) img.remove();
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {
    renderTablaPlazasMatricula();
});

document.querySelectorAll('form[action^="/toggle_estado/"]').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const url = form.action;
        fetch(url, { method: 'POST' })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    // Alterna la clase visual de ocupado/libre
                    const btn = form.querySelector('button');
                    btn.classList.toggle('occupied', data.nuevo_estado);
                    btn.classList.toggle('free', !data.nuevo_estado);
                    // Cambia el icono de la moto
                    const img = btn.querySelector('img');
                    if (img) {
                        img.src = data.nuevo_estado
                            ? "{{ url_for('static', filename='bike-occupied.png') }}"
                            : "{{ url_for('static', filename='bike.png') }}";
                        img.alt = data.nuevo_estado ? "Moto Ocupada" : "Moto";
                    }
                }
            });
    });
});


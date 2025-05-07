from flask import Blueprint, render_template, request, redirect, url_for, jsonify

from .models import ParkingSpace

routes = Blueprint('routes', __name__)

# Ajusta los IDs para que no se repitan y sigan un orden lógico
layout = {
    # 10 plazas superiores (gris, entre rampas)
    "superior": [ParkingSpace(id=i) for i in range(1, 11)],
    # Bloque azul (izquierda, 12 plazas)
    "bloque_izq": [ParkingSpace(id=i) for i in range(11, 23)],
    # Bloque verde (derecha, 12 plazas)
    "bloque_der": [ParkingSpace(id=i) for i in range(23, 45)],
    # Plazas inferiores (gris, 16 plazas)
    "inferior": [ParkingSpace(id=i) for i in range(45, 78)],
}

@routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        space_id = int(request.form['space_id'])
        for block in layout.values():
            for space in block:
                if space.id == space_id:
                    space.occupied = not space.occupied
        return redirect(url_for('routes.index'))
    return render_template('index.html', layout=layout)

parking_spaces = [space for block in layout.values() for space in block]

@routes.route('/occupy/<int:space_id>', methods=['POST'])
def occupy(space_id):
    space = next((s for s in parking_spaces if s.id == space_id), None)
    if space and not space.occupied:
        space.occupy()
        return jsonify({'status': 'success', 'message': 'Space occupied.'})
    return jsonify({'status': 'error', 'message': 'Space already occupied or does not exist.'})

@routes.route('/free/<int:space_id>', methods=['POST'])
def free(space_id):
    space = next((s for s in parking_spaces if s.id == space_id), None)
    if space and space.occupied:
        space.free()
        return jsonify({'status': 'success', 'message': 'Space freed.'})
    return jsonify({'status': 'error', 'message': 'Space not occupied or does not exist.'})

@routes.route('/toggle/<int:space_id>', methods=['POST'])
def toggle(space_id):
    for block in layout.values():
        for space in block:
            if space.id == space_id:
                space.occupied = not space.occupied
                break
    return redirect(url_for('routes.index'))
# app/notes.py

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from . import db
from .models import Note

notes_bp = Blueprint('notes', __name__)

def _to_dict(n):
    return {
        'id': n.id,
        'content': n.content,
        'bg_color': n.bg_color,
        'x': n.x, 'y': n.y,
        'width': n.width, 'height': n.height,
        'is_flashcard': n.is_flashcard,
        'front_content': n.front_content,
        'back_content': n.back_content,
        'created_at': n.created_at.isoformat(),
        'updated_at': n.updated_at.isoformat()
    }

@notes_bp.route('', methods=['GET'])
@login_required
def list_notes():
    unit = request.args.get('unit', type=int)
    notes = Note.query.filter_by(user_id=current_user.id, unit_id=unit).all()
    return jsonify([_to_dict(n) for n in notes])

@notes_bp.route('', methods=['POST'])
@login_required
def create_note():
    data = request.json
    note = Note(
        user_id=current_user.id,
        unit_id=data['unit_id'],
        content=data.get('content',''),
        bg_color=data.get('bg_color','#fffb85'),
        x=data.get('x',50), y=data.get('y',50),
        width=data.get('width',200), height=data.get('height',200)
    )
    db.session.add(note)
    db.session.commit()
    return jsonify(_to_dict(note)), 201

@notes_bp.route('/<int:id>', methods=['PUT'])
@login_required
def update_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        return jsonify(error='Forbidden'), 403
    for f in ('content','bg_color','x','y','width','height'):
        if f in request.json:
            setattr(note, f, request.json[f])
    db.session.commit()
    return jsonify(_to_dict(note))

@notes_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_note(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        return jsonify(error='Forbidden'), 403
    db.session.delete(note)
    db.session.commit()
    return '', 204

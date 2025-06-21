# run.py

from flask import render_template
from flask_login import login_required
from app import create_app
from app.models import Unit

app = create_app()

@app.route('/unit/<int:unit_id>')
@login_required
def view_unit(unit_id):
    unit = Unit.query.get_or_404(unit_id)
    return render_template('unit.html', unit=unit)

if __name__ == '__main__':
    app.run(debug=True)

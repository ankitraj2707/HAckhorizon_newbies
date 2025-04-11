from flask import Flask, jsonify, request
from models import db, Scheme
from config import Config

app = Flask(_name_)
app.config.from_object(Config)
db.init_app(app)

@app.before_first_request   
def create_tables():
    db.create_all()

@app.route('/schemes', methods=['GET'])
def get_schemes():
    schemes = Scheme.query.all()
    return jsonify([{'id': scheme.id, 'name': scheme.name, 'description': scheme.description} for scheme in schemes])

@app.route('/schemes', methods=['POST'])
def add_scheme():
    data = request.get_json()
    new_scheme = Scheme(name=data['name'], description=data['description'])
    db.session.add(new_scheme)
    db.session.commit()
    return jsonify({'id': new_scheme.id, 'name': new_scheme.name, 'description': new_scheme.description}), 201

@app.route('/schemes/<int:id>', methods=['PUT'])
def update_scheme(id):
    data = request.get_json()
    scheme = Scheme.query.get_or_404(id)
    scheme.name = data['name']
    scheme.description = data['description']
    db.session.commit()
    return jsonify({'id': scheme.id, 'name': scheme.name, 'description': scheme.description})

@app.route('/schemes/<int:id>', methods=['DELETE'])
def delete_scheme(id):
    scheme = Scheme.query.get_or_404(id)
    db.session.delete(scheme)
    db.session.commit()
    return jsonify({'message': 'Scheme deleted successfully'})

if _name_ == '_main_':
    app.run(debug=True)
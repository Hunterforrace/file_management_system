from flask import Blueprint, request, jsonify
from models import db, Folder, File

folder_routes = Blueprint('folder_routes', __name__)

@folder_routes.route('/folders', methods=['POST'])
def create_folder():
    data = request.json
    name = data.get('name')
    parent_id = data.get('parent_id')
    
    if not name:
        return jsonify({'error': 'Folder name is required'}), 400
    
    parent_folder = Folder.query.get(parent_id) if parent_id else None
    new_folder = Folder(name=name, parent=parent_folder)
    db.session.add(new_folder)
    db.session.commit()
    
    return jsonify({'message': 'Folder created', 'folder': {'id': new_folder.id, 'name': new_folder.name}}), 201

@folder_routes.route('/folders/<int:folder_id>', methods=['PUT'])
def rename_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    data = request.json
    folder.name = data.get('name', folder.name)
    db.session.commit()
    return jsonify({'message': 'Folder renamed', 'folder': {'id': folder.id, 'name': folder.name}})

@folder_routes.route('/folders/<int:folder_id>', methods=['DELETE'])
def delete_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    delete_recursively(folder)
    db.session.commit()
    return jsonify({'message': 'Folder and its contents deleted'})

def delete_recursively(folder):
    for file in folder.files:
        db.session.delete(file)
    for subfolder in folder.subfolders:
        delete_recursively(subfolder)
    db.session.delete(folder)

@folder_routes.route('/files', methods=['POST'])
def create_file():
    data = request.json
    name = data.get('name')
    folder_id = data.get('folder_id')
    
    if not name or not folder_id:
        return jsonify({'error': 'File name and folder ID are required'}), 400
    
    new_file = File(name=name, folder_id=folder_id)
    db.session.add(new_file)
    db.session.commit()
    
    return jsonify({'message': 'File created', 'file': {'id': new_file.id, 'name': new_file.name}}), 201

@folder_routes.route('/files/<int:file_id>', methods=['PUT'])
def rename_file(file_id):
    file = File.query.get_or_404(file_id)
    data = request.json
    file.name = data.get('name', file.name)
    db.session.commit()
    return jsonify({'message': 'File renamed', 'file': {'id': file.id, 'name': file.name}})

@folder_routes.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    db.session.delete(file)
    db.session.commit()
    return jsonify({'message': 'File deleted'})

@folder_routes.route('/folders/<int:folder_id>/contents', methods=['GET'])
def list_folder_contents(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    contents = {
        'folders': [{'id': f.id, 'name': f.name} for f in folder.subfolders],
        'files': [{'id': f.id, 'name': f.name} for f in folder.files]
    }
    return jsonify(contents)

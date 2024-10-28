from flask import Blueprint, jsonify, request
from api.models.alunos_model import AlunoNaoEncontrado, aluno_por_id, listar_alunos, adicionar_aluno, atualizar_aluno, excluir_aluno

alunos_bp = Blueprint('alunos', __name__)

# Rota para lista todos os alunos
@alunos_bp.route('/alunos', methods=['GET'])
def get_alunos():
    return jsonify(listar_alunos())

# Rota para listar um aluno específico
@alunos_bp.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return jsonify(aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
    
# Rota para criar o professor
@alunos_bp.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.json
    adicionar_aluno(data)
    return jsonify({'message': 'Aluno criado com sucesso!'}), 201

# Rota para atualizar o aluno
@alunos_bp.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    novos_dados = request.json
    try:
        atualizar_aluno(id_aluno, novos_dados)
        return jsonify({'message': 'Aluno atualizado com sucesso!'}), 200
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404

# Rota para excluir o aluno
@alunos_bp.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return ({'message': 'Aluno deletado com sucesso!'}), 200
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'}), 404
# Controllers: onde fica a lógica dos endpoints
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from api.models.turmas_model import db, Turma, TurmaNaoEncontrada, turma_por_id, listar_turmas, adicionar_turma, atualizar_turma, excluir_turma
from api.models.professores_model import Professor

turmas_bp = Blueprint('turmas', __name__)

# Rota para lista todas as turmas
@turmas_bp.route('/turmas', methods=['GET'])
def get_turmas():
    turmas = listar_turmas()
    return render_template('turmas/lista_turmas.html', turmas=turmas)

# Rota para listar uma turma específica
@turmas_bp.route('/turmas/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turmas/id_turma.html', turma=turma)
    except TurmaNaoEncontrada:
        return render_template('turmas/404.html'), 404

# Rota para exibir o formulário de criação da turma
@turmas_bp.route('/turmas/novo', methods=['GET'])
def nova_turma():
    # Busque a lista de professores para preencher um dropdown ou select no formulário
    professores = Professor.query.all() 
    return render_template('turmas/criar_turma.html', professores=professores)

# Função para adicionar a turma ao banco de dados
def adicionar_turma(data):
    turma = Turma(**data)
    db.session.add(turma)
    db.session.commit()

# Rota para criar a turma
@turmas_bp.route('/turmas', methods=['POST'])
def create_turma():
    data = request.form
    nova_turma = {
        "descricao": data.get('descricao'),
        "professor_id": int(data.get('professor')),  # Certifique-se de que o campo é um inteiro
        "ativo": data.get('ativo') == 'on'  # Convertendo checkbox para booleano
    }
    adicionar_turma(nova_turma)
    return redirect(url_for('turmas.get_turmas')) 

# Rota para atualizar a turma
@turmas_bp.route('/turmas/<int:id_turma>', methods=['PUT'])
def update_turma(id_turma):
    novos_dados = request.json
    try:
        atualizar_turma(id_turma, novos_dados)
        return jsonify({'message': 'Turma atualizada com sucesso!'}), 200
    except TurmaNaoEncontrada:
        return render_template('turmas/404.html'), 404
    
# Rota para excluir uma turma
@turmas_bp.route('/turmas/<int:id_turma>', methods=['DELETE'])
def delete_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return ({'message': 'Turma deletada com sucesso!'}), 200
    except TurmaNaoEncontrada:
        return render_template('turmas/404.html'), 404
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from api.models.alunos_model import Aluno, db, AlunoNaoEncontrado, aluno_por_id, listar_alunos, adicionar_aluno, atualizar_aluno, excluir_aluno
from datetime import datetime

alunos_bp = Blueprint('alunos', __name__)

# Rota para lista todos os alunos
@alunos_bp.route('/alunos', methods=['GET'])
def get_aluno():
    alunos = listar_alunos()
    return render_template('alunos/lista_alunos.html', alunos=alunos)

# Rota para listar um aluno específico
@alunos_bp.route('/alunos/<int:id_aluno>', methods=['GET'])
def get_aluno_by_id(id_aluno):
    try:
        aluno = aluno_por_id(id_aluno)
        return render_template('alunos/id_aluno.html', aluno=aluno)
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'})

# Rota para exibir o formulário de criação do aluno
@alunos_bp.route('/alunos/novo', methods=['GET'])
def novo_aluno():
    return render_template('alunos/criar_aluno.html')

# Função para adicionar o aluno ao banco de dados
def adicionar_aluno(data):
    aluno = Aluno(**data)
    db.session.add(aluno)
    db.session.commit()

# Rota para criar o aluno
@alunos_bp.route('/alunos', methods=['POST'])
def create_aluno():
    data = request.form  # Recebendo dados do formulário
    novo_aluno = {
        "nome": data.get('nome'),
        "idade": int(data.get('idade')),
        "turma_id": int(data.get('turma')),
        "data_nascimento": data.get('data_nascimento'),
        "nota_primeiro_semestre": float(data.get('nota_primeiro_semestre')) if data.get('nota_primeiro_semestre') else None,
        "nota_segundo_semestre": float(data.get('nota_segundo_semestre')) if data.get('nota_segundo_semestre') else None
    }
    # Converter a data de nascimento de string para datetime
    if isinstance(novo_aluno['data_nascimento'], str):
        novo_aluno['data_nascimento'] = datetime.strptime(novo_aluno['data_nascimento'], '%Y-%m-%d').date()

    adicionar_aluno(novo_aluno)
    return redirect(url_for('alunos.get_aluno'))

# Rota para atualizar o aluno
@alunos_bp.route('/alunos/<int:id_aluno>', methods=['PUT'])
def update_aluno(id_aluno):
    novos_dados = request.json
    try:
        atualizar_aluno(id_aluno, novos_dados)
        return jsonify({'message': 'Aluno atualizado com sucesso!'})
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'})

# Rota para excluir o aluno
@alunos_bp.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def delete_aluno(id_aluno):
    try:
        excluir_aluno(id_aluno)
        return ({'message': 'Aluno deletado com sucesso!'})
    except AlunoNaoEncontrado:
        return jsonify({'message': 'Aluno não encontrado'})
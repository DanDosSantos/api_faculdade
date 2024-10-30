# Controllers: onde fica a lógica dos endpoints
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from api.models.professores_model import ProfessorNaoEncontrado, professor_por_id, listar_professores, adicionar_professor, atualizar_professor, excluir_professor

professores_bp = Blueprint('professores', __name__)

@professores_bp.route('/', methods=['GET'])
def api():
    return 'A API está rodando'

# Rota para lista todos os professores
@professores_bp.route('/professores', methods=['GET'])
def get_professor():
    professores = listar_professores()
    return render_template('professores/lista_professores.html', professores=professores)

# Rota para listar um professor específico
@professores_bp.route('/professores/<int:id_professor>', methods=['GET'])
def get_professor_by_id(id_professor):
    try:
        professor = professor_por_id(id_professor)
        return render_template('professores/id_professor.html', professor=professor)
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404
    
# Rota para exibir o formulário de criação do professor
@professores_bp.route('/professores/novo', methods=['GET'])
def novo_professor():
    return render_template('professores/criar_professor.html')

# Rota para criar o professor
@professores_bp.route('/professores', methods=['POST'])
def create_professor():
    data = request.form
    try:
        novo_professor = {
            "nome": data.get('nome'),
            "idade": int(data.get('idade')) if data.get('idade') is not None else None,
            "materia": data.get('materia'),
            "observacoes": data.get('observacoes')
        }

        # Verifica se todos os campos obrigatórios estão preenchidos
        if None in novo_professor.values():
            return "Todos os campos são obrigatórios.", 400

        adicionar_professor(novo_professor)
        return redirect(url_for('professores.get_professor'))
    except ValueError:
        return "Erro ao processar os dados do professor.", 400

# Rota para atualizar o professor
@professores_bp.route('/professores/<int:id_professor>', methods=['PUT'])
def update_professor(id_professor):
    novos_dados = request.json
    try:
        atualizar_professor(id_professor, novos_dados)
        return jsonify({'message': 'Professor atualizado com sucesso!'}), 200
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404

# Rota para excluir o professor
@professores_bp.route('/professores/<int:id_professor>', methods=['DELETE'])
def delete_professor(id_professor):
    try:
        excluir_professor(id_professor)
        return ({'message': 'Professor deletado com sucesso!'}), 200
    except ProfessorNaoEncontrado:
        return jsonify({'message': 'Professor não encontrado'}), 404
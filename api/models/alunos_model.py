from config import db
from datetime import datetime

class Aluno(db.Model):
    __tablename__ = 'alunos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=True)
    nota_segundo_semestre = db.Column(db.Float, nullable=True)
    media = db.Column(db.Float, nullable=True)

    # Relacionamento com o modelo Turma
    turma = db.relationship('Turma', back_populates='alunos')

    def __init__(self, nome, idade, turma_id, data_nascimento, nota_primeiro_semestre=None, nota_segundo_semestre=None):
        self.nome = nome
        self.idade = idade
        self.turma_id = turma_id
        self.data_nascimento = data_nascimento
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.media = self.calcular_media()

    def calcular_media(self):
        if self.nota_primeiro_semestre is not None and self.nota_segundo_semestre is not None:
            return (self.nota_primeiro_semestre + self.nota_segundo_semestre) / 2
        return None

    def to_dict(self):
        return {
            'id': self.id, 
            'nome': self.nome,
            'data_nascimento': self.data_nascimento.strftime('%Y-%m-%d'),
            'turma': self.turma.descricao if self.turma else None,
            'idade': self.idade,
            'nota_primeiro_semestre': self.nota_primeiro_semestre,
            'nota_segundo_semestre': self.nota_segundo_semestre,
            'media': self.media
            }

class AlunoNaoEncontrado(Exception):
    pass

def aluno_por_id(id_aluno):
    aluno = db.session.get(Aluno, id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno.to_dict()

def listar_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dict() for aluno in alunos]

def adicionar_aluno(aluno_data):
    # Converter a string de data para um objeto date
    data_nascimento = datetime.strptime(aluno_data['data_nascimento'], '%Y-%m-%d').date()
    
    novo_aluno = Aluno(
        nome=aluno_data['nome'],
        idade=aluno_data['idade'],
        turma_id=aluno_data['turma_id'],
        data_nascimento=data_nascimento,  # Usando o objeto date aqui
        nota_primeiro_semestre=aluno_data['nota_primeiro_semestre'],
        nota_segundo_semestre=aluno_data['nota_segundo_semestre'],
    )
    db.session.add(novo_aluno)
    db.session.commit()

def atualizar_aluno(id_aluno, novos_dados):
    aluno = db.session.get(Aluno, id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    aluno.nome = novos_dados['nome']
    db.session.commit()

def excluir_aluno(id_aluno):
    aluno = db.session.get(Aluno, id_aluno)
    if not aluno:
        raise AlunoNaoEncontrado
    db.session.delete(aluno)
    db.session.commit()
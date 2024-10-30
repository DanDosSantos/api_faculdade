from config import db

class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(100))
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)
    ativo = db.Column(db.Boolean())

    # Relacionamento com o modelo Professor
    professor = db.relationship('Professor', back_populates='turmas')
    # Relacionamento com o modelo Turma
    alunos = db.relationship('Aluno', back_populates='turma', cascade="all, delete-orphan")

    def __init__(self, descricao, professor_id, ativo):
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo


    def to_dict(self):
        return {
            'id': self.id, 
            'descricao': self.descricao,
            'nome_do_professor': self.professor.nome,
            'ativo': self.ativo
            }

class TurmaNaoEncontrada(Exception):
    pass

def listar_turmas():
    turmas = Turma.query.all()
    return [turma.to_dict() for turma in turmas]

def turma_por_id(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    return turma.to_dict()

def adicionar_turma(turma_data):
    nova_turma = Turma(
        descricao=turma_data['descricao'],
        professor_id=turma_data['professor_id'],
        ativo=turma_data['ativo']
        )
    db.session.add(nova_turma)
    db.session.commit()

def atualizar_turma(id_turma, novos_dados):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    turma.descricao = novos_dados.get('descricao', turma.descricao)
    turma.professor_id = novos_dados.get('professor_id', turma.professor_id)
    turma.ativo = novos_dados.get('ativo', turma.ativo)
    db.session.commit()
    return turma

def excluir_turma(id_turma):
    turma = Turma.query.get(id_turma)
    if not turma:
        raise TurmaNaoEncontrada
    db.session.delete(turma)
    db.session.commit()

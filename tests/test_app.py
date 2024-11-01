import unittest
from app import app, db 
from api.models.alunos_model import Aluno
from datetime import date
import json

class AlunoTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Banco em memória
        cls.client = app.test_client()

        with app.app_context():
            db.create_all()  # Cria as tabelas no banco em memória para os testes

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()  # Limpa o banco após todos os testes

    def setUp(self):
        with app.app_context():
            aluno = Aluno(
                nome="Teste Aluno",
                idade=20,
                turma_id=1,
                data_nascimento=date(2003, 1, 1)  # Converte a data para um objeto date
            )
            db.session.add(aluno)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()


    def test_create_aluno(self):
        response = self.client.post('/alunos', data={
            'nome': 'Novo Aluno',
            'idade': 21,
            'turma': 1,
            'data_nascimento': '2003-01-01'
        })
        self.assertEqual(response.status_code, 302)  # Confirma redirecionamento após criação

    def test_get_alunos(self):
        response = self.client.get('/alunos')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Teste Aluno', response.data)  # Verifica se o aluno de teste está na lista

    def test_update_aluno(self):
        with app.app_context():
            aluno = Aluno.query.first()  # Obtém o primeiro aluno para atualização
            aluno_id = aluno.id

    # Faz uma solicitação PUT para atualizar o aluno com JSON e o Content-Type apropriado
            response = self.client.put(f'/alunos/{aluno_id}', 
                                    data=json.dumps({
                                        'nome': 'Aluno Atualizado',
                                        'idade': 22,
                                        'turma': 1,
                                        'data_nascimento': '2002-01-01'
                                    }),
                                    content_type='application/json')  # Define o tipo de conteúdo
            self.assertEqual(response.status_code, 200)  # Verifica o status da resposta

    def test_delete_aluno(self):
        with app.app_context():
            aluno = Aluno.query.first()  # Obtém o primeiro aluno para exclusão
            aluno_id = aluno.id

        # Faz uma solicitação DELETE para excluir o aluno
        response = self.client.delete(f'/alunos/{aluno_id}')
        self.assertEqual(response.status_code, 200)  # Verifica o status da resposta

        # Verifica se o aluno foi removido do banco de dados
        with app.app_context():
            aluno_deletado = Aluno.query.get(aluno_id)
            self.assertIsNone(aluno_deletado)


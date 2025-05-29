import unittest
from unittest.mock import patch, mock_open
from gerenciador import GerenciadorTarefas 
from tarefa import Tarefa
from io import StringIO
import os


class TestGerenciadorTarefas(unittest.TestCase):

    def setUp(self):
        self.test_filepath = 'test_tarefas.csv'
        if os.path.exists(self.test_filepath):
            os.remove(self.test_filepath)
    
    def tearDown(self):
        if os.path.exists(self.test_filepath):
            os.remove(self.test_filepath)

    

#Iniciar gerenciador

    #1 arquivo valido
    @patch('builtins.open', new_callable=mock_open, read_data="id,descricao,status\n1,Tarefa de teste,Pendente")
    def test_iniciar_gerenciador_com_arquivo_valido(self, _mock_file):
        fake_out = StringIO()
        with patch('sys.stdout', new=fake_out):
            gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        output = fake_out.getvalue()
        self.assertIsInstance(gerenciador, GerenciadorTarefas)
        self.assertEqual(gerenciador._filepath, self.test_filepath)
        self.assertEqual(len(gerenciador.listar_tarefas()), 1)
        tarefa = gerenciador.listar_tarefas()[0]
        self.assertEqual(tarefa.id, 1)
        self.assertEqual(tarefa.descricao, "Tarefa de teste")
        self.assertEqual(tarefa.status, Tarefa.STATUS_PENDENTE)
        self.assertEqual(gerenciador._proximo_id, 2)
        self.assertIn(f"Tarefas carregadas de '{self.test_filepath}'. Próximo ID: 2", output) #mensagem validacao

        
    #2 arquivo inválido, malformado
    @patch('builtins.open', new_callable=mock_open, read_data="id,name\n1,Tarefa sem descricao") 
    def test_iniciar_gerenciador_com_arquivo_invalido(self, _mock_file):
        fake_out = StringIO()
        with patch('sys.stdout', new=fake_out):
            gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        output = fake_out.getvalue()
        self.assertEqual(len(gerenciador.listar_tarefas()), 0)
        self.assertEqual(gerenciador._filepath, self.test_filepath)
        self.assertEqual(gerenciador._tarefas, [])
        self.assertEqual(gerenciador._proximo_id, 1)
        self.assertIn(f"Linha 1 ignorada no CSV por falta de colunas esperadas ({self.test_filepath}). Conteúdo: {{'id': '1', 'name': 'Tarefa sem descricao'}}", output)

    #3 sem arquivo
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_iniciar_gerenciador_sem_arquivo(self, _mock_file):
        fake_out = StringIO()
        with patch('sys.stdout', new=fake_out):
            gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        output = fake_out.getvalue()
        self.assertIsInstance(gerenciador, GerenciadorTarefas)
        self.assertEqual(gerenciador._filepath, self.test_filepath)  #valida que não existe
        self.assertEqual(len(gerenciador.listar_tarefas()), 0)  #lista vazia
        self.assertEqual(gerenciador._tarefas, [])  #garantia que não há tarefas
        self.assertEqual(gerenciador._proximo_id, 1)  #garantia que o próximo id é 1
        self.assertIn(f"Arquivo '{self.test_filepath}' não encontrado. Começando com lista de tarefas vazia.", output) #mensagem validacao


    #4 arquivo vazio
    @patch('builtins.open', new_callable=mock_open, read_data="") 
    def test_iniciar_gerenciador_com_arquivo_vazio(self, _mock_file):
        fake_out = StringIO()
        with patch('sys.stdout', new=fake_out):
            gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
            output = fake_out.getvalue()
            self.assertEqual(len(gerenciador.listar_tarefas()), 0)
            self.assertEqual(gerenciador._filepath, self.test_filepath) #valida que não existe
            self.assertEqual(gerenciador._tarefas, []) #garantia que não há tarefas
            self.assertEqual(gerenciador._proximo_id, 1)  #garantia que o próximo id é 1
            self.assertIn(f"Tarefas carregadas de '{self.test_filepath}'. Próximo ID: 1", output) #mensagem validacao
        

    #5 arquivo com status inválido
    @patch('builtins.open', new_callable=mock_open, read_data="id,descricao,status\n1,Tarefa errada,Em andamento")
    def test_iniciar_gerenciador_com_status_invalido(self, _mock_file):
        fake_out = StringIO()
        with patch('sys.stdout', new=fake_out): # Captura a saída padrão para verificar as mensagens de aviso
            gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
            output = fake_out.getvalue()
            self.assertEqual(len(gerenciador.listar_tarefas()), 0) #garantia que não há tarefas
            self.assertEqual(gerenciador._filepath, self.test_filepath)
            self.assertEqual(gerenciador._proximo_id, 1) #garantia que o próximo id é 1
            self.assertEqual(gerenciador._tarefas, []) #garantia que não há tarefas
            self.assertIn("Status inválido: Em andamento. Use 'Pendente' ou 'Concluída'.", output) #mensagem validacao1
            self.assertIn(f"Erro ao processar linha 1 do CSV ({self.test_filepath})", output) #mensagem validacao2
                

#Adicionar

    #6 adicionar nova tarefa
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas') #o motivo que utilizei o _salvar_tarefas foi para salvar a nova tarefa adicionada, por sugestão do gemini
    def test_adicionar_nova_tarefa_valida(self, mock_salvar, _mock_file):
        gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        gerenciador.adicionar_tarefa("Nova Tarefa")
        self.assertEqual(len(gerenciador._tarefas), 1)  
        self.assertEqual(gerenciador._tarefas[0].descricao, "Nova Tarefa")
        self.assertEqual(gerenciador._tarefas[0].status, Tarefa.STATUS_PENDENTE) #garantir que não tem trf pendente
        self.assertEqual(gerenciador._proximo_id, 2) #garantir que o proximo id será 2, já que o 1 foi criado
        mock_salvar.assert_called_once() #garantir que a funcao foi chamada


    #7 adicionar tarefa invalida
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_adicionar_nova_tarefa_invalida(self, _mock_salvar, _mock_file):
        gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        with self.assertRaises(ValueError) as context:
            gerenciador.adicionar_tarefa("")
            self.assertEqual(str(context.exception), "A descrição da tarefa não pode ser vazia.")
            self.assertEqual(len(gerenciador._tarefas), 0) #permanece 0 tarefas
            self.assertEqual(gerenciador._proximo_id, 1) #proximo id deve ser 1 para mostrar que nada foi salvo anteriormente

    
#Remover tarefa

    #8 Remover tarefa existente
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_remover_tarefa_existente(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        tarefa = gerenciador.adicionar_tarefa("Tarefa Existente")
        gerenciador.remover_tarefa(tarefa.id) 
        self.assertEqual(len(gerenciador._tarefas), 0) #garantir que não há tarefas
        self.assertEqual(gerenciador._proximo_id, 2) #garantir que o proximo id é 1
        self.assertNotIn(tarefa, gerenciador._tarefas) #garantir que a tarefa foi removida
        self.assertEqual(_mock_salvar.call_count, 2) #garantir que a funcao foi chamada

    #9 Remover tarefa inexistente
    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_remover_tarefa_inexistente(self, _mock_open):
        gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        with self.assertRaisesRegex(ValueError, r"Erro: Tarefa com ID \d+ não encontrada para remoção."):
            gerenciador.remover_tarefa(999)
            gerenciador.remover_tarefa(0)
        self.assertEqual(len(gerenciador._tarefas), 0)
        self.assertEqual(gerenciador._proximo_id, 1)


#Listar tarefas

    #10 Listar tarefas vazias | adicionei mais funcionalidades no teste
    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_listar_tarefas_vazia(self, _mock_open):
        gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        tarefas = gerenciador.listar_tarefas()
        self.assertEqual(tarefas, []) #nenhuma tarefa carregada
        self.assertEqual(gerenciador._proximo_id, 1) #id inicial 1
        self.assertEqual(gerenciador._tarefas, []) #garantir que a lista está vazia 
        self.assertIsInstance(gerenciador, GerenciadorTarefas)
        self.assertEqual(gerenciador._filepath, self.test_filepath) #valida que não existe


    #11 Listar tarefas pendentes 
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_listar_tarefas_pendentes(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        gerenciador.adicionar_tarefa("Tarefa Pendente 1")
        gerenciador.adicionar_tarefa("Tarefa Pendente 2")
        gerenciador.adicionar_tarefa("Tarefa Pendente 3")
        gerenciador.marcar_como_concluida(3) #concluí a tarefa numero 3

        tarefas_pendentes = gerenciador.listar_tarefas_pendentes() #busca as pendentes
        tarefas_concluidas = gerenciador.listar_tarefas_concluidas() #busca as concluidas

        self.assertEqual(len(tarefas_pendentes), 2) #mostra que restaram 2 pendentes
        self.assertEqual(len(tarefas_concluidas), 1) #mostra que 1 foi marcada concluida
        
        for tarefa in tarefas_pendentes:
            self.assertEqual(tarefa.status, Tarefa.STATUS_PENDENTE) #garantir que status é pendente

        for tarefa in tarefas_concluidas:
            self.assertEqual(tarefa.status, Tarefa.STATUS_CONCLUIDA) #garantir que status é concluida

        self.assertEqual(tarefas_concluidas[0].descricao, "Tarefa Pendente 3")  #tem descricao correta
        self.assertEqual(tarefas_concluidas[0].status, Tarefa.STATUS_CONCLUIDA) #tem status correto
        self.assertEqual(gerenciador._proximo_id, 4) #proximo id deve ser 4
        self.assertEqual(_mock_salvar.call_count, 4) #garantir que funcao foi chamada


    #12 Listar tarefas concluídas
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_listar_tarefas_concluidas(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        gerenciador.adicionar_tarefa("Tarefa Concluída 1")
        gerenciador.marcar_como_concluida(1)
        tarefas_concluidas = gerenciador.listar_tarefas_concluidas()
        self.assertEqual(len(tarefas_concluidas), 1)
        self.assertEqual(tarefas_concluidas[0].descricao, "Tarefa Concluída 1")
        self.assertEqual(tarefas_concluidas[0].status, Tarefa.STATUS_CONCLUIDA)
        self.assertEqual(gerenciador._proximo_id, 2) #verifica que proximo id é 2
        self.assertEqual(_mock_salvar.call_count, 2) #verifica que a funcao foi chamada ao adicionar tarefa e ao marca-la como concluida


    #Listar todas as tarefas
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_listas_todas_tarefas(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        gerenciador.adicionar_tarefa("Tarefa 1")
        gerenciador.adicionar_tarefa("Tarefa 2")
        tarefas = gerenciador.listar_tarefas()
        self.assertEqual(len(tarefas), 2)
        self.assertEqual(tarefas[0].descricao, "Tarefa 1")
        self.assertEqual(tarefas[1].descricao, "Tarefa 2")
        self.assertEqual(gerenciador._proximo_id, 3) #verifica que proximo id é 3
        self.assertEqual(_mock_salvar.call_count, 2) #verifica que a funcao foi chamada ao adicionar tarefa e ao marca-la como concluida

#Buscar tarefa por id

    #Buscar por id
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_buscar_tarefa_por_id_existente(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas()
        tarefa_adicionada = gerenciador.adicionar_tarefa("Tarefa Existente") #recebe id 1 por ser a primeira tarefa
        tarefa_encontrada = gerenciador._buscar_tarefa_por_id(tarefa_adicionada.id)
        self.assertIsNotNone(tarefa_encontrada) #trf encontrada pelo id
        self.assertEqual(tarefa_encontrada.descricao, "Tarefa Existente")
       

    #Buscar por id inexistente
    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_buscar_tarefa_por_id_inexistente(self, _mock_open):
        gerenciador = GerenciadorTarefas(filepath=self.test_filepath)
        tarefa_encontrada = gerenciador._buscar_tarefa_por_id(3) #id próximo que não existe
        self.assertIsNone(tarefa_encontrada)

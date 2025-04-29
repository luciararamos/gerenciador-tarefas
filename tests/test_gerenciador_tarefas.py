import unittest
from unittest.mock import patch, mock_open
from gerenciador_tarefas import GerenciadorTarefas
from tarefa import Tarefa

class TestGerenciadorTarefas(unittest.TestCase):

#Iniciar gerenciador

    #arquivo valido
    @patch('builtins.open', new_callable=mock_open, read_data="id,descricao,status\n")
    def test_iniciar_gerenciador_com_arquivo_valido(self, _mock_file):
        gerenciador = GerenciadorTarefas(filepath='minhas_tarefas.csv')
        self.assertIsInstance(gerenciador, GerenciadorTarefas)
        self.assertEqual(gerenciador._filepath, 'minhas_tarefas.csv')

    #arquivo inválido, malformado
    @patch('builtins.open', new_callable=mock_open, read_data="id,name\n1,Tarefa sem descricao")
    def test_iniciar_gerenciador_com_arquivo_invalido(self, _mock_file):
        gerenciador = GerenciadorTarefas(filepath='arquivo_invalido.csv')
        self.assertEqual(len(gerenciador.listar_tarefas()), 0)

    #sem arquivo
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_iniciar_gerenciador_sem_arquivo(self, _mock_file):
        gerenciador = GerenciadorTarefas()
        self.assertIsInstance(gerenciador, GerenciadorTarefas)

    #arquivo vazio
    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_iniciar_gerenciador_com_arquivo_vazio(self, _mock_file):
        gerenciador = GerenciadorTarefas(filepath='arquivo_vazio.csv')
        self.assertEqual(len(gerenciador.listar_tarefas()), 0)

    #arquivo faltando colunas
    @patch('builtins.open', new_callable=mock_open, read_data="id,descricao\n1,Tarefa sem status")
    def test_iniciar_gerenciador_com_arquivo_faltando_colunas(self, _mock_file):
        gerenciador = GerenciadorTarefas(filepath='arquivo_faltando_colunas.csv')
        self.assertEqual(len(gerenciador.listar_tarefas()), 0)

    #arquivo com status inválido
    @patch('builtins.open', new_callable=mock_open, read_data="id,descricao,status\n1,Tarefa errada,Em andamento")
    def test_iniciar_gerenciador_com_status_invalido(self, _mock_file):
        gerenciador = GerenciadorTarefas(filepath='arquivo_com_status_invalido.csv')
        self.assertEqual(len(gerenciador.listar_tarefas()), 0)

#Adicionar

    #Adicionar nova tarefa
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_adicionar_nova_tarefa_valida(self, _mock_salvar, _mock_file):
        gerenciador = GerenciadorTarefas()
        gerenciador.adicionar_tarefa("Nova Tarefa")
        self.assertEqual(len(gerenciador._tarefas), 1)

    #Adicionar tarefa invalida
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_adicionar_nova_tarefa_invalida(self, _mock_salvar, _mock_file):
        gerenciador = GerenciadorTarefas()
        with self.assertRaises(ValueError):
            gerenciador.adicionar_tarefa("")

    
#Remover tarefa

    #Remover tarefa existente
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_remover_tarefa_existente(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas()
        tarefa = gerenciador.adicionar_tarefa("Tarefa Existente")
        gerenciador.remover_tarefa(tarefa.id)
        self.assertEqual(len(gerenciador._tarefas), 0)

    #Remover tarefa inexistente
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_remover_tarefa_inexistente(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas()
        with self.assertRaises(ValueError):
            gerenciador.remover_tarefa(999)

#Listar tarefas

    #Listar tarefas vazias
    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_listar_tarefas_vazia(self, _mock_open):
        gerenciador = GerenciadorTarefas()
        tarefas = gerenciador.listar_tarefas()
        self.assertEqual(tarefas, [])

    #Listar tarefas pendentes
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_listar_tarefas_pendentes(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas()
        gerenciador.adicionar_tarefa("Tarefa Pendente 1")
        tarefas_pendentes = gerenciador.listar_tarefas_pendentes()
        self.assertEqual(len(tarefas_pendentes), 1)
        self.assertEqual(tarefas_pendentes[0].descricao, "Tarefa Pendente 1")
        self.assertEqual(tarefas_pendentes[0].status, Tarefa.STATUS_PENDENTE)

    #Listar tarefas concluídas
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_listar_tarefas_concluidas(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas()
        gerenciador.adicionar_tarefa("Tarefa Concluída 1")
        gerenciador.marcar_como_concluida(1)
        tarefas_concluidas = gerenciador.listar_tarefas_concluidas()
        self.assertEqual(len(tarefas_concluidas), 1)
        self.assertEqual(tarefas_concluidas[0].descricao, "Tarefa Concluída 1")
        self.assertEqual(tarefas_concluidas[0].status, Tarefa.STATUS_CONCLUIDA)

    #Listar todas as tarefas
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_listas_todas_tarefas(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas()
        gerenciador.adicionar_tarefa("Tarefa 1")
        gerenciador.adicionar_tarefa("Tarefa 2")
        tarefas = gerenciador.listar_tarefas()
        self.assertEqual(len(tarefas), 2)

#Buscar tarefa por id

    #Buscar por id
    @patch('builtins.open', new_callable=mock_open, read_data="")
    @patch.object(GerenciadorTarefas, '_salvar_tarefas')
    def test_buscar_tarefa_por_id_existente(self, _mock_salvar, _mock_open):
        gerenciador = GerenciadorTarefas()
        tarefa_adicionada = gerenciador.adicionar_tarefa("Tarefa Existente")
        tarefa_encontrada = gerenciador._buscar_tarefa_por_id(tarefa_adicionada.id)
        self.assertIsNotNone(tarefa_encontrada)
        self.assertEqual(tarefa_encontrada.descricao, "Tarefa Existente")

    #Buscar por id inexistente
    @patch('builtins.open', new_callable=mock_open, read_data="")
    def test_buscar_tarefa_por_id_inexistente(self, _mock_open):
        gerenciador = GerenciadorTarefas()
        tarefa_encontrada = gerenciador._buscar_tarefa_por_id(999)
        self.assertIsNone(tarefa_encontrada)

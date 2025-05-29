# projeto_tarefas_csv/gerenciador_tarefas.py

import csv
from typing import List, Optional   #importando duas ferramentas do módulo typind 
from tarefa import Tarefa


class GerenciadorTarefas:
    """Gerencia uma coleção de objetos Tarefa, com persistência em arquivo CSV."""

    CAMPOS_CSV = ['id', 'descricao', 'status']

    def __init__(self, filepath: str = 'tarefas.csv'):
        """
        Inicializa o gerenciador.

        Args:
            filepath (str): O caminho para o arquivo CSV onde as tarefas serão salvas.
                            Padrão é 'tarefas.csv' no diretório atual.
        """
        self._filepath = filepath
        self._tarefas: List[Tarefa] = []
        self._proximo_id: int = 1
        self._carregar_tarefas() # Carrega tarefas existentes ao iniciar

    def _carregar_tarefas(self):
        """Carrega as tarefas do arquivo CSV para a memória."""
        tarefas_carregadas = []
        max_id = 0
        try:
            # Usamos utf-8 para suportar caracteres acentuados
            # newline='' é importante para o módulo csv funcionar corretamente
            with open(self._filepath, mode='r', newline='', encoding='utf-8') as file:
                # Usar DictReader facilita o acesso por nome de coluna
                reader = csv.DictReader(file)
                for i, row in enumerate(reader):
                    try:
                        # Valida se as colunas esperadas existem
                        if not all(key in row for key in self.CAMPOS_CSV):
                             print(f"Aviso: Linha {i+1} ignorada no CSV por falta de colunas esperadas ({self._filepath}). Conteúdo: {row}")
                             continue

                        task_id = int(row['id'])
                        descricao = row['descricao']
                        status = row['status']

                        # Cria a tarefa (a classe Tarefa valida descrição e status)
                        tarefa = Tarefa(id=task_id, descricao=descricao, status=status)
                        tarefas_carregadas.append(tarefa)

                        # Atualiza o maior ID encontrado
                        if task_id > max_id:
                            max_id = task_id

                    except (ValueError, TypeError, KeyError) as e:
                        # Captura erros de conversão (int), status inválido (Tarefa), ou coluna faltando (KeyError)
                        print(f"Aviso: Erro ao processar linha {i+1} do CSV ({self._filepath}): {e}. Linha ignorada. Conteúdo: {row}")
                    except Exception as e:
                         print(f"Aviso: Erro inesperado ao processar linha {i+1} do CSV ({self._filepath}): {e}. Linha ignorada. Conteúdo: {row}")


            self._tarefas = tarefas_carregadas
            # Define o próximo ID como o maior ID encontrado + 1
            self._proximo_id = max_id + 1
            print(f"Tarefas carregadas de '{self._filepath}'. Próximo ID: {self._proximo_id}")

        except FileNotFoundError:
            print(f"Arquivo '{self._filepath}' não encontrado. Começando com lista de tarefas vazia.")
            self._tarefas = []
            self._proximo_id = 1
        except Exception as e:
            print(f"Erro crítico ao carregar o arquivo CSV '{self._filepath}': {e}. Iniciando com lista vazia.")
            # Em caso de erro grave na leitura, melhor começar vazio para não corromper
            self._tarefas = []
            self._proximo_id = 1


    def _salvar_tarefas(self):
        """Salva o estado atual da lista de tarefas no arquivo CSV."""
        try:
            with open(self._filepath, mode='w', newline='', encoding='utf-8') as file:
                # Usar DictWriter garante que as colunas sejam escritas corretamente
                writer = csv.DictWriter(file, fieldnames=self.CAMPOS_CSV)

                writer.writeheader() # Escreve o cabeçalho ('id', 'descricao', 'status')
                for tarefa in self._tarefas:
                    writer.writerow({
                        'id': tarefa.id,
                        'descricao': tarefa.descricao,
                        'status': tarefa.status
                    })
            # print(f"Tarefas salvas em '{self._filepath}'.") # Opcional: feedback de salvamento
        except IOError as e:
            print(f"Erro: Não foi possível salvar as tarefas no arquivo '{self._filepath}': {e}")
        except Exception as e:
             print(f"Erro inesperado ao salvar as tarefas no arquivo '{self._filepath}': {e}")


    def _gerar_proximo_id(self) -> int:
        """Gera e retorna o próximo ID único para uma tarefa, atualizando o contador."""
        id_atual = self._proximo_id
        self._proximo_id += 1
        return id_atual

    def _buscar_tarefa_por_id(self, id_tarefa: int) -> Optional[Tarefa]:
        """Busca uma tarefa na lista (em memória) pelo seu ID."""
        for tarefa in self._tarefas:
            if tarefa.id == id_tarefa:
                return tarefa
        return None

    def adicionar_tarefa(self, descricao: str) -> Tarefa:
        """
        Adiciona uma nova tarefa à lista e salva no CSV.

        Args:
            descricao (str): A descrição da nova tarefa.

        Returns:
            Tarefa: O objeto Tarefa que foi criado e adicionado.

        Raises:
            ValueError: Se a descrição for inválida (gerado pela classe Tarefa).
        """
        novo_id = self._gerar_proximo_id()
        # A classe Tarefa valida a descrição
        nova_tarefa = Tarefa(id=novo_id, descricao=descricao)
        self._tarefas.append(nova_tarefa)
        self._salvar_tarefas() # Salva a lista atualizada
        print(f"Tarefa '{nova_tarefa.descricao}' (ID: {nova_tarefa.id}) adicionada e salva.")
        return nova_tarefa

    def marcar_como_concluida(self, id_tarefa: int):
        """
        Marca uma tarefa como concluída pelo seu ID e salva a alteração no CSV.

        Args:
            id_tarefa (int): O ID da tarefa a ser marcada como concluída.

        Raises:
            ValueError: Se nenhuma tarefa com o ID fornecido for encontrada.
        """
        tarefa = self._buscar_tarefa_por_id(id_tarefa)
        if tarefa:
            if tarefa.status == Tarefa.STATUS_PENDENTE:
                tarefa.marcar_como_concluida()
                self._salvar_tarefas() # Salva após modificar
                print(f"Tarefa ID {id_tarefa} marcada como concluída e salva.")
            else:
                print(f"Tarefa ID {id_tarefa} já estava concluída. Nenhuma alteração salva.")
        else:
            raise ValueError(f"Erro: Tarefa com ID {id_tarefa} não encontrada.")

    def remover_tarefa(self, id_tarefa: int):
        """
        Remove uma tarefa da lista pelo seu ID e salva a alteração no CSV.

        Args:
            id_tarefa (int): O ID da tarefa a ser removida.

        Raises:
            ValueError: Se nenhuma tarefa com o ID fornecido for encontrada.
        """
        tarefa = self._buscar_tarefa_por_id(id_tarefa)
        if tarefa:
            self._tarefas.remove(tarefa)
            self._salvar_tarefas() # Salva após remover
            print(f"Tarefa ID {id_tarefa} removida com sucesso e alterações salvas.")
        else:
            raise ValueError(f"Erro: Tarefa com ID {id_tarefa} não encontrada para remoção.")

    # Os métodos de listagem operam na lista em memória, que foi carregada na inicialização.
    # Não precisam de alterações diretas para interagir com o CSV aqui.
    def listar_tarefas(self, status_desejado: Optional[str] = None) -> List[Tarefa]:
        """Lista tarefas em memória, opcionalmente filtrando por status."""
        if status_desejado:
            if status_desejado not in [Tarefa.STATUS_PENDENTE, Tarefa.STATUS_CONCLUIDA]:
                raise ValueError(f"Status inválido: {status_desejado}. Use '{Tarefa.STATUS_PENDENTE}' ou '{Tarefa.STATUS_CONCLUIDA}'.")
            return [tarefa for tarefa in self._tarefas if tarefa.status == status_desejado]
        else:
            return self._tarefas[:] # Retorna uma cópia

    def listar_tarefas_pendentes(self) -> List[Tarefa]:
        """Retorna uma lista (em memória) de tarefas pendentes."""
        return self.listar_tarefas(Tarefa.STATUS_PENDENTE)

    def listar_tarefas_concluidas(self) -> List[Tarefa]:
        """Retorna uma lista (em memória) de tarefas concluídas."""
        return self.listar_tarefas(Tarefa.STATUS_CONCLUIDA)
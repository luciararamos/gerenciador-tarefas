# projeto_tarefas_csv/main.py

from gerenciador import GerenciadorTarefas

def imprimir_lista(titulo: str, lista_tarefas: list):
    """Função auxiliar para imprimir listas de tarefas de forma organizada."""
    print(f"\n--- {titulo} ---")
    if not lista_tarefas:
        print("Nenhuma tarefa encontrada.")
    else:
        for tarefa in lista_tarefas:
            print(tarefa)
    print("--------------------")

if __name__ == "__main__":
    ARQUIVO_CSV = 'minhas_tarefas.csv' # Exemplo: usar um nome de arquivo específico
    print(f"Iniciando o Gerenciador de Tarefas Simples (Persistência: {ARQUIVO_CSV})")

    # Cria uma instância do gerenciador, especificando o arquivo CSV
    gerenciador = GerenciadorTarefas(filepath=ARQUIVO_CSV)

    # Verifica se já existem tarefas carregadas
    imprimir_lista("Tarefas Carregadas ao Iniciar", gerenciador.listar_tarefas())

    # Adicionando algumas tarefas (serão salvas no CSV)
    try:
        tarefa_nova1 = gerenciador.adicionar_tarefa("Revisar código do projeto X")
        tarefa_nova2 = gerenciador.adicionar_tarefa("Agendar reunião com equipe")
        # Tentando adicionar tarefa inválida
        # gerenciador.adicionar_tarefa("") # Descomente para testar o erro
    except ValueError as e:
        print(f"Erro ao adicionar tarefa: {e}")

    # Listando todas as tarefas (incluindo as carregadas e as novas)
    imprimir_lista("Todas as Tarefas Atuais", gerenciador.listar_tarefas())

    # Marcando uma tarefa como concluída (será salvo no CSV)
    # Vamos pegar o ID da primeira tarefa pendente, se houver
    tarefas_pendentes = gerenciador.listar_tarefas_pendentes()
    if tarefas_pendentes:
        try:
            id_para_concluir = tarefas_pendentes[0].id
            print(f"\nTentando marcar tarefa ID {id_para_concluir} como concluída...")
            gerenciador.marcar_como_concluida(id_para_concluir)
        except ValueError as e:
             print(e)
        except IndexError:
             print("Não há tarefas pendentes para marcar como concluída.") # Caso raro aqui
    else:
        print("\nNenhuma tarefa pendente para marcar como concluída.")


    # Tentando marcar ID inexistente
    try:
        gerenciador.marcar_como_concluida(9999)
    except ValueError as e:
        print(e)

    # Listando tarefas pendentes e concluídas (reflete o estado atual em memória e no CSV)
    imprimir_lista("Tarefas Pendentes Atuais", gerenciador.listar_tarefas_pendentes())
    imprimir_lista("Tarefas Concluídas Atuais", gerenciador.listar_tarefas_concluidas())

    # Removendo uma tarefa (será salvo no CSV)
    # Vamos remover a primeira tarefa concluída, se houver
    tarefas_concluidas = gerenciador.listar_tarefas_concluidas()
    if tarefas_concluidas:
        try:
            id_para_remover = tarefas_concluidas[0].id
            print(f"\nTentando remover tarefa ID {id_para_remover}...")
            gerenciador.remover_tarefa(id_para_remover)
        except ValueError as e:
            print(e)
        except IndexError:
            print("Não há tarefas concluídas para remover.") # Caso raro aqui
    else:
        print("\nNenhuma tarefa concluída para remover.")


    # Tentando remover ID inexistente
    try:
        gerenciador.remover_tarefa(8888)
    except ValueError as e:
        print(e)

    # Listando todas as tarefas após as operações
    imprimir_lista("Todas as Tarefas Finais", gerenciador.listar_tarefas())

    print(f"\nDemonstração concluída. Verifique o arquivo '{ARQUIVO_CSV}' para ver o resultado salvo.")
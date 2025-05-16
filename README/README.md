# Projeto Tarefas Simples com Persistência CSV (Python)

Este é um projeto simples em Python que implementa a lógica básica de um sistema de gerenciamento de tarefas (To-Do List), **com persistência de dados em um arquivo CSV**. O foco principal é ter uma estrutura organizada com classes separadas, ideal para praticar e implementar testes unitários posteriormente (considerando o desafio de lidar com I/O de arquivo nos testes).

**Atenção:** Este projeto **não inclui** os testes unitários, apenas a estrutura das classes e um exemplo de uso.

## Estrutura do Projeto

- `tarefa.py`: Contém a classe `Tarefa`, que representa uma tarefa individual com ID, descrição e status (Pendente/Concluída).
- `gerenciador_tarefas.py`: Contém a classe `GerenciadorTarefas`, responsável por carregar, adicionar, remover, buscar, listar e gerenciar o estado das tarefas, **salvando todas as alterações em um arquivo CSV**.
- `main.py`: Um script simples que demonstra como usar as classes `GerenciadorTarefas` e `Tarefa`. Serve como um ponto de entrada para ver o sistema em ação.
- `README.md`: Este arquivo.
- `tarefas.csv` (ou nome definido no `main.py`): Arquivo CSV que será criado/atualizado automaticamente para armazenar os dados das tarefas.

## Funcionalidades

- Carrega tarefas existentes de um arquivo CSV ao iniciar.
- Salva todas as alterações (adição, conclusão, remoção) de volta no arquivo CSV.
- Adicionar novas tarefas com descrição.
- Marcar tarefas existentes como concluídas.
- Remover tarefas.
- Listar todas as tarefas carregadas em memória.
- Listar apenas tarefas pendentes (em memória).
- Listar apenas tarefas concluídas (em memória).
- Validação básica (descrição não pode ser vazia, IDs são gerenciados).
- Tratamento de erros para operações inválidas e problemas de I/O (leitura/escrita do CSV).

## Como Executar

1.  **Pré-requisitos:** Certifique-se de ter o Python 3.x instalado em seu sistema.
2.  **Navegação:** Abra um terminal ou prompt de comando e navegue até o diretório raiz do projeto (`projeto_tarefas_csv/`).
3.  **Execução:** Execute o script principal `main.py` usando o comando:

    ```bash
    python main.py
    ```

    Isso rodará a demonstração definida no arquivo `main.py`. Ao executar pela primeira vez (ou se o arquivo CSV não existir), ele criará um arquivo CSV (por padrão `tarefas.csv`, ou o nome especificado em `main.py`). Nas execuções subsequentes, ele carregará os dados desse arquivo e salvará as alterações nele.

## Próximos Passos (Estudo de Testes Unitários)

A introdução da persistência em arquivo CSV torna os testes unitários mais complexos. Para testar a classe `GerenciadorTarefas` **em isolamento** (a definição de teste unitário), você precisaria:

- **Mocar (Mocking):** Usar bibliotecas como `unittest.mock` para substituir as funções embutidas `open` e os objetos/métodos do módulo `csv` (`reader`, `writer`, etc.). Isso permite simular a leitura e escrita de arquivos sem realmente tocar no sistema de arquivos, tornando os testes mais rápidos e independentes do estado do disco.
- **Testar a Lógica:** Focar em testar se o `GerenciadorTarefas` chama corretamente as funções de leitura/escrita simuladas e se a lógica interna (manipulação da lista `_tarefas`, geração de IDs) funciona como esperado com base nos dados simulados.

Testar a classe `Tarefa` permanece simples, pois ela não tem dependências de I/O.

## Executar os Testes Unitários da classe Tarefa

Para executar os testes unitários da classe `Tarefa`

1. Certifique-se de que você está dentro da pasta `gerenciador_tarefas/`

2. Acesse a subpasta `tests/test_tarefa.py`

3. Execute o comando: python -m unittest tests.test_tarefa

## Executar os Testes Unitários da classe GerenciadorTarefas

Para executar os testes unitários da classe `GerenciadorTarefas`,

1. Certifique-se de que você está dentro da pasta `gerenciador_tarefas/`

2. Acesse a subpasta `tests/test_gerenciador_tarefas.py`

3. Execute o comando: python -m unittest tests.test_gerenciador_tarefas
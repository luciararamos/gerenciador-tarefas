
class Tarefa:
    """Representa uma tarefa individual no sistema."""

    STATUS_PENDENTE = "Pendente"
    STATUS_CONCLUIDA = "Concluída"

    def __init__(self, id: int, descricao: str, status: str = STATUS_PENDENTE):
        """
        Inicializa uma nova tarefa.

        Args:
            id (int): O identificador único da tarefa.
            descricao (str): A descrição da tarefa. Não pode ser vazia.
            status (str): O status inicial da tarefa (Pendente ou Concluída).

        Raises:
            ValueError: Se a descrição for vazia ou nula, ou se o status for inválido.
        """
        if not descricao or not descricao.strip():
            raise ValueError("A descrição da tarefa não pode ser vazia.")
        if status not in [self.STATUS_PENDENTE, self.STATUS_CONCLUIDA]:
             raise ValueError(f"Status inválido: {status}. Use '{self.STATUS_PENDENTE}' ou '{self.STATUS_CONCLUIDA}'.")

        self.id = id
        self.descricao = descricao.strip()
        self.status = status

    def marcar_como_concluida(self):
        """Muda o status da tarefa para 'Concluída'."""
        self.status = self.STATUS_CONCLUIDA

    def __str__(self) -> str:
        """Retorna uma representação em string da tarefa."""
        return f"ID: {self.id} | Descrição: {self.descricao} | Status: {self.status}"

    def __repr__(self) -> str:
        """Retorna uma representação mais técnica da tarefa."""
        return f"Tarefa(id={self.id}, descricao='{self.descricao}', status='{self.status}')"
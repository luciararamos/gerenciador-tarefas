import unittest
from tarefa import Tarefa


class TestTarefa(unittest.TestCase):
 
    def test_criar_tarefa_com_descricao_valida(self):
        tarefa = Tarefa(id=1, descricao="Minha descricao")
        self.assertEqual(tarefa.descricao, "Minha descricao")

    def test_criar_tarefa_com_descricao_invalida_espaco_em_branco(self):
        with self.assertRaises(ValueError):
            Tarefa(id=2, descricao="  ")

    def test_criar_tarefa_sem_descricao(self):
        with self.assertRaises(ValueError):
            Tarefa(id=3, descricao="")

    def test_criar_tarefa_com_status_concluida(self):
        tarefa = Tarefa(id=4, descricao="Minha descricao", status=Tarefa.STATUS_CONCLUIDA)
        self.assertEqual(tarefa.status, Tarefa.STATUS_CONCLUIDA)                

    def test_criar_tarefa_com_status_pendente(self):
        tarefa = Tarefa(id=5, descricao="Minha descricao", status=Tarefa.STATUS_PENDENTE)
        self.assertEqual(tarefa.status, Tarefa.STATUS_PENDENTE)

    def test_criar_tarefa_com_status_inexistente(self):
        with self.assertRaises(ValueError):
            Tarefa(id=6, descricao="Minha descricao", status="Em andamento")

    def test_criar_tarefa_sem_status_deve_ficar_pendente(self):
        tarefa = Tarefa(id=7, descricao="Minha descricao")
        self.assertEqual(tarefa.status, Tarefa.STATUS_PENDENTE)

    def test_marcar_tarefa_pendente_como_concluida(self):
        tarefa = Tarefa(id=8, descricao="Minha descricao")
        tarefa.marcar_como_concluida()
        self.assertEqual(tarefa.status, Tarefa.STATUS_CONCLUIDA)

    def test_marcar_tarefa_ja_concluida_novamente_mantem_status(self):
        tarefa = Tarefa(id=9, descricao="Minha descricao", status=Tarefa.STATUS_CONCLUIDA)
        tarefa.marcar_como_concluida()
        self.assertEqual(tarefa.status, Tarefa.STATUS_CONCLUIDA)

    def test_str_com_status_pendente(self):                      #___str___
        tarefa = Tarefa(id=10, descricao="Minha descricao",  status=Tarefa.STATUS_PENDENTE)
        self.assertEqual(str(tarefa), "ID: 9 | Descrição: Minha descricao | Status: Pendente")

    def test_str_com_status_concluido(self):                     
        tarefa = Tarefa(id=11, descricao="Minha descricao", status=Tarefa.STATUS_CONCLUIDA)
        self.assertEqual(str(tarefa), "ID: 11 | Descrição: Minha descricao | Status: Concluída")
 
    def test_repr_para_ambos_status(self):                          #___repr___
        tarefa_pendente = Tarefa(id=12, descricao="Minha descricao", status=Tarefa.STATUS_PENDENTE)       
        tarefa_concluida = Tarefa(id=13, descricao="Minha descricao", status=Tarefa.STATUS_CONCLUIDA)
        self.assertEqual(repr(tarefa_pendente), "Tarefa(id=11, descricao='Minha descricao', status='Pendente')")
        self.assertEqual(repr(tarefa_concluida), "Tarefa(id=12, descricao='Minha descricao', status='Concluída')")

if __name__ == '__main__':
    import unittest
    unittest.main()




        
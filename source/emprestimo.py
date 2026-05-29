class Emprestimo:
    """
        Classe base para emprestimos.
    """
    def __init__(self, devolucao, livro, usuario):
        self.devolucao = devolucao
        self.livro = livro
        self.usuario = usuario
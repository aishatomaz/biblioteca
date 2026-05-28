class Usuario():
    def __init__(self, id_usuario, nome, username, data_nascimento, contato, senha):
        self.id = id_usuario
        self.nome = nome
        self.username = username
        self.data_nasc = data_nascimento
        self.contato = contato
        self.senha = senha

user = Usuario()
print(user(1, "Will", "rafaelwi", "30/07/1978", 993034429, "#####"))
import sys
import uuid
from typing import Optional

from source.usuario import Usuario
from source.livro import Livro
from source.emprestimo import Emprestimo

usuario_atual: Optional[Usuario] = None
usuarios: list[Usuario] = list()
livros: list[Livro] = list()
emprestimos: list[Emprestimo] = list()
programa_ativo: bool = True

lista_comandos_atalhos: str = """
    ----------------------------------------
    Lista de comandos
    ----------------------------------------
        
        * ajuda - Mostra esta mensagem novamente
        
        * cadastrar livro - Cadastrar um novo livro
        * cadastrar usuário - Cadastrar um novo usuário
        
        * devolver livro - Devolver um livro emprestado
        
        * efetuar empréstimo - Fazer empréstimo de livro
        * efetuar autenticação - Fazer login no sistema
        
        * listar empréstimos - Listar empréstimos em andamento 
        * listar usuários - Lista de usuários
        * listar livros - Lista os livros disponíveis
        
        * sair usuário - Desconectar do usuário atual
        * sair sistema - Encerrar o programa
        
    ----------------------------------------
    Atalhos
    ----------------------------------------
    
        cad: cadastrar
        dev: devolver
        eft: efetuar
        lis: listar
        
        -a: autenticação
        -e: empréstimo(s)
        -l: livro(s)
        -s: sistema
        -u: usuário(s)
"""

# ---------------------------------------------------
# CADASTRAR
# ---------------------------------------------------

def cadastrar_usuario():
    print("""
    ----------------------------------------
    Crie um usuário para usar o sistema
    ----------------------------------------
    """)

    global usuarios
    global usuario_atual
    nome = input("Nome: ")
    senha = input("Crie uma senha: ")

    usuario = Usuario(
        id_usuario=uuid.uuid4(),
        nome=nome,
        senha=senha,
        data_nascimento=None,
        username=None,
        contato=None
    )
    usuarios.append(usuario)
    usuario_atual = usuario

def cadastrar_livro():
    print("""
    ----------------------------------------
    Cadastro de livros
    ----------------------------------------
    """)

    global livros
    titulo = input("Título: ")
    paginas = int(input("Quantidade de Páginas: "))
    autor = input("Autor: ")

    livro = Livro(
        id_livro=uuid.uuid4(),
        titulo=titulo.strip().capitalize(),
        paginas=paginas,
        autor=autor.strip().capitalize(),
        disponivel=True,
        categoria=None
    )

    livros.append(livro)
    print(f"Você cadastrou o livro '{livro.titulo}'")

# ---------------------------------------------------
# EFETUAR
# ---------------------------------------------------

def efetuar_autenticacao():
    print("""
    ----------------------------------------
    Autenticação de Usuário
    ----------------------------------------
    """)
    global usuario_atual
    nome = input("Nome: ")
    senha = input("Senha: ")

    for usuario in usuarios:
        if usuario.nome == nome and usuario.senha == senha:
            usuario_atual = usuario
            return

    print(f"Erro: nome e/ou senha inválidos", file=sys.stderr)

def efetuar_emprestimo():
    global emprestimos
    global usuario_atual
    global livros

    if not usuario_atual:
        print(f"Erro: Visitantes não podem realizar empréstimos", file=sys.stderr)
        return

    print("""
    ----------------------------------------
    Empréstimo de Livros
    ----------------------------------------
    """)

    titulo = input("Título: ").strip().capitalize()

    for livro in livros:
        if livro.titulo == titulo and livro.disponivel == True:

            emprestimo = Emprestimo(
                devolucao=False,
                usuario=usuario_atual,
                livro=livro
            )

            emprestimo.livro.disponivel = False
            emprestimos.append(emprestimo)
            print(f"Você realizou o empréstimo do livro '{livro.titulo}'")
            return

    print(f"Erro: Livro '{titulo}' não cadastrado ou indisponível", file=sys.stderr)

# ---------------------------------------------------
# LISTAR
# ---------------------------------------------------

def listar_usuarios():
    global usuarios

    if not usuarios:
        print("Nenhum usuário cadastrado")
    else:
        for usuario in usuarios:
            print(f"""
            
                {usuario.nome};
            """)
    print()

def listar_livros():
    global livros

    if not livros:
        print("Nenhum livro cadastrado")
    else:
        for livro in livros:
            print(f"""
            
                {livro.titulo}
                autor: {livro.autor}
                páginas: {livro.paginas}
                disponível?: {"Sim" if livro.disponivel else "Não"}
            """)
    print()


def listar_emprestimos():
    global emprestimos

    if not emprestimos:
        print("Nenhum empréstimo feito")
    else:
        for emprestimo in emprestimos:
            print(f"""

                usuário: {emprestimo.usuario.nome}
                livro: {emprestimo.livro.titulo}
                situação: {"Encerrado" if emprestimo.devolucao else "Ativo"}
            """)
    print()

# ---------------------------------------------------
# SAIR
# ---------------------------------------------------

def sair_sistema():
    global programa_ativo
    programa_ativo = False

def sair_usuario():
    global usuario_atual
    usuario_atual = None

# ---------------------------------------------------
# DEVOLVER
# ---------------------------------------------------

def devolver_livro():
    global usuario_atual
    global emprestimos

    print("""
    ----------------------------------------
    Devolução de Livros
    ----------------------------------------
    
    """)

    if not usuario_atual:
        print(f"Erro: Visitantes não podem realizar devoluções", file=sys.stderr)
        return

    emprestimos_em_andamento: list[Emprestimo] = list()

    for emprestimo in emprestimos:
        if emprestimo.usuario.id == usuario_atual.id and not emprestimo.devolucao:
            emprestimos_em_andamento.append(emprestimo)

    if emprestimos_em_andamento is None:
        print(f"Erro: Você não realizou empréstimos", file=sys.stderr)
        return

    for emprestimo in emprestimos_em_andamento:
        print(f"""
            livro: {emprestimo.livro.titulo};
            
        """)

    titulo = input("Qual livro deseja devolver?: ").strip().capitalize()

    for emprestimo in emprestimos_em_andamento:
        if titulo == emprestimo.livro.titulo:
            emprestimo.livro.disponivel = False
            emprestimo.devolucao = True
            print(f"Devolução de '{emprestimo.livro.titulo}' realizada")
        else:
            print(f"Erro: Livro não encontrado", file=sys.stderr)

# ---------------------------------------------------
# FLUXO PRINCIPAL
# ---------------------------------------------------

def cadastrar(item):
    match item:
        case "usuário" | "usuario" | "-u":
           cadastrar_usuario()
        case "livro" | "-l":
            cadastrar_livro()
        case _:
            print(f"Erro: Incapaz de cadastrar '{item}'", file=sys.stderr)

def efetuar(item):
    match item:
        case "autenticação" | "-a":
            efetuar_autenticacao()
        case "empréstimo" | "-e":
            efetuar_emprestimo()
        case _:
            print(f"Erro: Incapaz de efetuar '{item}'", file=sys.stderr)

def devolver(item):
    match item:
        case "livro" | "-l":
            devolver_livro()
        case _:
            print(f"Erro: Incapaz de devolver '{item}'", file=sys.stderr)


def listar(item):
    match item:
        case "empréstimos" | "-e":
            listar_emprestimos()
        case "livros" | "-l":
            listar_livros()
        case "usuários" | "-u":
            listar_usuarios()
        case _:
            print(f"Erro: Incapaz de listar '{item}'", file=sys.stderr)

def sair(item):
    match item:
        case "sistema" | "-s":
            sair_sistema()
        case "usuário" | "-u":
            sair_usuario()
        case _:
            print(f"Erro: Incapaz de sair para '{item}'", file=sys.stderr)


if __name__ == "__main__":
    print(lista_comandos_atalhos)

    msg_caixa_texto: str

    while programa_ativo:
        msg_caixa_texto = f"\n({usuario_atual.nome}): " if usuario_atual else "\n<Visitante>: "

        entrada: list[str] = input(msg_caixa_texto).lower().strip().split()

        comando = entrada[0]
        item = entrada[1] if len(entrada) > 1 else " "


        match comando:
            case "ajuda":
                print(lista_comandos_atalhos)
            case "cadastrar" | "cad":
                cadastrar(item)
            case "devolver" | "dev":
                devolver(item)
            case "efetuar" | "eft":
                efetuar(item)
            case "listar" | "lis":
                listar(item)
            case "sair":
                sair(item)
            case _:
                print(f"Erro: Comando '{comando}' é desconhecido", file=sys.stderr)

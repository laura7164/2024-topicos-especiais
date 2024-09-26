import sqlite3

def exibir_menu():
    print()
    print('1. Adicionar novo livro')
    print('2. Exibir todos os livros')
    print('3. Atualizar preço de um livro')
    print('4. Remover um livro')
    print('5. Sair')

conexao = sqlite3.connect('minha_livraria.db') 
cursor = conexao.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS livraria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao TEXT NOT NULL,
        preco FLOAT NOT NULL
    )
''')

def adicionar_livro(titulo: str, autor: str, ano_publicacao: str, preco: float):
    cursor.execute('INSERT INTO livraria (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)', (titulo, autor, ano_publicacao, preco))

def exibir_livros():
    cursor.execute('SELECT * FROM livraria')
    livraria = cursor.fetchall()

    for livro in livraria:
        print(livro)

def atualizar_preco(preco: float, titulo: str):
    cursor.execute('UPDATE livraria set preco = ? WHERE titulo = ?', (preco, titulo))

def remover_livro(titulo: str):
    cursor.execute('DELETE FROM livraria WHERE titulo = ?', (titulo,))

while True:
    exibir_menu()

    opcao = int(input('Escolha uma opção: '))

    if opcao == 1:
        titulo = input('Digite o titulo do livro: ')
        autor = input(f'Digite o autor do livro "{titulo}": ')
        ano_publicacao = input(f'Digite o ano de publicação do livro "{titulo}": ')
        preco = float(input(f'Digite o preço do livro "{titulo}": '))

        adicionar_livro(titulo, autor, ano_publicacao, preco)

        print('Livro cadastrado com sucesso!')
        
    elif opcao == 2:
        exibir_livros()

    elif opcao == 3:
        titulo = input('Digite o livro que deseja alterar o preço: ')
        novo_preco = float(input(f'Digite o novo preço do livro "{titulo}": '))

        print('Preço atualizado com sucesso!')

        atualizar_preco(novo_preco, titulo)

    elif opcao == 4:
        titulo = input('Digite o livro que deseja remover: ')

        print('Livro removido com sucesso!')

        remover_livro()

    elif opcao == 5:
        print('Saindo.')
        break

    else:
        print('Opção inválida, digite novamente.')

    conexao.commit()

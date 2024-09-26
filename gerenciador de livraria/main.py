import sqlite3

def exibir_menu():
    print()
    print('1. Adicionar um novo livro')
    print('2. Exibir todos os livros cadastrados')
    print('3. Atualizar o preço de um livro')
    print('4. Remover um livro')
    print('5. Buscar livros por autor')
    print('6. Exportar dados para o CSV')
    print('7. Importar dados do CSV')
    print('8. Fazer backup do banco de dados')
    print('9. Sair')

# conexão com o banco de dados SQLite
conexao = sqlite3.connect('minha_livraria.db') 
cursor = conexao.cursor()

# criação da tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS livraria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        ano_publicacao INTEGER NOT NULL,
        preco FLOAT NOT NULL
    )
''')

def adicionar_livro(titulo: str, autor: str, ano_publicacao: int, preco: float):
    cursor.execute('INSERT INTO livraria (titulo, autor, ano_publicacao, preco) VALUES (?, ?, ?, ?)', (titulo, autor, ano_publicacao, preco))

def exibir_livros():
    cursor.execute('SELECT * FROM livraria')
    resultado = cursor.fetchall()

    for livro in resultado:
        print(livro)

def atualizar_preco(preco: float, titulo: str):
    cursor.execute('UPDATE livraria set preco = ? WHERE titulo = ?', (preco, titulo))

def remover_livro(titulo: str):
    cursor.execute('DELETE FROM livraria WHERE titulo = ?', (titulo,))

def buscar_livro(autor: str):
    cursor.execute('SELECT * FROM livraria WHERE autor = ?', (autor))
    resultado = cursor.fetchall()

    for livro in resultado:
        print(livro)

while True:
    exibir_menu()

    try:
        opcao = int(input('Escolha uma opção: '))
    except ValueError:
        print('Por favor, insira um número válido.')
        continue

    if opcao == 1:
        titulo = input('Digite o titulo do livro: ')
        autor = input(f'Digite o autor do livro "{titulo}": ')

        while True:
            try:
                ano_publicacao = int(input(f'Digite o ano de publicação do livro "{titulo}": '))
                break
            except ValueError:
                print('Por favor, insira apenas números.')

        while True:
            try:
                preco = float(input(f'Digite o preço do livro "{titulo}": '))
                break
            except ValueError:
                print('Por favor, insira um valor numérico para o preço.')


        adicionar_livro(titulo, autor, ano_publicacao, preco)
        print(f'{titulo} cadastrado com sucesso!')
 
    elif opcao == 2:
        exibir_livros()

    elif opcao == 3:
        titulo = input('Digite o livro que deseja alterar o preço: ')

        while True:
            try:
                novo_preco = float(input(f'Digite o novo preço do livro "{titulo}": '))
                break
            except ValueError:
                print('Por favor, insira um valor numérico para o preço.')

        atualizar_preco(novo_preco, titulo)
        print('Preço atualizado com sucesso!')

    elif opcao == 4:
        titulo = input('Digite o livro que deseja remover: ')

        remover_livro()
        print(f'{titulo} removido com sucesso!')

    elif opcao == 5:
        autor = input('Digite o nome do autor do livro que deseja buscar: ')

        buscar_livro(autor)
    
    elif opcao == 6:
        ...

    elif opcao == 7:
        ...
    
    elif opcao == 8:
        ...
    
    elif opcao == 9:
        print('Saindo do sistema...')
        break

    else:
        print('Opção inválida, digite novamente.')

    # commit das alterações no banco de dados
    conexao.commit()

# fechar a conexão após sair do loop
conexao.close()

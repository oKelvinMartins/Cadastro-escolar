'''
O que devo desenvolver?
Implementar todas as funcionalidades já desenvolvidas (ex.: incluir e listar) para os demais módulos do sistema. Veja os dados necessários para cada um dos grupos abaixo:
Professores
Código do professor (Número inteiro)
Nome do professor (String)
CPF do professor (String)
Disciplinas
Código da disciplina (Número inteiro)
Nome da disciplina (String)
Turmas
Código da turma (Número inteiro)
Código do professor (Número inteiro)
Código da disciplina (Número inteiro)
Matrículas
Código da turma (Número inteiro)
Código do estudante (Número inteiro)
Validação de dados na manipulação de turmas e matrículas (verificar se um código já existe antes de incluir uma nova turma/matrícula com o mesmo código).

O que meu sistema deve ter no final? (checklist)
As quatro operações básicas (incluir/listar/atualizar/excluir) para todos os módulos (estudantes/professores/disciplinas/turmas/matrículas) do sistema.
Utilização de estruturas condicionais (if/elif/else) no código.
Utilização de estruturas de repetição (for ou while) para navegação dos menus
Utilização de estruturas de dados compostas (listas, dicionários, e/ou tuplas) para organização dos dados.
Utilização de arquivos para a persistência dos dados cadastrados.
Utilização de funções para modularizar as principais funcionalidades da aplicação.
As funções devem ser utilizadas seguindo boas práticas de programação.
Se possível, reaproveitar funções para diferentes módulos do sistema (ex.: uma única função para incluir registro de estudantes, professores, disciplinas, turmas e matrículas).
Validações de dados e controle de possíveis exceções/erros de execução (try/except).

'''

'''


'''

'''
Menu principal [ok]
Menu operações 
- Testes ok
- Deixar menu modular 
Menu estudantes 
Menu displinas 
Menu Professores 
Menu turmas 
Menu Matrículas 

'''


# Função - Salvar lista em JSON

import json
def salvar_lista_json(lista, arquivo):
    with open(arquivo, "w", encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)

# Função - Ler lista de cadastros do JSON


def ler_lista_json(arquivo):
    try:
        with open(arquivo, "r", encoding='utf-8') as f:
            cadastros = json.load(f)
        return cadastros
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Função - Mostrar menu principal


def mostrar_menu_principal():
    print("\n================== Menu Principal =================")
    print("1. Estudantes")
    print("2. Disciplinas")
    print("3. Professores")
    print("4. Turmas")
    print("5. Matrículas")
    print("0. Sair")

    try:
        return int(input("Digite o número da opção escolhida: "))

    except ValueError:
        print("Ops! Essa não é uma opção válida")
        return -1
# Função - Mostrar menu de operações


def mostrar_menu_operacao():
    print("\n==== Menu de Operações ====")
    print("1. Incluir")
    print("2. Listar")
    print("3. Atualizar")
    print("4. Excluir")
    print("5. Voltar ao Menu Principal")

    try:
        return int(input("Digite o número da operação escolhida: "))

    except ValueError:
        print("Ops! Essa não é uma opção válida")
        return -1

# Função processar menu de operações


def processar_menu_op(menu_op, arquivo):

    if menu_op == 1:
        incluir_cadastros(arquivo)
    elif menu_op == 2:
        listar_cadastros(arquivo)
    elif menu_op == 3:
        atualizar_cadastro(arquivo)
    elif menu_op == 4:
        excluir_cadastro(arquivo)
    elif menu_op == 5:
        print("Voltando ao menu principal...")
        return False
    else:
        print("Opção inválida. Tente novamente.")
    return


# Função - Incluir estudante

def incluir_cadastros(codigo_existe, arquivo):
    cadastros = ler_lista_json(arquivo)
    print("\n[Incluir Estudante]")
    nome_cadastro = input("Nome: ").strip()
    codigo_cadastro = int(input("Código de matrícula: "))
    cpf_cadastro = input("CPF: ").strip()
    dados_cadastro = {
        "codigo": codigo_cadastro,
        "nome": nome_cadastro,
        "cpf": cpf_cadastro
    }

    if codigo_existe(codigo_cadastro, arquivo):
        print("Já existe um cadastro com esse código!")
    elif any(e["cpf"] == cpf_cadastro for e in cadastros):
        print("Já existe um cadastro com esse CPF!")
    else:
        cadastros.append(dados_cadastro)
        salvar_lista_json(cadastros, arquivo)
        print(f"Cadastro '{nome_cadastro}' adicionado com sucesso!")
        return


# Função incluir disciplinas

def incluir_disciplinas(arquivo):
    disciplinas = ler_lista_json(arquivo)
    print("\n[Incluir disciplinas]")
    nome_disciplina = input("Nome: ").strip()
    codigo_disciplina = int(input("Código da disciplina: "))
    dados_disciplina = {
        "codigo": codigo_disciplina,
        "nome": nome_disciplina,

    }
    disciplinas.append(dados_disciplina)
    salvar_lista_json(disciplinas, arquivo)
    print(f"Disciplina '{nome_disciplina}' adicionado com sucesso!")


# Função - Listar cadastros


def listar_cadastros(arquivo):
    cadastros = ler_lista_json(arquivo)
    print(f"\n[Listar cadastros - {arquivo}]")
    if not cadastros:
        print("Nenhum registro cadastrado.")
    else:
        for cadastro in cadastros:
            linha = []
            for chave, valor in cadastro.items():
                linha.append(f"{chave.capitalize()}: {valor}")
            print(" | ".join(linha))

# Função - Atualizar cadastros


def atualizar_cadastro(arquivo):
    cadastros = ler_lista_json(arquivo)
    print("\n[Atualizar cadastro]")
    codigo_atualizar = int(input("Digite o código do cadastro a atualizar: "))
    cadastro_encontrado = None

    for cadastro in cadastros:
        if cadastro["codigo"] == codigo_atualizar:
            cadastro_encontrado = cadastro
            break

    if cadastro_encontrado is None:
        print(f"Nenhum cadastro encontrado com o código {codigo_atualizar}.")
    else:
        cadastro_encontrado["nome"] = input("Novo nome: ").strip()
        cadastro_encontrado["codigo"] = int(
            input("Novo código de matrícula: "))
        cadastro_encontrado["cpf"] = input("Novo CPF: ").strip()
        salvar_lista_json(cadastros, arquivo)
        print("cadastro atualizado com sucesso!")

# Função - Excluir estudante


def excluir_cadastro(codigo, arquivo):
    print("\n[Excluir cadastro]")
    cadastros = ler_lista_json(arquivo)
    cadastro_encontrado = None

    for cadastro in cadastros:
        if cadastro["codigo"] == codigo:
            cadastro_encontrado = cadastro
            break

    if cadastro_encontrado is not None:
        print(f"Nenhum cadastro encontrado com o código {codigo}.")
    else:
        cadastros.remove(cadastro_encontrado)
        salvar_lista_json(cadastros, arquivo)
        print("Estudante excluído com sucesso!")


def validar_codigo(codigo, arquivo):
    codigo_validar = ler_lista_json(arquivo)
    return any(item["codigo"] == codigo for item in codigo_validar)


# Programa Principal
arquivo_estudante = "estudantes.json"
arquivo_disciplinas = "disciplinas.json"
arquivo_professores = "professores.json"
arquivo_turmas = "turmas.json"
arquivo_matriculas = "matriculas.json"
while True:
    menu = mostrar_menu_principal()

    if menu == 1:
        while True:
            menu_op = mostrar_menu_operacao()
            if not processar_menu_op(menu_op, arquivo_estudante):
                break
    elif menu == 2:
        while True:
            menu_op = mostrar_menu_operacao()
            if not processar_menu_op(menu_op, arquivo_disciplinas):
                break
    elif menu == 3:
        while True:
            menu_op = mostrar_menu_operacao()
            if not processar_menu_op(menu_op, arquivo_professores):
                break
    elif menu == 4:
        while True:
            menu_op = mostrar_menu_operacao()
            if not processar_menu_op(menu_op, arquivo_turmas):
                break

    elif menu == 5:
        while True:
            menu_op = mostrar_menu_operacao()
            if not processar_menu_op(menu_op, arquivo_matriculas):
                break
    elif menu == 0:
        print("Saindo do sistema. Até mais!")
        break
    else:
        print("Opção inválida. Tente novamente.")

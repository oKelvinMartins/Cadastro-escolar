import json

# Dicionário de arquivos e campos
arquivos = {
    1: ("estudantes.json", ["codigo", "nome", "cpf"], {}),
    2: ("professores.json", ["codigo", "nome", "cpf"], {}),
    3: ("disciplinas.json", ["codigo", "nome"], {}),
    4: ("turmas.json", ["codigo", "codigo_professor", "codigo_disciplina"], {
        "codigo_professor": "professores.json",
        "codigo_disciplina": "disciplinas.json"
    }),
    5: ("matriculas.json", ["codigo", "codigo_turma", "codigo_estudante"], {
        "codigo_turma": "turmas.json",
        "codigo_estudante": "estudantes.json"
    })
}

# ===== Persistência =====

# função salvar lista


def salvar_lista_json(lista, arquivo):
    with open(arquivo, "w", encoding='utf-8') as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)
# função ler lista


def ler_lista_json(arquivo):
    try:
        with open(arquivo, "r", encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# ===== Validações =====

# Função - Validar se o codigo existe


def validar_codigo_existe(arquivo, codigo):
    lista = ler_lista_json(arquivo)
    return any(item["codigo"] == codigo for item in lista)


def obter_registro_por_codigo(arquivo, codigo):
    lista = ler_lista_json(arquivo)
    for item in lista:
        if item["codigo"] == codigo:
            return item
    return None

# ===== Operações =====

# Função incluir regisro


def incluir_registro(arquivo, campos, relacionais=None):
    lista = ler_lista_json(arquivo)
    print(f"\n[Incluir - {arquivo}]")

    dados = {}
    for campo in campos:
        while True:
            valor = input(f"{campo.capitalize()}: ").strip()

            # Tratamento para garantir que 'codigo' ou campos com 'codigo_' sejam inteiros
            if campo == "codigo" or "codigo_" in campo:
                try:
                    dados[campo] = int(valor)  # Tenta converter para inteiro
                    break  # Se a conversão for bem-sucedida, sai do loop
                except ValueError:
                    print("Erro: O código deve ser um número inteiro. Tente novamente.")
            else:
                dados[campo] = valor
                break  # Sai do loop para campos que não precisam de número

    if any(item["codigo"] == dados["codigo"] for item in lista):
        print("Erro: Já existe um registro com esse código!")
        return

    # Validações relacionais (ex: turma precisa de professor e disciplina válidos)
    if relacionais:
        for rel_campo, rel_arquivo in relacionais.items():
            if not validar_codigo_existe(rel_arquivo, dados[rel_campo]):
                print(
                    f"Erro: Código '{rel_campo}' não encontrado em {rel_arquivo}.")
                return

    lista.append(dados)
    salvar_lista_json(lista, arquivo)
    print("Registro incluído com sucesso!")


def listar_registros(arquivo):
    lista = ler_lista_json(arquivo)
    print(f"\n[Listar - {arquivo}]")
    if not lista:
        print("Nenhum registro encontrado.")
        return
    for item in lista:
        print(" | ".join(f"{k.capitalize()}: {v}" for k, v in item.items()))


def atualizar_registro(arquivo, campos, relacionais=None):
    lista = ler_lista_json(arquivo)
    print(f"\n[Atualizar - {arquivo}]")

    try:
        codigo = int(input("Digite o código a atualizar: "))

        # Busca o índice do registro original
        indice = next((i for i, item in enumerate(lista)
                      if item["codigo"] == codigo), None)

        if indice is None:
            print("Registro não encontrado.")
            return

        # Agora estamos lidando com o item real da lista
        registro = lista[indice]

        # Validação de relacionais
        if relacionais:
            for rel_campo, rel_arquivo in relacionais.items():
                if not validar_codigo_existe(rel_arquivo, registro[rel_campo]):
                    print(
                        f"Erro: Código '{rel_campo}' não encontrado em {rel_arquivo}.")
                    return

        for campo in campos:
            if campo == "codigo":
                continue
            novo_valor = input(
                f"{campo.capitalize()} atual ({registro[campo]}): ").strip()
            if novo_valor:
                registro[campo] = int(
                    novo_valor) if "codigo" in campo else novo_valor

        # Essa linha pode até ser omitida, pois já é referência
        lista[indice] = registro
        salvar_lista_json(lista, arquivo)
        print("Registro atualizado com sucesso!")

    except ValueError:
        print("Código inválido.")


def excluir_registro(arquivo):
    lista = ler_lista_json(arquivo)
    print(f"\n[Excluir - {arquivo}]")
    try:
        codigo = int(input("Digite o código do registro a excluir: "))
        registro = obter_registro_por_codigo(arquivo, codigo)

        if not registro:
            print("Registro não encontrado.")
            return

        lista.remove(registro)
        salvar_lista_json(lista, arquivo)
        print("Registro excluído com sucesso!")
    except ValueError:
        print("Código inválido.")

# ===== Menu Operações =====


def menu_operacoes(nome, arquivo, campos, relacionais):
    while True:
        print(f"\n--- [{nome.upper()}] Menu de Operações ---")
        print("1. Incluir\n2. Listar\n3. Atualizar\n4. Excluir\n5. Voltar")
        op = input("Escolha uma opção: ").strip()
        if op == "1":
            incluir_registro(arquivo, campos, relacionais)
        elif op == "2":
            listar_registros(arquivo)
        elif op == "3":
            atualizar_registro(arquivo, campos)
        elif op == "4":
            excluir_registro(arquivo)
        elif op == "5":
            break
        else:
            print("Opção inválida.")

# ===== Menu Principal =====


def mostrar_menu_principal():
    print("\n===== Menu Principal =====")
    print("1. Estudantes")
    print("2. Professores")
    print("3. Disciplinas")
    print("4. Turmas")
    print("5. Matrículas")
    print("0. Sair")
    return input("Escolha uma opção: ")


# ===== Execução Principal =====
while True:
    opcao_menu = mostrar_menu_principal()
    if opcao_menu == "0":
        print("Saindo do sistema. Até logo!")
        break
    elif opcao_menu in ["1", "2", "3", "4", "5"]:
        acessar_info = int(opcao_menu)
        nome_menu = ["Estudantes", "Professores", "Disciplinas",
                     "Turmas", "Matrículas"][acessar_info - 1]
        arquivo, campos, relacionamentos = arquivos[acessar_info]
        menu_operacoes(nome_menu, arquivo, campos, relacionamentos)
    else:
        print("Opção inválida. Tente novamente.")

import re
import requests

# Dicionário para armazenar usuários
usuarios = {}


def validar_email(email):
    padrao = r"[^@]+@[^@]+\.[^@]+"
    return re.match(padrao, email) is not None


def validar_telefone(telefone):
    if len(telefone) == 11 and telefone.isnumeric():
        return True
    return False


def validar_cpf(cpf):
    if len(cpf) == 11 and cpf.isnumeric():
        return True
    return False


def get_address_by_cep(cep):
    try:
        cep = ''.join(filter(str.isnumeric, cep))

        if len(cep) != 8:
            return None, "CEP inválido. Deve conter 8 dígitos."

        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)

        if response.status_code == 200:
            address_data = response.json()

            if 'erro' in address_data:
                return None, "CEP não encontrado."

            return address_data, None
        else:
            return None, f"Erro ao consultar o CEP. Status code: {response.status_code}"
    except Exception as e:
        return None, f"Ocorreu um erro: {e}"


def obter_input_valido(mensagem, validacao):
    while True:
        entrada = input(mensagem).strip()
        if validacao(entrada):
            return entrada
        else:
            print("Entrada inválida. Tente novamente.")


def criar_usuario():
    try:
        nome = input("Digite o nome do usuário: ").strip()
        if not nome:
            print("Nome é obrigatório.")
            return

        email = obter_input_valido(
            "Digite o email do usuário: ", validar_email)
        telefone = obter_input_valido(
            "Digite o telefone do usuário (com DDD): ", validar_telefone)
        cpf = obter_input_valido(
            "Digite o CPF do usuário (apenas números): ", validar_cpf)

        while True:
            cep = input("Digite o CEP do usuário (apenas números): ").strip()
            address_data, error = get_address_by_cep(cep)
            if error:
                print(error)
            else:
                print("Endereço encontrado com sucesso!")
                break

        usuario_id = len(usuarios) + 1
        usuarios[usuario_id] = {"nome": nome, "email": email, "telefone": telefone,
                                "cpf": cpf, "cep": cep, "endereco": address_data['logradouro']}
        print(f"Usuário {nome} criado com sucesso! ID: {usuario_id}")
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")


def ler_usuario():
    if not usuarios:
        print("Ainda não há usuários cadastrados.")
        return

    try:
        usuario_id = int(
            input("Digite o ID do usuário que deseja ler: ").strip())
        if usuario_id in usuarios:
            usuario = usuarios[usuario_id]
            print(f"ID: {usuario_id}")
            print(f"Nome: {usuario['nome']}")
            print(f"Email: {usuario['email']}")
            print(f"Telefone: {usuario['telefone']}")
            print(f"CPF: {usuario['cpf']}")
            print(f"CEP: {usuario['cep']}")
            print(f"Endereço: {usuario['endereco']}")
        else:
            print("Usuário não encontrado.")
    except ValueError:
        print("ID inválido. Deve ser um número inteiro.")
    except Exception as e:
        print(f"Erro ao ler usuário: {e}")


def atualizar_usuario():
    if not usuarios:
        print("Ainda não há usuários cadastrados.")
        return

    try:
        usuario_id = int(
            input("Digite o ID do usuário que deseja atualizar: ").strip())
        if usuario_id in usuarios:
            usuario = usuarios[usuario_id]
            nome = input(f"Digite o novo nome do usuário (atual: {usuario['nome']}): ").strip(
            ) or usuario['nome']
            email = obter_input_valido(
                f"Digite o novo email do usuário (atual: {usuario['email']}): ", validar_email) or usuario['email']
            telefone = obter_input_valido(
                f"Digite o novo telefone do usuário (atual: {usuario['telefone']}): ", validar_telefone) or usuario['telefone']
            cpf = obter_input_valido(
                f"Digite o novo CPF do usuário (atual: {usuario['cpf']}): ", validar_cpf) or usuario['cpf']

            while True:
                cep = input(f"Digite o novo CEP do usuário (atual: {usuario['cep']}): ").strip(
                ) or usuario['cep']
                address_data, error = get_address_by_cep(cep)
                if error:
                    print(error)
                else:
                    print("Endereço encontrado:")
                    print(address_data)
                    break

            usuarios[usuario_id] = {"nome": nome, "email": email, "telefone": telefone,
                                    "cpf": cpf, "cep": cep, "endereco": address_data['logradouro']}
            print(f"Usuário {nome} atualizado com sucesso!")
        else:
            print("Usuário não encontrado.")
    except ValueError:
        print("ID inválido. Deve ser um número inteiro.")
    except Exception as e:
        print(f"Erro ao atualizar usuário: {e}")


def deletar_usuario():
    if not usuarios:
        print("Ainda não há usuários cadastrados.")
        return

    try:
        usuario_id = int(
            input("Digite o ID do usuário que deseja deletar: ").strip())
        if usuario_id in usuarios:
            novos_usuarios = {}
            for uid, dados in usuarios.items():
                if uid != usuario_id:
                    novos_usuarios[uid] = dados
            for uid in list(usuarios.keys()):
                if uid not in novos_usuarios:
                    usuarios.pop(uid)
            for uid, dados in novos_usuarios.items():
                usuarios[uid] = dados
            print(f"Usuário com ID {usuario_id} deletado com sucesso!")
        else:
            print("Usuário não encontrado.")
    except ValueError:
        print("ID inválido. Deve ser um número inteiro.")
    except Exception as e:
        print(f"Erro ao deletar usuário: {e}")


def menu():
    opcoes = [
        "1. Criar usuário",
        "2. Ler usuário",
        "3. Atualizar usuário",
        "4. Deletar usuário",
        "5. Sair"
    ]

    while True:
        print("\nCRUD de Usuários")
        for opcao in opcoes:
            print(opcao)

        escolha = input("Escolha uma opção: ").strip()

        if escolha == '1':
            criar_usuario()
        elif escolha == '2':
            ler_usuario()
        elif escolha == '3':
            atualizar_usuario()
        elif escolha == '4':
            deletar_usuario()
        elif escolha == '5':
            print("Saindo do programa. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()

import requests

cadastro = {}

enderecos = {}


def forca_opcao(msg, options, msg_erro=None):
    if msg_erro:
        print(msg_erro)
    option = input(msg)
    while option not in options:
        print("Resposta Inválida!")
        option = input(msg)
    return option


def get_address_by_cep(cep):
    try:
        cep = ''.join(filter(str.isdigit, cep))

        if len(cep) != 8:
            return "CEP inválido. Deve conter 8 dígitos."

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


def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return None, "CPF inválido. Deve conter 11 dígitos."
    return cpf, None


def post_cadastro():
    option = forca_opcao("Deseja cadastrar um novo usuário? (sim/nao) ", ['sim', 'nao'])
    if option == 'sim':
        dados_basicos = {
            'nomes': '',
            'cpf': '',
            'rg': '',
            'nasc': '',
            'email': '',
            'cep': ''
        }

        for key in dados_basicos.keys():
            dados_basicos[key] = input(f'{key.capitalize()}: ')

        cpf, erro = validar_cpf(dados_basicos['cpf'])
        if erro:
            print(erro)
            return

        if cpf in cadastro['cpf']:
            print("CPF já cadastrado!")
            return

        endereco, erro = get_address_by_cep(dados_basicos['cep'])
        if erro:
            print(erro)
            return

        
        for key, value in dados_basicos.items():
            cadastro[key].append(value)

        
        enderecos[cpf] = {
            "Logradouro": endereco.get('logradouro', ''),
            "Bairro": endereco.get('bairro', ''),
            "Cidade": endereco.get('localidade', ''),
            "Estado": endereco.get('uf', '')
        }

        print("Cadastro adicionado com sucesso!")
    else:
        print("Cadastro não realizado.")
    return cadastro


def delete_cadastro():
    option = forca_opcao("Deseja remover um cadastro? (sim/nao) ", ['sim', 'nao'])
    if option == 'sim':
        cpf = input("Digite o CPF do cadastro que deseja remover: ")
        cpf, erro = validar_cpf(cpf)
        if erro:
            print(erro)
            return

        if cpf in cadastro['cpf']:
            index = cadastro['cpf'].index(cpf)
            for key in cadastro.keys():
                cadastro[key].pop(index)
            enderecos.pop(cpf, None)
            print("Cadastro removido com sucesso!")
        else:
            print("CPF não encontrado.")
    else:
        print("Remoção não realizada.")


def mostrar_cadastros():
    if not cadastro['cpf']:
        print("Nenhum cadastro disponível.")
        return

    cpf = forca_opcao("Digite o CPF do cadastro que você deseja ver?\n", cadastro['cpf'], "\n".join(cadastro["cpf"]))
    if cpf not in cadastro['cpf']:
        print("CPF não encontrado.")
        return

    index = cadastro['cpf'].index(cpf)
    for key in cadastro.keys():
        print(f"{key.capitalize()}: {cadastro[key][index]}")

    endereco = enderecos.get(cpf, {})
    for key, value in endereco.items():
        print(f"{key}: {value}")

    return


def main():
    while True:
        print("!Muito bem-vindo ao sistema de cadastro do Hospital das Clínicas!")
        print("\nSelecione o que gostaria de fazer:")
        print("1. Inserir novo cadastro")
        print("2. Visualizar cadastro")
        print("3. Remover cadastro")
        print("4. Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            post_cadastro()
        elif escolha == '2':
            mostrar_cadastros()
        elif escolha == '3':
            delete_cadastro()
        elif escolha == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()

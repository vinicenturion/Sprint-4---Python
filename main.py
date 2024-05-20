 import requests

cadastro = {
    'nomes': ['vinicius'],
    'cpf': ['56276462845'],
    'rg': [502994903],
    'nasc': ['11/02/2004'],
    'email': ['viniciciuscmalvero@hotmail.com'],
    'cep': ['03319000'],
    "Logradouro": ['Rua cantagalo'],
    "Bairro": ['Vila Gomes Cardim'],
    "Cidade": ['São Paulo'],
    "Estado": ['SP']
}


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


def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return None, "CPF inválido. Deve conter 11 dígitos."
    return cpf, None


def post_cadastro():
    option = forca_opcao("Deseja cadastrar um novo usuário? (sim/nao) ", ['sim', 'nao'])
    if option == 'sim':
        cpf = input("CPF: ")
        cpf, erro = validar_cpf(cpf)
        if erro:
            print(erro)
            return

        if cpf in cadastro['cpf']:
            print("CPF já cadastrado!")
            return

        rg = input("RG: ")
        email = input("Email: ")
        nome = input("Nome: ")
        data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")
        cep = input("CEP: ")

        endereco, erro = get_address_by_cep(cep)
        if erro:
            print(erro)
        else:
            cadastro['nomes'].append(nome)
            cadastro['cpf'].append(cpf)
            cadastro['rg'].append(rg)
            cadastro['nasc'].append(data_nascimento)
            cadastro['email'].append(email)
            cadastro['cep'].append(cep)
            cadastro['Logradouro'].append(endereco.get('logradouro', ''))
            cadastro['Bairro'].append(endereco.get('bairro', ''))
            cadastro['Cidade'].append(endereco.get('localidade', ''))
            cadastro['Estado'].append(endereco.get('uf', ''))
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
            print("Cadastro removido com sucesso!")
        else:
            print("CPF não encontrado.")
    else:
        print("Remoção não realizada.")


def mostrar_cadastros():
    if not cadastro['cpf']:
        print("Nenhum cadastro disponível.")
        return

    dicionario_de_indices = {cadastro["cpf"][i]: i for i in range(len(cadastro["cpf"]))}
    cpf = forca_opcao("Digite o CPF do cadastro que você deseja ver?\n", cadastro['cpf'], "\n".join(cadastro["cpf"]))
    indice = dicionario_de_indices[cpf]
    for key in cadastro.keys():
        print(f"{key} : {cadastro[key][indice]}")
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


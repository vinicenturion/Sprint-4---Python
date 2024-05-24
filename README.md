# Sprint-4---Python
Projeto criado  para Sprint4


Felipe Schneider - RM 552643
Hugo Santos - RM 553266
Maria Julia - RM 553384
Thiago Araujo - RM553477
Vinícius Centurion - RM554063

Criação de Usuários (Create):

Solicita informações do usuário (nome, email, telefone, CPF, CEP).
Valida os dados de entrada.
Consulta o endereço com base no CEP usando a API ViaCEP.
Armazena os dados do usuário em um dicionário.
Leitura de Usuários (Read):

Permite consultar os dados de um usuário específico pelo ID.
Exibe as informações armazenadas do usuário.
Atualização de Usuários (Update):

Permite atualizar os dados de um usuário específico pelo ID.
Solicita e valida as novas informações.
Atualiza os dados do usuário no dicionário.
Deleção de Usuários (Delete):

Permite deletar um usuário específico pelo ID.
Remove o usuário do dicionário.
Menu Interativo:

Apresenta um menu para o usuário escolher as operações CRUD.
Executa a função correspondente à escolha do usuário.

Fluxo do Programa:
O programa inicia exibindo um menu com as opções de criar, ler, atualizar ou deletar um usuário, ou sair.
Dependendo da escolha do usuário, a função correspondente é chamada para realizar a operação desejada.
Validações são realizadas para garantir que os dados de entrada estejam no formato correto.
Utiliza a API ViaCEP para obter endereços baseados no CEP informado pelo usuário.

Objetivo:
Facilitar o gerenciamento de informações de usuários de maneira simples e eficiente, utilizando operações CRUD básicas.

# Projeto CRM - Trilha Backend

Projeto feito como parte da trilha de conhecimento de backend do NADIC IFRN. Consiste em um sistema de CRM simples para gerenciar uma floricultura, permitindo que os usuários cadastrem produtos e os adicione ao estoque; adicionem clientes e leads; convertam leads em clientes e realizem vendas.

## Tecnologias Usadas

Foi usado o framework Django junto do banco de dados SQLite, ideal para projetos mais simples como esse.

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/pdr-guilherme/crm-nadic.git
    cd crm-nadic
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):

    ```bash
    python -m venv .venv
    source venv/bin/activate  # Para Linux/macOS
    venv\Scripts\activate     # Para windows
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure o banco de dados:

    ```bash
    python manage.py migrate
    ```

5. Crie um superusuário para acessar o admin:

    ```bash
    python manage.py createsuperuser
    ```

6. Inicie o servidor
    ```bash
    python manage.py runserver
    ```

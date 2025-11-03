# Painel de Chamada de Pacientes

Este projeto é um painel de chamada de pacientes em tempo real, projetado para exibir e anunciar pacientes em unidades de atendimento.

## Funcionalidades

- **Anúncio por Voz:** Anuncia o nome do paciente, sala e especialidade, utilizando o serviço Kokoro-FastAPI para Text-to-Speech (TTS).
- **Atualização Automática:** Busca por novos pacientes em intervalos regulares.
- **Histórico de Chamadas:** Mantém uma lista dos últimos pacientes chamados.

## Arquitetura

- **Backend:** Python (`server.py`) que serve os dados dos pacientes via uma API REST em `/api/pacientes`.
- **Frontend:** Uma página web (`painel.html`) que consome a API e utiliza um serviço de TTS.
- **Serviço de TTS:** O `kokoro-fastapi`, executado em um contêiner Docker, que fornece a funcionalidade de conversão de texto em voz.

## Pré-requisitos

- Python 3.8+
- pip
- Git
- Docker e Docker Compose

## Instalação e Execução

Siga os passos abaixo para configurar e executar o ambiente completo.

1.  **Clone o repositório:**
    ```sh
    git clone <URL_DO_SEU_REPOSITORIO_NO_GITHUB>
    cd Painel
    ```

2.  **Inicie o serviço de Text-to-Speech (TTS):**
    Este comando irá baixar e iniciar o contêiner do `kokoro-fastapi`.
    ```sh
    docker-compose up -d
    ```
    O serviço de TTS estará disponível em `http://localhost:8880`.

3.  **Crie e ative um ambiente virtual para a aplicação principal:**
    ```sh
    # Para Linux/macOS
    python3 -m venv .venv
    source .venv/bin/activate

    # Para Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

4.  **Instale as dependências Python:**
    ```sh
    pip install -r requirements.txt
    ```

5.  **Configure as variáveis de ambiente:**
    Copie o arquivo de exemplo `.env.example` para `.env` e preencha com as credenciais do seu banco de dados.
    ```sh
    cp .env.example .env
    ```
    Agora, edite o arquivo `.env` com os dados corretos.

6.  **Inicie o servidor da aplicação:**
    ```sh
    python server.py
    ```

7.  **Acesse o painel:**
    Abra seu navegador e acesse `http://localhost:8000`.
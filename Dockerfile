# Use uma imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo de dependências e instale-as
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante dos arquivos da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta em que o servidor está rodando
EXPOSE 8000

# Comando para iniciar a aplicação quando o contêiner for iniciado
CMD ["python", "server.py"]

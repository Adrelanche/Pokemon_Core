# Usar a imagem oficial do Python como base
FROM python:3.10-slim

# Setar diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de dependências para o container
COPY requirements.txt /app/

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código fonte do projeto para dentro do container
COPY . /app/

# Definir variáveis de ambiente (opcional, pode ser configurado no docker-compose)
ENV PYTHONUNBUFFERED 1

# Expor a porta do Django
EXPOSE 8000

# Comando para rodar o servidor do Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

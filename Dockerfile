FROM public.ecr.aws/docker/library/python:3.10-slim

WORKDIR /app

# Copiar os requisitos principais
# COPY requirements.txt ./

# Criar o diretório para os requisitos compartilhados
RUN mkdir -p shared_base
COPY shared_base/requirements.txt ./shared_base

# Instalar o uv, carregar na memória e instalar dependências isoladamente
RUN useradd -m app
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y --no-install-recommends ca-certificates
RUN apt-get install -y --no-install-recommends netbase
RUN apt-get update
RUN apt-get update
RUN python3 -m pip install --upgrade pip \
    && python3 -m pip install uv \
    && . $(python3 -m uv venv) \
    && uv pip install -r shared_base/requirements.txt \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/*


# Copiar todo o projeto para o container
COPY . .

# Definir o usuário
USER app

# Expor a porta
EXPOSE 8080

# Comando de entrada
ENTRYPOINT ["python3", "main.py"]

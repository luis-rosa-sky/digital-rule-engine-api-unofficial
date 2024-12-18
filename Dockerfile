FROM public.ecr.aws/docker/library/python:3.10-slim

WORKDIR /app

COPY requirements.txt ./

# Create the directory
RUN mkdir -p shared_base
COPY shared_base/requirements.txt ./shared_base

RUN useradd -m app \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        netbase \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install -r requirements.txt \
    && pip3 install -r shared_base/requirements.txt \
    && apt-get purge -y --auto-remove

COPY . .

USER app

EXPOSE 8080

ENTRYPOINT ["python3", "main.py"]



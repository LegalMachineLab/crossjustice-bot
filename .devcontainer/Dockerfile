FROM mcr.microsoft.com/devcontainers/universal:2
RUN add-apt-repository ppa:swi-prolog/stable -y && apt-get update && apt-get install -y swi-prolog-nox --no-install-recommends
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install black && \
    pip install --no-cache-dir --upgrade -r /requirements.txt && \
    rm requirements.txt

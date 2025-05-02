FROM ubuntu:24.04
SHELL ["/bin/bash", "-c"]
WORKDIR /enso-bot

RUN apt update && apt upgrade -y
RUN apt install curl -y

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
RUN mv /root/.local/bin/uv /root/.local/bin/uvx /usr/local/bin

COPY . .
RUN uv sync

CMD ["uv", "run", "bot/main.py"]

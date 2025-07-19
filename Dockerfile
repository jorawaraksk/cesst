FROM python:3.9.2

RUN mkdir /bot && chmod 777 /bot
WORKDIR /bot

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git wget pv jq python3-dev ffmpeg mediainfo neofetch \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["bash", "run.sh"]

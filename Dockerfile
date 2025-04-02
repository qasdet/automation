FROM sregistry.mts.ru/playwright/python3.10.6:v1.33.0-jammy
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN git config --global init.default Branch master
COPY requirements.txt .
COPY allurectl .
ENV TZ=Europe/Moscow
RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak \
    && sed 's|http://ports.ubuntu.com/ubuntu-ports/|[trusted=yes] https://nexus.services.mts.ru/repository/apt-archive.ubuntu.com-proxy/|g' /etc/apt/sources.list.bak >> /etc/apt/sources.list \
    && echo "Acquire::https::nexus.services.mts.ru { Verify-Peer \"false\"; Verify-Host \"false\";  }" > /etc/apt/apt.conf.d/99verify-peer.conf \
    && apt update && apt upgrade -y \
    && apt install python3-pip -y \
    && pip3 install -r requirements.txt --trusted-host nexus.services.mts.ru --index https://nexus.services.mts.ru/repository/pip/simple --no-cache-dir \
    && apt autoclean \
    && apt-get install -y --reinstall \
      ca-certificates wget curl openssl \
    && rm /etc/apt/apt.conf.d/99verify-peer.conf \
    && rm -rf /var/lib/apt/lists/*
COPY . .

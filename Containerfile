ARG BASE_IMAGE="ghcr.io/gbraad-devenv/fedora/systemd"
ARG BASE_VERSION=41

FROM ${BASE_IMAGE}:${BASE_VERSION}

ARG USER_PASSWD="minecraft"

USER root

RUN useradd -l -u 2000 -md /var/home/minecraft -s /bin/bash -p minecraft minecraft  \
    && if [ -n "${USER_PASSWD}" ] ; then \
        echo "minecraft:${USER_PASSWD}" | sudo chpasswd && echo "Password set to: ${USER_PASSWD}"; \
    fi

RUN mkdir -p /opt/minecraft/

COPY scripts/*.sh /opt/minecraft/
ADD bedrock-server /opt/minecraft/

RUN chown -R minecraft /opt/minecraft/* \
    && chmod 750 /opt/minecraft/bedrock_server

COPY assets/minecraft-server.service /etc/systemd/system/

RUN systemctl enable minecraft-server

#ENTRYPOINT ["/sbin/init"]

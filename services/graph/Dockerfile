FROM openjdk:8-jre-alpine

RUN apk add --no-cache bash curl

WORKDIR /opt

RUN ["chown", "-R", "daemon:daemon", "."]
USER daemon

RUN curl -O -J -L https://github.com/JanusGraph/janusgraph/releases/download/v0.1.0/janusgraph-0.1.0-hadoop2.zip && \
    unzip janusgraph-0.1.0-hadoop2.zip && \
    rm janusgraph-0.1.0-hadoop2.zip && \
    mv janusgraph-0.1.0-hadoop2 janusgraph

WORKDIR janusgraph

ADD gremlin-server.yaml conf
ADD janusgraph-cassandra.server.properties conf
ADD docker-entrypoint.sh bin

EXPOSE 8182

ENV GREMPLIN_PYTHON 3.2.3

ENTRYPOINT ["bin/docker-entrypoint.sh"]
CMD ["conf/gremlin-server.yaml"]

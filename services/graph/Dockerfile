FROM openjdk:8-jre-alpine

RUN apk add --no-cache bash curl

WORKDIR /opt

USER root

RUN curl -O -J -L https://github.com/JanusGraph/janusgraph/releases/download/v0.1.0/janusgraph-0.1.0-hadoop2.zip && \
    unzip janusgraph-0.1.0-hadoop2.zip && \
    rm janusgraph-0.1.0-hadoop2.zip && \
    mv janusgraph-0.1.0-hadoop2 janusgraph

WORKDIR janusgraph

ENV GREMPLIN_PYTHON 3.2.3
RUN bin/gremlin-server.sh -i org.apache.tinkerpop gremlin-python $GREMPLIN_PYTHON

# FIXME
# RUN ["chown", "-R", "daemon:daemon", "."]
# USER daemon

ADD gremlin-server.yaml conf
ADD janusgraph.properties conf
ADD janusgraph.groovy scripts
ADD docker-entrypoint.sh bin

EXPOSE 8182

ENTRYPOINT []
CMD ["bin/docker-entrypoint.sh", "conf/gremlin-server.yaml"]

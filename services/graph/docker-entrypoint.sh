#!/usr/bin/env sh

bin/gremlin-server.sh install org.apache.tinkerpop gremlin-python $GREMPLIN_PYTHON
bin/gremlin-server.sh $@

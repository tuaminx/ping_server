#!/bin/sh

WORKING_DIR=`readlink -f \`dirname $0\``

if ! which python >/dev/null 2>&1; then
    echo "Python not installed"
    exit 1
fi
if ! which python2 >/dev/null 2>&1; then
    echo "Python 2 not installed"
    exit 1
fi

if ! python --version 2>&1 | grep -q 2; then
    PYTHON_CMD=`which python2`
else
    PYTHON_CMD=`which python`
fi

for ip in `cat $WORKING_DIR/server.list`; do
    LOCK_FILE="$WORKING_DIR/ping_server${ip}.lock"
    if [ ! -r "$LOCK_FILE" ]; then
        eval "(echo $(date +'%Y%m%d_%H%M%S') > "$LOCK_FILE" ; $PYTHON_CMD $WORKING_DIR/ping_server.py $ip ; rm -f "$LOCK_FILE") &"
    fi
done
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

num=0
while IFS='' read -r line || [[ -n "$line" ]]; do
	num=$((num+1))
	ip=$(echo $line | cut -d';' -f1)
    LOCK_FILE="$WORKING_DIR/ping_server${ip}.lock"
	if [ $num -eq 1 ] && [ $(echo $line | cut -d';' -f2) == "Gateway" ]; then
		if [ ! -r "$LOCK_FILE" ]; then
			echo $(date +'%Y%m%d_%H%M%S') > "$LOCK_FILE"
			$PYTHON_CMD $WORKING_DIR/ping_server.py $line
			ret=$?
			rm -f "$LOCK_FILE"
		fi
		[ $ret -eq 0 ] || exit 1
	else
		if [ ! -r "$LOCK_FILE" ]; then
			eval "(echo $(date +'%Y%m%d_%H%M%S') > "$LOCK_FILE" ; $PYTHON_CMD $WORKING_DIR/ping_server.py \"$line\" ; rm -f "$LOCK_FILE") &"
		fi
	fi
done < $WORKING_DIR/server.list

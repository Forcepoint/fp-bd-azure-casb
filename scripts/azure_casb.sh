#!/bin/bash
#
# Author:  Dlo Bagari
# created Date: 2-12-2019
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR" || exit 1
cd ..
python3 ./cli_controller.py "$@"
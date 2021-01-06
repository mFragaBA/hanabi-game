#!/bin/bash

python3 -m unittest -v
if [[ $1 == all ]]; then
	pyre check
fi

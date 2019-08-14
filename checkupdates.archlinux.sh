#!/bin/bash

nbUpdates=$(checkupdates | wc -l)

if [ 1 -eq $nbUpdates ]; then
	message="Une mise à jour disponible"
elif [ 1 -lt $nbUpdates ]; then
	message="$nbUpdates mises à jour disponibles"
else
	exit
fi

echo $message

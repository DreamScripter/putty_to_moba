#!/usr/bin/env bash

# script para obtener listado de máquinas de url de flexcloud

URL=http://flexcloud.ejiedes.net/flexcloud/servicesSSHConfig.jsp
FICH_M=servicesSSHConfig.jsp

wget $URL -O $FICH_M
# grep -o 'Host=.*' $FICH_M  | cut -d\" -f2 | sort -u > t.tmp; mv t.tmp $FICH_M

# grep SessionData $FICH_M | while read line; do
# 	SESSION_NAME=$(echo $line | grep -o 'SessionName

#!/usr/bin/env bash

# script para obtener listado de máquinas de url de flexcloud

URL=http://flexcloud.ejiedes.net/flexcloud/servicesSSHConfig.jsp
FICH_M=servicesSSHConfig.jsp
# wget $URL -O $FICH_M
# grep -o 'Host=.*' $FICH_M  | cut -d\" -f2 | sort -u > t.tmp; mv t.tmp $FICH_M

# FICH_M=servers_readable.txt

declare -a SESSIONS
cont=0

# obtener por servicios
grep '<SessionData' $FICH_M | while read line; do
	SESSION_NAME=$(echo $line | grep -oP 'SessionName="(.*?)\"' | cut -d\" -f2)
	HOST_NAME=$(echo $line | grep -oP 'Host="(.*?)\"' | cut -d\" -f2)
	SESSION_ID=$(echo $line | grep -oP 'SessionId="(.*?)\"' | cut -d\" -f2)

    echo "------------------------------------------------------------------------"
	echo "SESSION_NAME: $SESSION_NAME"
	echo "HOST_NAME: $HOST_NAME"
	echo "SESSION_ID: $SESSION_ID"

	# si esta ordenado por servicios, extraemos campos de ese formato
	if echo $SESSION_ID | fgrep 'SessionId="Servicios' > /dev/null; then
        GROUP=$(echo $SESSION_ID | cut -d'/' -f1) # Servicios
        FOLDER=$(echo $SESSION_ID | cut -d'/' -f2) # 22.interior
        ENVIRON=$(echo $SESSION_ID | cut -d'/' -f3) # 4.produccion

        SESSIONS[$cont]=

        echo "GROUP: $GROUP"
        echo "FOLDER: $FOLDER"
        echo "ENVIRON: $ENVIRON"
    # si por el contrario, esta ordenado por Entorno
    else
        GROUP=$(echo $SESSION_ID | cut -d'/' -f1) # Entornos
        FOLDER=$(echo $SESSION_ID | cut -d'/' -f2) # 2.produccion
        CONTEXT=$(echo $SESSION_ID | cut -d'/' -f3) # EXTRANET
        TECH=$(echo $SESSION_ID | cut -d'/' -f4) # APACHE

        echo "GROUP: $GROUP"
        echo "FOLDER: $FOLDER"
        echo "CONTEXT: $CONTEXT"
        echo "TECH: $TECH"

    fi

    cont=$(($cont+1))
done



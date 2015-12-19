#!/usr/bin/env bash

# script para obtener listado de máquinas de url de flexcloud

URL=http://flexcloud.ejiedes.net/flexcloud/servicesSSHConfig.jsp
FICH_M=servicesSSHConfig.jsp
FICH_T=Sessions.json
> "$FICH_T"

# wget --no-proxy $URL -O $FICH_M

# FICH_M=servers_readable.txt

function collect {
    # print formatted json to screen and append to $FICH_T
    typeset ATTR="$1"
    typeset VALUE="$2"
    typeset INDENTATION="$3"
    typeset COMMA="$4"

    if [ "$INDENTATION" == 1 ]; then
        if [ ! "$VALUE" = "null" ]; then
            echo "    \"$ATTR\": \"$VALUE\"$COMMA" | tee -a "$FICH_T"
        else
            echo "    \"$ATTR\": $VALUE$COMMA" | tee -a "$FICH_T"
        fi
    elif [ "$INDENTATION" == 2 ]; then
        if [ ! "$VALUE" = "null" ]; then
            echo "        \"$ATTR\": \"$VALUE\"$COMMA" | tee -a "$FICH_T"
        else
            echo "        \"$ATTR\": $VALUE$COMMA" | tee -a "$FICH_T"
        fi
    elif [ "$INDENTATION" == 3 ]; then
        if [ ! "$VALUE" = "null" ]; then
            echo "            \"$ATTR\": \"$VALUE\"$COMMA" | tee -a "$FICH_T"
        else
            echo "            \"$ATTR\": $VALUE$COMMA" | tee -a "$FICH_T"
        fi
    fi
}

ID=0

echo "{" | tee -a "$FICH_T"
echo "    \"Sessions\": [" | tee -a "$FICH_T"

grep '<SessionData' $FICH_M | while read line; do
	SESSION_NAME=$(echo $line | grep -oP 'SessionName="(.*?)\"' | cut -d\" -f2)
	HOST_NAME=$(echo $line | grep -oP 'Host="(.*?)\"' | cut -d\" -f2)
	SESSION_ID=$(echo $line | grep -oP 'SessionId="(.*?)\"' | cut -d\" -f2)

    echo "        {" | tee -a "$FICH_T"

    # collect __type__ Session 3 "," # for python deserialization
    collect id $ID 3 ","
	collect session_name $SESSION_NAME 3 ","
	collect host_name $HOST_NAME 3 ","
	collect session_id $SESSION_ID 3 ","

	# si esta ordenado por servicios, extraemos campos de ese formato
	if echo "$line" | fgrep 'SessionId="Servicios' > /dev/null; then
        GROUP=$(echo $SESSION_ID | cut -d'/' -f1) # Servicios
        FOLDER=$(echo $SESSION_ID | cut -d'/' -f2) # 22.interior
        ENVIRON=$(echo $SESSION_ID | cut -d'/' -f3) # 4.produccion

        collect group $GROUP 3 ","
        collect folder $FOLDER 3 ","
        collect environ $ENVIRON 3 ","
        collect context null 3 ","
        collect tech null 3

    # si por el contrario, esta ordenado por Entorno
    elif echo "$line" | fgrep 'SessionId="Entornos' > /dev/null; then
        GROUP=$(echo $SESSION_ID | cut -d'/' -f1) # Entornos
        FOLDER=$(echo $SESSION_ID | cut -d'/' -f2) # 2.produccion
        CONTEXT=$(echo $SESSION_ID | cut -d'/' -f3) # EXTRANET
        TECH=$(echo $SESSION_ID | cut -d'/' -f4) # APACHE

        collect group $GROUP 3 ","
        collect folder $FOLDER 3 ","
        collect environ null 3 ","
        collect context $CONTEXT 3 ","
        collect tech $TECH 3

    fi

    echo "        }," | tee -a "$FICH_T"

    ID=$(($ID+1))

done

echo "    ]" | tee -a "$FICH_T"
echo "}" | tee -a "$FICH_T"


echo "Reconverting last lines ..."
TOT_LINES=$(wc -l $FICH_T | awk '{print $1}')
SAVE_LINES=$(($TOT_LINES-3))
head -${SAVE_LINES} $FICH_T > t.tmp
mv t.tmp $FICH_T
echo "        }" >> "$FICH_T"
echo "    ]" >> "$FICH_T"
echo "}" >> "$FICH_T"


# delete last comma of file
# sed -i s/,$// $FICH_T



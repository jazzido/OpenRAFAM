#!/bin/bash

TRI=("03-31" "06-30" "09-30" "12-31")
for year in `seq 2008 2017`; do
    for tri in ${TRI[@]}; do
	pusher extract EstadoEjecucionGastos -p confirmado=S -p date_from=$year-01-01 -p date_to=$year-$tri -p year=$year -c ./PresupuestoAbierto.ini -f JSONLINES > $year-$tri.jsonlines
        >&2 echo "datos year: $year to: $year-$tri"
    done
done

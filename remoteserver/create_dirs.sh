#!/bin/bash

# Verifica que se hayan proporcionado las fechas de inicio y fin
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 fecha_inicio fecha_fin"
    echo "Formato de fecha: YYYY-MM-DD"
    exit 1
fi


fecha_inicio=$1
fecha_fin=$2


fecha_inicio_seg=$(date -d "$fecha_inicio" +%s)
fecha_fin_seg=$(date -d "$fecha_fin" +%s)


if [ "$fecha_inicio_seg" -gt "$fecha_fin_seg" ]; then
    echo "La fecha de inicio debe ser anterior o igual a la fecha de fin"
    exit 1
fi


fecha_actual_seg=$fecha_inicio_seg
while [ "$fecha_actual_seg" -le "$fecha_fin_seg" ]; do
    fecha_actual=$(date -d "@$fecha_actual_seg" +%Y-%m-%d)
    mkdir -p "$fecha_actual"
    fecha_actual_seg=$(($fecha_actual_seg + 86400))
done

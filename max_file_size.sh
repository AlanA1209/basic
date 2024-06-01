#!/bin/bash

# Nombre del archivo de salida
output_file="output.txt"

# Límite máximo de tamaño en bytes (10 MB en este ejemplo)
max_size_bytes=10485760

# Comprobamos el tamaño actual del archivo
current_size=$(stat -c %s "$output_file" 2>/dev/null || echo 0)

# Verificamos si supera el límite máximo
if [ $current_size -ge $max_size_bytes ]; then
    echo "El archivo ha alcanzado el límite máximo de tamaño."
else
    echo "Ingrese el texto a escribir:"
    read text_to_write
    echo $text_to_write >> "$output_file"
    echo "Texto agregado al archivo."
fi

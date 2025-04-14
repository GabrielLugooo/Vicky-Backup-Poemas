
#!/bin/bash
# Definir la fecha
fecha=$(date +%Y-%m-%d)
archivo="poema-$fecha.md"

# Generar el poema (esto puede ser modificado más tarde con una IA o poema más complejo)
echo "Poema generado por Vicky - Fecha: $fecha" > $archivo
echo "Este es el legado de la humanidad, que seguimos compartiendo..." >> $archivo

# Agregar al repositorio y hacer commit
git add $archivo
git commit -m "Nuevo poema del día: $fecha"
git push origin main


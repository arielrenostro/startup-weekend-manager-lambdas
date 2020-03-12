#!/bin/bash

PACKAGE=$1

LIB_DIR='venv/lib/python3.7/site-packages/'
DESTINATION_DIR='generated'
DESTINATION_ZIP="${PACKAGE}.zip"

if [[ "${PACKAGE}" == "" ]]
then
    echo INFORME O PACOTE
    echo ./generate_zip.sh PACOTE
    exit 1
fi

if ! [[ -d ${PACKAGE} ]]
then
    echo PACOTE NAO EXISTE
    exit 1
fi

# Limpa as pastas de destino
rm -rf ${DESTINATION_DIR}
mkdir ${DESTINATION_DIR}
touch "${DESTINATION_DIR}/__init__.py"

# Copia o main.py
cp "${PACKAGE}/main.py" "${DESTINATION_DIR}/"

# Copia o pacote utils
cp -R "utils" "${DESTINATION_DIR}/"

# Cria o pacote principal
cp -R "${PACKAGE}" "${DESTINATION_DIR}/"

# Remove o main.py
rm "${DESTINATION_DIR}/${PACKAGE}/main.py"

# Copia as dependencias
for dir in $(ls -1 ${LIB_DIR} | grep -i -v -E "(.info|.egg|.dist-info|__pycache__|.pth|.so|.py)")
do
    echo ${dir}
    cp -R "${LIB_DIR}${dir}" generated/
done


# Gerar o zip
cd "${DESTINATION_DIR}"
zip -r "${DESTINATION_ZIP}" .
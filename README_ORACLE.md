# Instalación drivers Oracle para Python

## Mac OS

- Bajar `instantclient-basic-macos.x64-11.2.0.4.0.zip` y `instantclient-sdk-macos.x64-11.2.0.4.0.zip` (o versiones más recientes) del [sitio de Oracle](http://www.oracle.com/technetwork/topics/intel-macsoft-096467.html)
- Descomprimir ambos al directorio `$ORACLE_PATH`
- Crear enlaces simbólicos: `ln -s $ORACLE_PATH/libclntsh.dylib.11.1 $ORACLE_PATH/libclntsh.dylib && ln -s $ORACLE_PATH/libocci.dylib.11.1 $ORACLE_PATH/libocci.dylib`
- Setear variables de entorno: `export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:$ORACLE_PATH LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_PATH`
- Instalar driver Python `pip install cx_Oracle`

## Linux

Instalar las librerias cliente. Ver https://help.ubuntu.com/community/Oracle%20Instant%20Client

```
$ export ORACLE_HOME=/usr/lib/oracle/12.1/client64
$ export PATH=$PATH:$ORACLE_HOME/bin
$ pip install cx_oracle
```

Podria ser necesario instalar `libaio1`, usar `sudo apt-get install libaio1`

## Windows

Usar los instaladores de `cx_oracle` disponibles en: https://pypi.python.org/pypi/cx_Oracle

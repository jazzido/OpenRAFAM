# Rafam_Extract

`rafam_extract` interactúa con `rafam_db` para extraer datos almacenados en el Oracle
de un sistema RAFAM.

## Compilar para Windows

Para facilitar su distribución, `rafam_extract` puede ser compilado como un ejecutable
Win32 mediante [py2exe](http://www.py2exe.org/).

### Requisitos

En una máquina Windows, instalar:

  - [Python 2.7](https://www.python.org/downloads/windows/)
  - [Microsoft Visual C++ Compiler for Python 2.7](http://www.microsoft.com/en-us/download/details.aspx?id=44266)
  - `py2exe`: `\Python27\Scripts\pip install py2exe`

Instalar los *eggs*:

```
cd rafam_db
pip install -r requirements.txt
pip install -e .

cd rafam_extract
pip install -r requirements.txt
pip install -e .
```

### Compilar

Una vez instalados los requisitos, ejecutar desde el directorio `rafam_extract`:

```
python setup.py py2exe
```

Si el procedimiento se completó con éxito, el directorio `dist` contendrá una versión
distribuíble y "compilada" de la aplicación.

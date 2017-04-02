# OpenRAFAM — Manual de uso

El presente documento describe el uso del comando `rafam_extract.py`, que extrae datos de la base de datos de RAFAM en formato JSON o CSV.

## Configuración

Los parámetros de conexión a la base de datos se proveen al sistema con el archivo `PresupuestoAbierto.ini`:

```ini
[Database]
username=nombre_de_usuario
password=clave
host=host.del.oracle
sid=oracle_sid
```

Los valores de los 4 parámetros (`username`, `password`, `host` y `sid`) deben ser reemplazados por los correspondientes para el sistema RAFAM.

La aplicación `rafam_extract` *no realiza modificaciones de los datos almacenados en la BD Oracle*, sino que se limita a hacer consultas de sólo-lectura (`SELECT`). No obstante, es recomendable crear un usuario con privilegios de _lectura_ para usar con esta herramienta.

## Uso

El comando `rafam_extract.py` reconoce los siguientes comandos:

### `datasets`

El comando `datasets` emite una lista de los conjuntos de datos que es posible extraer con la aplicación. La versión actual reconoce los siguientes:

```
> rafam_extract datasets
Datasets disponibles:
  - EstadoEjecucionGastos
    Dataset de estado de ejecucion del presupuesto de gastos
    Parametros: confirmado, date_from, date_to, year

  - EstadoEjecucionRecursos
    Dataset del estado de ejecucion de los recursos
    Parametros: date_from, date_to, year

  - VersionesRafam
    Lista de las versiones de los susbsistemas RAFAM instalados en el servidor
    Parametros:

  - Proveedores
    Listado de Proveedores
    Parametros:

```

### `test`

El comando `test` se usa para verificar los parámetros de conexión que fueron especificados en el archivo de configuración. Si los parámetros de conexión son correctos, debe verse un mensaje similar al siguiente:

```
> rafam_extract test -c PresupuestoAbierto.ini
Subsistemas RAFAM:
  - TES Tesoreria - v007_000_006 (2014-04-09)
  - PRE Presupuesto - v007_000_002 (2013-11-04)
  - TES Tesoreria - v007_000_006 (2014-04-09)
  - BIE Bienes Fisicos - v007_000_005 (2014-07-23)
  - TES Tesoreria - v007_000_006 (2014-04-09)
  - CTR Contrataciones - v007_000_005 (2014-09-19)
  - CTA Contabilidad - v007_002_002 (2015-07-16)
  - PER PER - v007_004_003 (2015-07-16)
  - CAS Configuracion Auditoria y Seguridad - v007_000_001 (2012-12-19)
  - CRE Credito Publico - v007_000_001 (2012-12-19)
  - ING ING - v007_000_001 (2012-12-19)
  - INV Inversion Publica - v007_000_001 (2012-12-19)
  - EST EST - v007_000_002 (2013-11-12)
```

### extract

El comando `extract` ejecuta consultas definidas en los `datasets`. Por ejemplo, el siguiente comando extrae datos de ejecución del presupuesto de gastos desde el 01/01/2015 hasta el 31/03/2015, almacenando los resultados en un archivo formato [`JSONLINES`](http://jsonlines.org/):

```
> rafam_extract extract EstadoEjecucionGastos -p confirmado=S -p date_from=2015-01-01 -p date_to=2015-03-31 -p year=2015 -c PresupuestoAbierto.ini -f JSONLINES -o gastos_1er_trimestre_2015.jsonlines
```

Si el procedimiento se realizó correctamente, deberá haberse creado un archivo llamado `gastos_1er_trimestre_2015.jsonlines` cuyas primeras líneas
serán similares a las siguientes:

```
{"deno_ff": "De origen provincial", "jurisdiccion": "1110107000", "subfuncion": null, "credito_aprobado": 20000, "deno_par_subp": "Presentismo", "par_prin": 2, "deno_jurisdiccion": "Secretaria de Salud", "activ_proy": 14, "deno_funcion": "Salud", "finalidad": 3, "activ_obra": 0, "deno_proyecto": "R.A. (132) Plan Nacer - Sumar", "modificaciones": 0, "deno_par_parc": "Retribuciones que no hacen al cargo", "programa": 1, "anio": 2015, "deno_subfuncion": null, "pagado": 0, "deno_par_prin": "Personal temporario", "compromiso": 0, "deno_finalidad": "Servicios sociales", "inciso": 1, "deno_inciso": "Gastos en personal", "preventivo": 0, "deno_obra": null, "par_parc": 2, "codigo_ff": 132, "devengado": 0, "funcion": 1, "par_subp": 5, "deno_programa": "Actividades Centrales"}
{"deno_ff": "Tesoro Municipal", "jurisdiccion": "1110101000", "subfuncion": null, "credito_aprobado": 77772.96, "deno_par_subp": null, "par_prin": 2, "deno_jurisdiccion": "Intendencia", "activ_proy": 1, "deno_funcion": "Direccion superior ejecutiva", "finalidad": 1, "activ_obra": 0, "deno_proyecto": "Administracion Intendencia", "modificaciones": 0, "deno_par_parc": "Sueldo anual complementario", "programa": 1, "anio": 2015, "deno_subfuncion": null, "pagado": 0, "deno_par_prin": "Personal temporario", "compromiso": 0, "deno_finalidad": "Administracion gubernamental", "inciso": 1, "deno_inciso": "Gastos en personal", "preventivo": 0, "deno_obra": null, "par_parc": 3, "codigo_ff": 110, "devengado": 0, "funcion": 3, "par_subp": 0, "deno_programa": "Actividades Centrales"}
```

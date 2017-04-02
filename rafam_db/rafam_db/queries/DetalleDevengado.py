QUERY = """
SELECT O.EJERCICIO AS Anio,
       O.NRO_OC AS OrdenCompra,
       O.FECH_OC AS Fecha,
       O.IMPORTE_TOT AS Importe ,
       O.FANTASIA AS Proveedor ,
       O.DEP_DESCRIPCION AS Dependencia,
       concat(O.TIPO_DOC_RES_DESC,concat(' ', concat(O.NRO_DOC_RES, concat('/',O.ANIO_DOC_RES)))) AS Expediente,
       O.TIPO_DOC_RES_DESC,
       O.ANIO_DOC_RES,
       O.NRO_DOC_RES ,
       O.DESCRIPCION AS DESCRIP ,
       O.CANTIDAD AS QTY ,
       O.IMP_UNITARIO AS IMPUN,
       O.JURISDICCION AS JUR
FROM OWNER_RAFAM.MBB_ORDENCOMPRA O
WHERE (O.ESTADO_OC = 'R')
  AND (O.EJERCICIO = :year)
GROUP BY O.EJERCICIO,
         O.NRO_OC,
         O.FECH_OC,
         O.IMPORTE_TOT,
         O.FANTASIA,
         O.DEP_DESCRIPCION,
         O.NRO_DOC_RES,
         O.ANIO_DOC_RES,
         O.TIPO_DOC_RES_DESC,
         O.DESCRIPCION,
         O.CANTIDAD,
         O.IMP_UNITARIO,
         O.JURISDICCION
ORDER BY O.EJERCICIO,
         O.NRO_OC
"""

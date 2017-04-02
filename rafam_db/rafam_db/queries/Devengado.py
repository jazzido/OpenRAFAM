QUERY = """SELECT *
FROM
  (SELECT M.JURISDICCION AS JURISDICCION,
          J.DENOMINACION AS DENO_JURISDICCION,
          M.GASTOI AS gasto,
          SUM(M.VIGENTE) AS PRESUPUESTADO_ANUAL,
          SUM(M.DEVENGADO) AS DEVENGADO_A_LA_FECHA,
          count(*) AS QTY
   FROM
     (SELECT MO.EJERCICIO AS EJERCICIO,
             MO.FECH_MOV AS FECH_MOV,
             MO.CODIGO_FF AS CODIGO_FF,
             MO.INCISO AS INCISO,
             MO.PAR_PRIN AS PAR_PRIN,
             MO.PAR_PARC AS PAR_PARC,
             MO.PAR_SUBP AS PAR_SUBP,
             0 AS VIGENTE,
             MO.IMPORTE AS DEVENGADO,
             MO.COD_PROV,
             PR.RAZON_SOCIAL,
             RD.TIPO_DOC AS TIPO_DOC,
             RD.NRO_DOC AS NRO_DOC,
             RD.ANIO_DOC AS ANIO_DOC,
             MO.JURISDICCION AS JURISDICCION,
             ' ' AS CONCEPTO,
             GA.DENOMINACION AS GASTO,
             GI.DENOMINACION_AB AS GASTOI,
             GP.DENOMINACION_AB AS GASTOP
      FROM OWNER_RAFAM.MOV_PRES_DEV MO,
           OWNER_RAFAM.REG_DEVEN RD,
           OWNER_RAFAM.PROVEEDORES PR,
           OWNER_RAFAM.GASTOS GA,
           OWNER_RAFAM.GASTOS GI,
           OWNER_RAFAM.GASTOS GP
      WHERE MO.EJERCICIO=RD.EJERCICIO
        AND MO.NRO_REG_DEVEN=RD.NRO_REG_DEVEN
        AND MO.NRO_REG_DEVEN>0
        AND MO.COD_PROV=PR.COD_PROV
        AND GA.ANIO_PRESUP=MO.EJERCICIO
        AND GA.INCISO=MO.INCISO
        AND GA.PAR_PRIN=MO.PAR_PRIN
        AND GA.PAR_PARC=MO.PAR_PARC
        AND GA.PAR_SUBP=MO.PAR_SUBP
        AND GI.ANIO_PRESUP=MO.EJERCICIO
        AND GI.INCISO=MO.INCISO
        AND GI.PAR_PRIN=0
        AND GI.PAR_PARC=0
        AND GI.PAR_SUBP=0
        AND GP.ANIO_PRESUP=MO.EJERCICIO
        AND GP.INCISO=MO.INCISO
        AND GP.PAR_PRIN=MO.PAR_PRIN
        AND GP.PAR_PARC=0
        AND GP.PAR_SUBP=0
      UNION ALL SELECT MO.EJERCICIO AS EJERCICIO,
                       MO.FECH_MOV AS FECH_MOV,
                       MO.CODIGO_FF AS CODIGO_FF,
                       MO.INCISO AS INCISO,
                       MO.PAR_PRIN AS PAR_PRIN,
                       MO.PAR_PARC AS PAR_PARC,
                       MO.PAR_SUBP AS PAR_SUBP,
                       0 AS VIGENTE,
                       MO.IMPORTE AS DEVENGADO,
                       MO.COD_PROV,
                       PR.RAZON_SOCIAL,
                       OT.TIPO_DOC AS TIPO_DOC,
                       OT.NRO_DOC AS NRO_DOC,
                       OT.ANIO_DOC AS ANIO_DOC,
                       MO.JURISDICCION AS JURISDICCION,
                       ' ' AS CONCEPTO,
                       GA.DENOMINACION AS GASTO,
                       GI.DENOMINACION_AB AS GASTOI,
                       GP.DENOMINACION_AB AS GASTOP
      FROM OWNER_RAFAM.MOV_PRES_DEV MO,
           OWNER_RAFAM.ORDEN_REINT OT,
           OWNER_RAFAM.PROVEEDORES PR,
           OWNER_RAFAM.GASTOS GA,
           OWNER_RAFAM.GASTOS GI,
           OWNER_RAFAM.GASTOS GP
      WHERE MO.EJERCICIO=OT.EJERCICIO
        AND MO.NRO_REINT=OT.NRO_REINT
        AND MO.NRO_REINT>0
        AND MO.COD_PROV=PR.COD_PROV
        AND GA.ANIO_PRESUP=MO.EJERCICIO
        AND GA.INCISO=MO.INCISO
        AND GA.PAR_PRIN=MO.PAR_PRIN
        AND GA.PAR_PARC=MO.PAR_PARC
        AND GA.PAR_SUBP=MO.PAR_SUBP
        AND GI.ANIO_PRESUP=MO.EJERCICIO
        AND GI.INCISO=MO.INCISO
        AND GI.PAR_PRIN=0
        AND GI.PAR_PARC=0
        AND GI.PAR_SUBP=0
        AND GP.ANIO_PRESUP=MO.EJERCICIO
        AND GP.INCISO=MO.INCISO
        AND GP.PAR_PRIN=MO.PAR_PRIN
        AND GP.PAR_PARC=0
        AND GP.PAR_SUBP=0
      UNION ALL SELECT MO.EJERCICIO AS EJERCICIO,
                       MO.FECH_MOV AS FECH_MOV,
                       MO.CODIGO_FF AS CODIGO_FF,
                       MO.INCISO AS INCISO,
                       MO.PAR_PRIN AS PAR_PRIN,
                       MO.PAR_PARC AS PAR_PARC,
                       MO.PAR_SUBP AS PAR_SUBP,
                       0 AS VIGENTE,
                       MO.IMPORTE AS DEVENGADO,
                       MO.COD_PROV,
                       PR.RAZON_SOCIAL,
                       OP.TIPO_DOC AS TIPO_DOC,
                       OP.NRO_DOC AS NRO_DOC,
                       OP.ANIO_DOC AS ANIO_DOC,
                       MO.JURISDICCION AS JURISDICCION,
                       ' ' AS CONCEPTO,
                       GA.DENOMINACION AS GASTO,
                       GI.DENOMINACION_AB AS GASTOI,
                       GP.DENOMINACION_AB AS GASTOP
      FROM OWNER_RAFAM.MOV_PRES_DEV MO,
           OWNER_RAFAM.ORDEN_PAGOEA OP,
           OWNER_RAFAM.PROVEEDORES PR,
           OWNER_RAFAM.GASTOS GA,
           OWNER_RAFAM.GASTOS GI,
           OWNER_RAFAM.GASTOS GP
      WHERE MO.EJERCICIO=OP.EJERCICIO
        AND MO.NRO_OPEA=OP.NRO_OP
        AND MO.NRO_OPEA>0
        AND MO.COD_PROV=PR.COD_PROV
        AND GA.ANIO_PRESUP=MO.EJERCICIO
        AND GA.INCISO=MO.INCISO
        AND GA.PAR_PRIN=MO.PAR_PRIN
        AND GA.PAR_PARC=MO.PAR_PARC
        AND GA.PAR_SUBP=MO.PAR_SUBP
        AND GI.ANIO_PRESUP=MO.EJERCICIO
        AND GI.INCISO=MO.INCISO
        AND GI.PAR_PRIN=0
        AND GI.PAR_PARC=0
        AND GI.PAR_SUBP=0
        AND GP.ANIO_PRESUP=MO.EJERCICIO
        AND GP.INCISO=MO.INCISO
        AND GP.PAR_PRIN=MO.PAR_PRIN
        AND GP.PAR_PARC=0
        AND GP.PAR_SUBP=0
      UNION ALL SELECT MO.EJERCICIO AS EJERCICIO,
                       MO.FECH_MOV AS FECH_MOV,
                       MO.CODIGO_FF AS CODIGO_FF,
                       MO.INCISO AS INCISO,
                       MO.PAR_PRIN AS PAR_PRIN,
                       MO.PAR_PARC AS PAR_PARC,
                       MO.PAR_SUBP AS PAR_SUBP,
                       0 AS VIGENTE,
                       MO.IMPORTE AS DEVENGADO,
                       MO.COD_PROV,
                       PR.RAZON_SOCIAL,
                       RC.TIPO_DOC AS TIPO_DOC,
                       RC.NRO_DOC AS NRO_DOC,
                       RC.ANIO_DOC AS ANIO_DOC,
                       MO.JURISDICCION AS JURISDICCION,
                       ' ' AS CONCEPTO,
                       GA.DENOMINACION AS GASTO,
                       GI.DENOMINACION_AB AS GASTOI,
                       GP.DENOMINACION_AB AS GASTOP
      FROM OWNER_RAFAM.MOV_PRES_DEV MO,
           OWNER_RAFAM.REG_COMP RC,
           OWNER_RAFAM.REGUL_DESAF RD,
           OWNER_RAFAM.PROVEEDORES PR,
           OWNER_RAFAM.GASTOS GA,
           OWNER_RAFAM.GASTOS GI,
           OWNER_RAFAM.GASTOS GP
      WHERE MO.EJERCICIO=RD.EJERCICIO
        AND MO.NRO_REGUL=RD.NRO_REGUL
        AND RD.TIPO_DESA='D'
        AND RD.EJERCICIO=RC.EJERCICIO
        AND RD.NRO_REG_COMP=RC.NRO_REG_COMP
        AND MO.COD_PROV=PR.COD_PROV
        AND GA.ANIO_PRESUP=MO.EJERCICIO
        AND GA.INCISO=MO.INCISO
        AND GA.PAR_PRIN=MO.PAR_PRIN
        AND GA.PAR_PARC=MO.PAR_PARC
        AND GA.PAR_SUBP=MO.PAR_SUBP
        AND GI.ANIO_PRESUP=MO.EJERCICIO
        AND GI.INCISO=MO.INCISO
        AND GI.PAR_PRIN=0
        AND GI.PAR_PARC=0
        AND GI.PAR_SUBP=0
        AND GP.ANIO_PRESUP=MO.EJERCICIO
        AND GP.INCISO=MO.INCISO
        AND GP.PAR_PRIN=MO.PAR_PRIN
        AND GP.PAR_PARC=0
        AND GP.PAR_SUBP=0
      UNION ALL SELECT MO.EJERCICIO AS EJERCICIO,
                       MO.FECH_MOV AS FECH_MOV,
                       MO.CODIGO_FF AS CODIGO_FF,
                       MO.INCISO AS INCISO,
                       MO.PAR_PRIN AS PAR_PRIN,
                       MO.PAR_PARC AS PAR_PARC,
                       MO.PAR_SUBP AS PAR_SUBP,
                       0 AS VIGENTE,
                       MO.IMPORTE AS DEVENGADO,
                       MO.COD_PROV,
                       PR.RAZON_SOCIAL,
                       RC.TIPO_DOC AS TIPO_DOC,
                       RC.NRO_DOC AS NRO_DOC,
                       RC.ANIO_DOC AS ANIO_DOC,
                       MO.JURISDICCION AS JURISDICCION,
                       ' ' AS CONCEPTO,
                       GA.DENOMINACION AS GASTO,
                       GI.DENOMINACION_AB AS GASTOI,
                       GP.DENOMINACION_AB AS GASTOP
      FROM OWNER_RAFAM.MOV_PRES_DEV MO,
           OWNER_RAFAM.REGUL_CORREC RC,
           OWNER_RAFAM.PROVEEDORES PR,
           OWNER_RAFAM.GASTOS GA,
           OWNER_RAFAM.GASTOS GI,
           OWNER_RAFAM.GASTOS GP
      WHERE MO.EJERCICIO=RC.EJERCICIO
        AND MO.NRO_REGUL=RC.NRO_REGUL
        AND MO.NRO_REGUL>0
        AND MO.COD_PROV=PR.COD_PROV
        AND GA.ANIO_PRESUP=MO.EJERCICIO
        AND GA.INCISO=MO.INCISO
        AND GA.PAR_PRIN=MO.PAR_PRIN
        AND GA.PAR_PARC=MO.PAR_PARC
        AND GA.PAR_SUBP=MO.PAR_SUBP
        AND GI.ANIO_PRESUP=MO.EJERCICIO
        AND GI.INCISO=MO.INCISO
        AND GI.PAR_PRIN=0
        AND GI.PAR_PARC=0
        AND GI.PAR_SUBP=0
        AND GP.ANIO_PRESUP=MO.EJERCICIO
        AND GP.INCISO=MO.INCISO
        AND GP.PAR_PRIN=MO.PAR_PRIN
        AND GP.PAR_PARC=0
        AND GP.PAR_SUBP=0
      UNION ALL SELECT MO.EJERCICIO AS EJERCICIO,
                       MO.FECH_MOV AS FECH_MOV,
                       MO.CODIGO_FF AS CODIGO_FF,
                       MO.INCISO AS INCISO,
                       MO.PAR_PRIN AS PAR_PRIN,
                       MO.PAR_PARC AS PAR_PARC,
                       MO.PAR_SUBP AS PAR_SUBP,
                       0 AS VIGENTE,
                       MO.IMPORTE AS DEVENGADO,
                       MO.COD_PROV,
                       PR.RAZON_SOCIAL,
                       RG.TIPO_DOC AS TIPO_DOC,
                       RG.NRO_DOC AS NRO_DOC,
                       RG.ANIO_DOC AS ANIO_DOC,
                       MO.JURISDICCION AS JURISDICCION,
                       ' ' AS CONCEPTO,
                       GA.DENOMINACION AS GASTO,
                       GI.DENOMINACION_AB AS GASTOI,
                       GP.DENOMINACION_AB AS GASTOP
      FROM OWNER_RAFAM.MOV_PRES_DEV MO,
           OWNER_RAFAM.REGUL_GASTOS RG,
           OWNER_RAFAM.PROVEEDORES PR,
           OWNER_RAFAM.GASTOS GA,
           OWNER_RAFAM.GASTOS GI,
           OWNER_RAFAM.GASTOS GP
      WHERE MO.EJERCICIO=RG.EJERCICIO
        AND MO.NRO_REGUL=RG.NRO_REGUL
        AND MO.NRO_REGUL>0
        AND MO.COD_PROV=PR.COD_PROV
        AND GA.ANIO_PRESUP=MO.EJERCICIO
        AND GA.INCISO=MO.INCISO
        AND GA.PAR_PRIN=MO.PAR_PRIN
        AND GA.PAR_PARC=MO.PAR_PARC
        AND GA.PAR_SUBP=MO.PAR_SUBP
        AND GI.ANIO_PRESUP=MO.EJERCICIO
        AND GI.INCISO=MO.INCISO
        AND GI.PAR_PRIN=0
        AND GI.PAR_PARC=0
        AND GI.PAR_SUBP=0
        AND GP.ANIO_PRESUP=MO.EJERCICIO
        AND GP.INCISO=MO.INCISO
        AND GP.PAR_PRIN=MO.PAR_PRIN
        AND GP.PAR_PARC=0
        AND GP.PAR_SUBP=0
      UNION ALL SELECT MO.ANIO_PRESUP AS EJERCICIO,
                       CAST('01/01/1900' AS DATE) AS FECH_MOV,
                       MO.CODIGO_FF AS CODIGO_FF,
                       MO.INCISO AS INCISO,
                       MO.PAR_PRIN AS PAR_PRIN,
                       MO.PAR_PARC AS PAR_PARC,
                       MO.PAR_SUBP AS PAR_SUBP,
                       IMPORTE AS VIGENTE,
                       0 AS DEVENGADO,
                       0 AS COD_PROV,
                       ' ' AS RAZON_SOCIAL,
                       ' ' AS TIPO_DOC,
                       0 AS NRO_DOC,
                       MO.ANIO_PRESUP AS ANIO_DOC,
                       MO.JURISDICCION AS JURISDICCION,
                       ' ' AS CONCEPTO,
                       GA.DENOMINACION AS GASTO,
                       GI.DENOMINACION_AB AS GASTOI,
                       GP.DENOMINACION_AB AS GASTOP
      FROM OWNER_RAFAM.VIS_FORMULARIOS MO,
           OWNER_RAFAM.GASTOS GA,
           OWNER_RAFAM.GASTOS GI,
           OWNER_RAFAM.GASTOS GP
      WHERE GA.ANIO_PRESUP=MO.ANIO_PRESUP
        AND GA.INCISO=MO.INCISO
        AND GA.PAR_PRIN=MO.PAR_PRIN
        AND GA.PAR_PARC=MO.PAR_PARC
        AND GA.PAR_SUBP=MO.PAR_SUBP
        AND GI.ANIO_PRESUP=MO.ANIO_PRESUP
        AND GI.INCISO=MO.INCISO
        AND GI.PAR_PRIN=0
        AND GI.PAR_PARC=0
        AND GI.PAR_SUBP=0
        AND GP.ANIO_PRESUP=MO.ANIO_PRESUP
        AND GP.INCISO=MO.INCISO
        AND GP.PAR_PRIN=MO.PAR_PRIN
        AND GP.PAR_PARC=0
        AND GP.PAR_SUBP=0
      UNION ALL SELECT MO.ANIO_PRESUP AS EJERCICIO,
                       MO.FECH_MOV AS FECH_MOV,
                       MO.CODIGO_FF AS CODIGO_FF,
                       MO.INCISO AS INCISO,
                       MO.PAR_PRIN AS PAR_PRIN,
                       MO.PAR_PARC AS PAR_PARC,
                       MO.PAR_SUBP AS PAR_SUBP,
                       IMPORTE_MODIF AS VIGENTE,
                       0 AS DEVENGADO,
                       0 AS COD_PROV,
                       ' ' AS RAZON_SOCIAL,
                       ' ' AS TIPO_DOC,
                       0 AS NRO_DOC,
                       MO.ANIO_PRESUP AS ANIO_DOC,
                       MO.JURISDICCION AS JURISDICCION,
                       ' ' AS CONCEPTO,
                       GA.DENOMINACION AS GASTO,
                       GI.DENOMINACION_AB AS GASTOI,
                       GP.DENOMINACION_AB AS GASTOP
      FROM OWNER_RAFAM.PRESUP_MODIF MO,
           OWNER_RAFAM.GASTOS GA,
           OWNER_RAFAM.GASTOS GI,
           OWNER_RAFAM.GASTOS GP
      WHERE GA.ANIO_PRESUP=MO.ANIO_PRESUP
        AND GA.INCISO=MO.INCISO
        AND GA.PAR_PRIN=MO.PAR_PRIN
        AND GA.PAR_PARC=MO.PAR_PARC
        AND GA.PAR_SUBP=MO.PAR_SUBP
        AND GI.ANIO_PRESUP=MO.ANIO_PRESUP
        AND GI.INCISO=MO.INCISO
        AND GI.PAR_PRIN=0
        AND GI.PAR_PARC=0
        AND GI.PAR_SUBP=0
        AND GP.ANIO_PRESUP=MO.ANIO_PRESUP
        AND GP.INCISO=MO.INCISO
        AND GP.PAR_PRIN=MO.PAR_PRIN
        AND GP.PAR_PARC=0
        AND GP.PAR_SUBP=0) M,
                           OWNER_RAFAM.JURISDICCIONES J
   WHERE M.DEVENGADO<>0
     AND M.ejercicio=:year
     AND M.JURISDICCION=J.JURISDICCION
   GROUP BY M.JURISDICCION,
            J.DENOMINACION,
            M.GASTOI
   ORDER BY J.DENOMINACION)
ORDER BY DEVENGADO_A_LA_FECHA DESC
"""

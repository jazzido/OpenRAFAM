QUERY = """SELECT DENOMINACION,
       SUM(IMPOR_ESTI+IMPOR_MODI) AS CALCULADO_ANUAL,
       SUM(IMPOR_PERCI) AS PERCIBIDO_A_LA_FECHA
FROM
  (SELECT ALL MO.ANIO_PRESUP AS ANIO_PRESUP,
              MO.TIPO AS TIPO,
              MO.CLASE AS CLASE,
              MO.CONCEPTO AS CONCEPTO,
              MO.SUBCONCEPTO AS SUBCONCEPTO,
              MO.PROGRAMADO AS IMPOR_ESTI,
              0 AS IMPOR_MODI,
              0 AS IMPOR_DEVEN,
              0 AS IMPOR_PERCI,
              RE.DENOMINACION AS DENOMINACION,
              ORI.CODIGO AS CODIGO
   FROM
     (SELECT anio_presup,
             jurisdiccion,
             tipo,
             clase,
             concepto,
             subconcepto,
             programado,
             proy1,
             proy2,
             exenciones,
             otras
      FROM OWNER_RAFAM.formulario2
      UNION ALL SELECT anio_presup,
                       jurisdiccion,
                       tipo,
                       clase,
                       concepto,
                       subconcepto,
                       importe_ff AS programado,
                       proy1,
                       proy2,
                       0 AS exenciones,
                       0 AS otras
      FROM OWNER_RAFAM.formulario10a) MO,
                                      OWNER_RAFAM.VI_RUB_ORI ORI,
                                      OWNER_RAFAM.RECURSOS RE
   WHERE MO.ANIO_PRESUP=ORI.ANIO_PRESUP
     AND MO.TIPO=ORI.TIPO
     AND MO.CLASE=ORI.CLASE
     AND MO.concepto=ORI.CONCEPTO
     AND MO.subconcepto=ORI.SUBCONCEPTO
     AND MO.ANIO_PRESUP=RE.anio_presup
     AND MO.TIPO=RE.TIPO
     AND MO.CLASE=RE.clase
     AND MO.CONCEPTO=RE.CONCEPTO
     AND MO.subconcepto=RE.subconcepto
   UNION ALL SELECT MO.ANIO_PRESUP AS ANIO_PRESUP,
                    MO.TIPO AS TIPO,
                    MO.CLASE AS CLASE,
                    MO.CONCEPTO AS CONCEPTO,
                    MO.SUBCONCEPTO AS SUBCONCEPTO,
                    0 AS IMPOR_ESTI,
                    IMPORTE_MODIF AS IMPOR_MODI,
                    0 AS IMPOR_DEVEN,
                    0 AS IMPOR_PERCI,
                    RE.DENOMINACION AS DENOMINACION,
                    ORI.CODIGO AS CODIGO
   FROM OWNER_RAFAM.CALCULO_MODIF MO,
        OWNER_RAFAM.VI_RUB_ORI ORI,
        OWNER_RAFAM.RECURSOS RE
   WHERE MO.ANIO_PRESUP=ORI.ANIO_PRESUP
     AND MO.TIPO=ORI.TIPO
     AND MO.CLASE=ORI.CLASE
     AND MO.concepto=ORI.CONCEPTO
     AND MO.subconcepto=ORI.SUBCONCEPTO
     AND MO.ANIO_PRESUP=RE.anio_presup
     AND MO.TIPO=RE.TIPO
     AND MO.CLASE=RE.clase
     AND MO.CONCEPTO=RE.CONCEPTO
     AND RE.subconcepto=MO.SUBCONCEPTO
   UNION ALL SELECT MO.EJERCICIO AS ANIO_PRESUP,
                    MO.TIPO AS TIPO,
                    MO.CLASE AS CLASE,
                    MO.CONCEPTO AS CONCEPTO,
                    MO.SUBCONCEPTO AS SUBCONCEPTO,
                    0 AS IMPOR_ESTI,
                    0 AS IMPOR_MODI,
                    IMPORTE AS IMPOR_DEVEN,
                    0 AS IMPOR_PERCI,
                    RE.DENOMINACION AS DENOMINACION,
                    ORI.CODIGO AS CODIGO
   FROM OWNER_RAFAM.MOV_PRES_REC_DEV MO,
        OWNER_RAFAM.VI_RUB_ORI ORI,
        OWNER_RAFAM.RECURSOS RE
   WHERE MO.EJERCICIO=ORI.ANIO_PRESUP
     AND MO.TIPO=ORI.TIPO
     AND MO.CLASE=ORI.CLASE
     AND MO.concepto=ORI.CONCEPTO
     AND MO.subconcepto=ORI.SUBCONCEPTO
     AND MO.EJERCICIO=RE.anio_presup
     AND MO.TIPO=RE.TIPO
     AND MO.CLASE=RE.clase
     AND MO.CONCEPTO=RE.CONCEPTO
     AND RE.subconcepto=MO.subconcepto
   UNION ALL SELECT MO.EJERCICIO AS ANIO_PRESUP,
                    MO.TIPO AS TIPO,
                    MO.CLASE AS CLASE,
                    MO.CONCEPTO AS CONCEPTO,
                    MO.SUBCONCEPTO AS SUBCONCEPTO,
                    0 AS IMPOR_ESTI,
                    0 AS IMPOR_MODI,
                    0 AS IMPOR_DEVEN,
                    IMPORTE AS IMPOR_PERCI,
                    RE.DENOMINACION AS DENOMINACION,
                    ORI.CODIGO AS CODIGO
   FROM OWNER_RAFAM.MOV_PRES_REC_PER MO,
        OWNER_RAFAM.VI_RUB_ORI ORI,
        OWNER_RAFAM.RECURSOS RE
   WHERE MO.EJERCICIO=ORI.ANIO_PRESUP
     AND MO.TIPO=ORI.TIPO
     AND MO.CLASE=ORI.CLASE
     AND MO.concepto=ORI.CONCEPTO
     AND MO.subconcepto=ORI.SUBCONCEPTO
     AND MO.EJERCICIO=RE.anio_presup
     AND MO.TIPO=RE.TIPO
     AND MO.CLASE=RE.clase
     AND MO.CONCEPTO=RE.CONCEPTO
     AND RE.subconcepto=MO.subconcepto )
WHERE ANIO_PRESUP=:year
GROUP BY DENOMINACION
ORDER BY DENOMINACION

"""

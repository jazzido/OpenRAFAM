# inspirado en CTA_EJECUCIONRECURSOSPRESUP
QUERY = """
SELECT r.anio                        AS anio,
       r.jurisdiccion                AS jurisdiccion,
       j.denominacion                AS deno_jurisdiccion,
       vro.codigo                    AS codi_proce,
       ro.denominacion               AS deno_proce,
       vrc.codigo                    AS codi_carac,
       re.denominacion               AS deno_carac,
       r.tipo                        AS tipo,
       rec_tipo.denominacion         AS deno_tipo,
       r.clase                       AS clase,
       rec_clase.denominacion        AS deno_clase,
       r.concepto                    AS concepto,
       rec_concepto.denominacion     AS deno_concepto,
       r.subconcepto                 AS subconcepto,
       rec_subconcepto.denominacion  as deno_subconcepto,
       SUM(impor_esti)               AS impor_esti,
       SUM(impor_modi)               AS impor_modif,
       SUM(impor_deven)              AS impor_deven,
       SUM(impor_perci)              AS impor_preci
FROM
  (SELECT vis.anio_presup AS anio,
          vis.jurisdiccion,
          vis.tipo,
          vis.clase,
          vis.concepto,
          vis.subconcepto,
          vis.programado AS impor_esti,
          0 AS impor_modi,
          0 AS impor_deven,
          0 AS impor_perci
   FROM owner_rafam.vis_movimientos_recursos vis
   WHERE vis.anio_presup = :year

   UNION

   SELECT cm.anio_presup AS anio,
                cm.jurisdiccion,
                cm.tipo,
                cm.clase,
                cm.concepto,
                cm.subconcepto,
                0 AS impor_esti,
                cm.importe_modif AS impor_modi,
                0 AS impor_deven,
                0 AS impor_perci
   FROM owner_rafam.calculo_modif cm
   WHERE cm.anio_presup = :year
     AND trunc(cm.fech_mov) >= to_date(:date_from, 'YYYY-MM-DD')
     AND trunc(cm.fech_mov) <= to_date(:date_to, 'YYYY-MM-DD')

   UNION

   SELECT mprd.ejercicio AS anio,
                mprd.jurisdiccion,
                mprd.tipo,
                mprd.clase,
                mprd.concepto,
                mprd.subconcepto,
                0 AS impor_esti,
                0 AS impor_modi,
                mprd.importe AS impor_deven,
                0 AS impor_perci
   FROM owner_rafam.MOV_PRES_REC_DEV mprd
   WHERE mprd.ejercicio = :year
     AND trunc(mprd.fech_mov) >= to_date(:date_from, 'YYYY-MM-DD')
     AND trunc(mprd.fech_mov) <= to_date(:date_to, 'YYYY-MM-DD')

   UNION SELECT mprp.ejercicio AS anio,
                mprp.jurisdiccion,
                mprp.tipo,
                mprp.clase,
                mprp.concepto,
                mprp.subconcepto,
                0 AS impor_esti,
                0 AS impor_modi,
                0 AS impor_deven,
                mprp.importe AS impor_perci
   FROM owner_rafam.MOV_PRES_REC_PER mprp
   WHERE mprp.ejercicio = :year
     AND trunc(mprp.fech_mov) >= to_date(:date_from, 'YYYY-MM-DD')
     AND trunc(mprp.fech_mov) <= to_date(:date_to, 'YYYY-MM-DD')
   ) r

JOIN OWNER_RAFAM.JURISDICCIONES j
ON r.jurisdiccion = j.jurisdiccion

JOIN OWNER_RAFAM.RECURSOS rec_tipo
   ON rec_tipo.anio_presup = r.anio
  AND rec_tipo.tipo = r.tipo
  AND rec_tipo.clase = 0
  AND rec_tipo.concepto = 0
  AND rec_tipo.subconcepto = 0

LEFT OUTER JOIN OWNER_RAFAM.RECURSOS rec_clase
 ON rec_clase.anio_presup = r.anio
AND rec_clase.tipo = r.tipo
AND rec_clase.clase = r.clase
AND rec_clase.clase <> 0
AND rec_clase.concepto = 0
AND rec_clase.subconcepto = 0

LEFT OUTER JOIN OWNER_RAFAM.RECURSOS rec_concepto
 ON rec_concepto.anio_presup = r.anio
AND rec_concepto.tipo = r.tipo
AND rec_concepto.clase = r.clase
AND rec_concepto.concepto = r.concepto
AND rec_concepto.concepto <> 0
AND rec_concepto.subconcepto = 0

LEFT OUTER JOIN OWNER_RAFAM.RECURSOS rec_subconcepto
 ON rec_subconcepto.anio_presup = r.anio
AND rec_subconcepto.tipo = r.tipo
AND rec_subconcepto.clase = r.clase
AND rec_subconcepto.concepto = r.concepto
AND rec_subconcepto.subconcepto = r.subconcepto
AND rec_subconcepto.subconcepto <> 0

-- obtener origen (procedencia) segun rubro
JOIN OWNER_RAFAM.VI_RUB_ORI vro
ON vro.anio_presup = r.anio
AND vro.tipo = r.tipo
AND vro.clase = r.clase
AND vro.concepto = r.concepto
AND vro.subconcepto = r.subconcepto

-- obtener denominacion origen (procedencia)
JOIN OWNER_RAFAM.REC_ORIG ro
ON ro.codigo = SUBSTR(vro.codigo, 1, 1)||'0'

-- obtener caracter economico segun rubro
JOIN OWNER_RAFAM.VI_RUB_CAR vrc
ON vrc.anio_presup = r.anio
AND vrc.tipo = r.tipo
AND vrc.clase = r.clase
AND vrc.concepto = r.concepto
AND vrc.subconcepto = r.subconcepto

-- obtener denominacion por caracter economico
JOIN OWNER_RAFAM.RE_CA_EC re
ON re.codigo = vrc.codigo

GROUP BY r.anio,
         r.jurisdiccion,
         j.denominacion,
         vro.codigo,
         ro.denominacion,
         vrc.codigo,
         re.denominacion,
         r.tipo,
         rec_tipo.denominacion,
         r.clase,
         rec_clase.denominacion,
         r.concepto,
         rec_concepto.denominacion,
         r.subconcepto,
         rec_subconcepto.denominacion"""

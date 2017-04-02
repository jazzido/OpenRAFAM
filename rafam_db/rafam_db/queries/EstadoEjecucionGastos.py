# inspirado en CTA_ESTADOEJECUCIONPRESUPGASTO
QUERY = """
SELECT g.anio                   AS anio,
  g.jurisdiccion                AS jurisdiccion,
  j.denominacion                AS deno_jurisdiccion,
  g.programa                    AS programa,
  ep_programa.denominacion      AS deno_programa,
  g.activ_proy                  AS activ_proy,
  ep_proyecto.denominacion      AS deno_proyecto,
  g.activ_obra                  AS activ_obra,
  ep_obra.denominacion          AS deno_obra,
  g.codigo_ff                   AS codigo_ff,
  ff.denominacion               AS deno_ff,
  g.inciso                      AS inciso,
  g_inciso.denominacion         AS deno_inciso,
  g.par_prin                    AS par_prin,
  g_par_prin.denominacion       AS deno_par_prin,
  g.par_parc                    AS par_parc,
  g_par_parc.denominacion       AS deno_par_parc,
  g.par_subp                    AS par_subp,
  g_par_subp.denominacion       AS deno_par_subp,
  ff_finalidad.finalidad        AS finalidad,
  ff_finalidad.denominacion     AS deno_finalidad,
  ff_funcion.funcion            AS funcion,
  ff_funcion.denominacion       AS deno_funcion,
  ff_subfuncion.subfuncion      AS subfuncion,
  ff_subfuncion.denominacion    AS deno_subfuncion,
  SUM(g.credito_aprobado)       AS credito_aprobado,
  SUM(g.modificaciones)         AS modificaciones,
  SUM(g.devengado)              AS devengado,
  SUM(g.pagado)                 AS pagado,
  SUM(g.preventivo)             AS preventivo,
  SUM(g.compromiso)             AS compromiso
FROM
  (
  /* Credito */
  SELECT anio_presup AS anio,
    jurisdiccion,
    programa,
    activ_proy,
    activ_obra,
    codigo_ff,
    inciso,
    par_prin,
    par_parc,
    par_subp,
    importe AS credito_aprobado,
    0       AS pagado,
    0       AS preventivo_difer,
    0       AS modificaciones,
    0       AS preventivo,
    0       AS compromiso,
    0       AS devengado,
    0       AS compromiso_difer,
    'CRED'  AS reg_id
  FROM OWNER_RAFAM.VIS_FORMULARIOS vis
  WHERE vis.anio_presup = :year

  UNION ALL

  /*Modificaciones*/
  SELECT anio_presup AS anio,
    jurisdiccion,
    programa,
    activ_proy,
    activ_obra,
    codigo_ff,
    inciso,
    par_prin,
    par_parc,
    par_subp,
    0             AS credito_aprobado,
    0             AS pagado,
    0             AS preventivo_difer,
    importe_modif AS modificaciones,
    0             AS preventivo,
    0             AS compromiso,
    0             AS devengado,
    0             AS compromiso_difer,
    'MODI'        AS reg_id
  FROM OWNER_RAFAM.PRESUP_MODIF pm
  WHERE pm.anio_presup = :year
  AND (TRUNC(pm.fech_mov) >= to_date(:date_from, 'YYYY-MM-DD')
       AND TRUNC(pm.fech_mov)  <= to_date(:date_to, 'YYYY-MM-DD'))

  UNION ALL

  /*Preventivo*/
  SELECT ejercicio AS anio,
    jurisdiccion,
    programa,
    activ_proy,
    activ_obra,
    codigo_ff,
    inciso,
    par_prin,
    par_parc,
    par_subp,
    0                AS credito_aprobado,
    0                AS pagado,
    mpp.importe_ejer AS preventivo_difer,
    0                AS modificaciones,
    importe          AS preventivo,
    0                AS compromiso,
    0                AS devengado,
    0                AS compromiso_difer,
    'PREV'           AS reg_id
  FROM OWNER_RAFAM.MOV_PRES_PREV mpp
  WHERE mpp.ejercicio                                                                                                                                = :year
  AND OWNER_RAFAM.CTA_MOVIMIENTOCONFIRMADOPRES ( 'R', :year, NVL(mpp.deleg_solic,0), NVL(mpp.nro_solic,0), NVL(mpp.nro_regul,0), 0, mpp.fech_hora ) IN ('S', :confirmado)
  AND (TRUNC(mpp.fech_mov) >= to_date(:date_from, 'YYYY-MM-DD')
       AND TRUNC(mpp.fech_mov)  <= to_date(:date_to, 'YYYY-MM-DD'))
  AND (deleg_solic                                                                                                                                   > 0
  OR nro_solic                                                                                                                                       > 0
  OR nro_regul                                                                                                                                       > 0)
  UNION ALL

  /*Compromiso*/
  SELECT ejercicio AS anio,
    jurisdiccion,
    programa,
    activ_proy,
    activ_obra,
    codigo_ff,
    inciso,
    par_prin,
    par_parc,
    par_subp,
    0             AS credito_aprobado,
    0             AS pagado,
    0             AS preventivo_difer,
    0             AS modificaciones,
    0             AS preventivo,
    importe       AS compromiso,
    0             AS devengado,
    importe_difer AS compromiso_difer,
    'COMP'        AS reg_id
  FROM OWNER_RAFAM.MOV_PRES_COMP mpc
  WHERE mpc.ejercicio                                                                                                                                            = :year
  AND OWNER_RAFAM.CTA_MovimientoConfirmadoPres ( 'C', mpc.ejercicio, NVL(mpc.nro_reg_comp,0), NVL(mpc.nro_reint,0), NVL(mpc.nro_regul,0), NVL(mpc.nro_opea,0) ) IN ('S', :confirmado)
  AND (TRUNC(mpc.fech_mov) >= to_date(:date_from, 'YYYY-MM-DD') AND TRUNC(mpc.fech_mov)  <= to_date(:date_to, 'YYYY-MM-DD'))
  AND (nro_reg_comp                                                                                                                                              > 0
  OR nro_reint                                                                                                                                                   > 0
  OR nro_regul                                                                                                                                                   > 0
  OR nro_opea                                                                                                                                                    > 0)

  UNION ALL

  /*Devengado*/
  SELECT ejercicio AS anio,
    jurisdiccion,
    programa,
    activ_proy,
    activ_obra,
    codigo_ff,
    inciso,
    par_prin,
    par_parc,
    par_subp,
    NULL    AS credito_aprobado,
    NULL    AS pagado,
    NULL    AS preventivo_difer,
    NULL    AS modificaciones,
    NULL    AS preventivo,
    NULL    AS compromiso,
    importe AS devengado,
    NULL    AS compromiso_difer,
    'DEVE'  AS reg_id
  FROM OWNER_RAFAM.MOV_PRES_DEV mpd
  WHERE mpd.ejercicio                                                                                                                                             = :year
  AND OWNER_RAFAM.CTA_MovimientoConfirmadoPres ( 'D', mpd.ejercicio, NVL(mpd.nro_reg_deven,0), NVL(mpd.nro_reint,0), NVL(mpd.nro_regul,0), NVL(mpd.nro_opea,0) ) IN ('S', :confirmado)
  AND (TRUNC(mpd.fech_mov) >= to_date(:date_from, 'YYYY-MM-DD') AND TRUNC(mpd.fech_mov)  <= to_date(:date_to, 'YYYY-MM-DD'))
  AND (nro_reg_deven                                                                                                                                              > 0
  OR nro_reint                                                                                                                                                    > 0
  OR nro_regul                                                                                                                                                    > 0
  OR nro_opea                                                                                                                                                     > 0)
  UNION ALL

  /*pagado*/
  SELECT ejercicio AS anio,
    jurisdiccion,
    programa,
    activ_proy,
    activ_obra,
    codigo_ff,
    inciso,
    par_prin,
    par_parc,
    par_subp,
    NULL    AS credito_aprobado,
    importe AS pagado,
    NULL    AS preventivo_difer,
    NULL    AS modificaciones,
    NULL    AS preventivo,
    NULL    AS compromiso,
    NULL    AS devengado,
    NULL    AS compromiso_difer,
    'PAGA'  AS reg_id
  FROM OWNER_RAFAM.MOV_PRES_PAG mpp
  WHERE mpp.ejercicio                                                                                                                             = :year
  AND OWNER_RAFAM.CTA_MovimientoConfirmadoPres ('P', :year, NVL(mpp.nro_op,0), NVL(mpp.nro_reint,0), NVL(mpp.nro_regul,0), NVL(mpp.nro_opea,0) ) IN ('S', :confirmado)
  AND (TRUNC(mpp.fech_mov) >= to_date(:date_from, 'YYYY-MM-DD') AND TRUNC(mpp.fech_mov) <= to_date(:date_to, 'YYYY-MM-DD'))
  AND (nro_op                                                                                                                                     > 0
  OR nro_reint                                                                                                                                    > 0
  OR nro_regul                                                                                                                                    > 0
  OR nro_opea                                                                                                                                     > 0)
  ) g

/* denominacion jurisdicciones */
JOIN OWNER_RAFAM.JURISDICCIONES j
ON g.jurisdiccion = j.jurisdiccion

/* denominacion programa */
JOIN OWNER_RAFAM.ESTRUC_PROG ep_programa
ON ep_programa.anio_presup   = g.anio
AND ep_programa.jurisdiccion = g.jurisdiccion
AND ep_programa.programa     = g.programa
AND ep_programa.activ_proy   = 0
AND ep_programa.activ_obra   = 0

/* denominacion proyecto */
LEFT OUTER JOIN OWNER_RAFAM.ESTRUC_PROG ep_proyecto
ON ep_proyecto.anio_presup   = g.anio
AND ep_proyecto.jurisdiccion = g.jurisdiccion
AND ep_proyecto.programa     = g.programa
AND ep_proyecto.activ_proy   = g.activ_proy
AND ep_proyecto.activ_proy  <> 0
AND ep_proyecto.activ_obra   = 0

/* denominacion obra */
LEFT OUTER JOIN OWNER_RAFAM.ESTRUC_PROG ep_obra
ON ep_obra.anio_presup   = g.anio
AND ep_obra.jurisdiccion = g.jurisdiccion
AND ep_obra.programa     = g.programa
AND ep_obra.activ_proy   = g.activ_proy
AND ep_obra.activ_obra   = g.activ_obra
AND ep_obra.activ_obra  <> 0

/* denominacion fuente financiamiento */
JOIN OWNER_RAFAM.FUEN_FIN ff
ON ff.anio_presup = g.anio
AND ff.codigo_ff  = g.codigo_ff

  /* denominacion inciso */
JOIN OWNER_RAFAM.gastos g_inciso
ON g_inciso.anio_presup = g.anio
AND g_inciso.inciso     = g.inciso
AND g_inciso.par_prin   = 0
AND g_inciso.par_parc   = 0
AND g_inciso.par_subp   = 0

  /* denominacion partida principal */
LEFT OUTER JOIN OWNER_RAFAM.gastos g_par_prin
ON g_par_prin.anio_presup = g.anio
AND g_par_prin.inciso     = g.inciso
AND g_par_prin.par_prin   = g.par_prin
AND g_par_prin.par_parc   = 0
AND g_par_prin.par_subp   = 0

  /* denominacion partida parcial */
LEFT OUTER JOIN OWNER_RAFAM.gastos g_par_parc
ON g_par_parc.anio_presup = g.anio
AND g_par_parc.inciso     = g.inciso
AND g_par_parc.par_prin   = g.par_prin
AND g_par_parc.par_parc   = g.par_parc
AND g_par_parc.par_subp   = 0
AND g_par_parc.par_parc  <> 0

  /* denominacion partida subparcial */
LEFT OUTER JOIN OWNER_RAFAM.gastos g_par_subp
ON g_par_subp.anio_presup = g.anio
AND g_par_subp.inciso     = g.inciso
AND g_par_subp.par_prin   = g.par_prin
AND g_par_subp.par_parc   = g.par_parc
AND g_par_subp.par_subp   = g.par_subp
AND g_par_subp.par_subp  <> 0

/* finalidad y funcion */

JOIN OWNER_RAFAM.ESTRUC_PROG e
 ON e.jurisdiccion  = g.jurisdiccion
AND e.anio_presup   = g.anio
AND e.programa      = g.programa
AND e.activ_proy    = g.activ_proy
AND e.activ_obra    = g.activ_obra

JOIN OWNER_RAFAM.FIN_FUN ff_finalidad
ON ff_finalidad.finalidad   = e.finalidad
AND ff_finalidad.funcion    = 0
AND ff_finalidad.subfuncion = 0

LEFT OUTER JOIN OWNER_RAFAM.FIN_FUN ff_funcion
 ON ff_funcion.finalidad  =  e.finalidad
AND ff_funcion.funcion    =  e.funcion
AND ff_funcion.funcion    <> 0
AND ff_funcion.subfuncion =  0

LEFT OUTER JOIN OWNER_RAFAM.FIN_FUN ff_subfuncion
 ON ff_subfuncion.finalidad  = e.finalidad
AND ff_subfuncion.funcion    = e.funcion
AND ff_subfuncion.subfuncion = e.subfuncion
AND ff_subfuncion.subfuncion <> 0


GROUP BY g.anio,
  g.jurisdiccion,
  j.denominacion,
  g.programa,
  ep_programa.denominacion,
  g.activ_proy,
  ep_proyecto.denominacion,
  g.activ_obra,
  ep_obra.denominacion,
  g.codigo_ff,
  ff.denominacion,
  g.inciso,
  g_inciso.denominacion,
  g.par_prin,
  g_par_prin.denominacion,
  g.par_parc,
  g_par_parc.denominacion,
  g.par_subp,
  g_par_subp.denominacion,
  ff_finalidad.finalidad,
  ff_finalidad.denominacion,
  ff_funcion.funcion,
  ff_funcion.denominacion,
  ff_subfuncion.subfuncion,
  ff_subfuncion.denominacion

"""

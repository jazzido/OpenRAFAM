QUERY = """SELECT O.EJERCICIO AS Anio,
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
FROM (
SELECT o.ejercicio,
       o.uni_compra,
       o.nro_oc,
       o.nro_adjud,
       o.fech_oc,
       o.lug_emi,
       o.cod_prov,
       decode(ent.cod_lug_ent ,NULL,o.cod_lug_ent,ent.cod_lug_ent) cod_lug_ent,
       o.fech_entrega,
       o.estado_oc,
       o.tipo_doc_aprob,
       o.nro_doc_aprob,
       o.anio_doc_aprob,
       o.confirmado ,
       o.fech_confirm,
       o.cant_impres,
       o.fech_anul,
       o.motivo_anul,
       o.observaciones,
       o.importe_tot,
       o.cond_pago,
       o.desc_cond_pago,
       oi.item_oc,
       oi.cantidad ,
       oi.descripcion,
       oi.imp_unitario,
       sgdi.deleg_solic,
       sgdi.nro_solic,
       p.fantasia,
       p.razon_social,
       p.cuit,
       p.calle_postal,
       p.nro_postal,
       p.nro_postal_med,
       p.piso_postal,
       p.dept_postal,
       p.loca_postal,
       lp.Descripcion AS loca_desc_postal,
       p.cod_postal,
       p.calle_legal,
       p.nro_legal,
       p.nro_legal_med,
       p.piso_legal,
       p.dept_legal,
       p.loca_legal,
       ll.Descripcion AS loca_desc_legal,
       p.cod_legal ,
       da.descripcion AS tipo_doc_aprob_desc,
       c.nro_doc_res,
       c.anio_doc_res,
       dr.descripcion AS tipo_doc_res_desc,
       c.nro_cont,
       c.anio_cont,
       co.descripcion AS tipo_doc_cont_desc,
       lo.descripcion AS lug_emi_descripcion,
       sg.jurisdiccion,
       sg.fech_solic,
       sg.codigo_UE AS unidad_ejecutora,
       ue.denominacion AS unidad_ejecutora_denominacion,
       ju.denominacion AS jurisdiccion_descripcion,
       le.descripcion AS lug_ent_descripcion,
       le.calle AS lug_ent_calle,
       le.nro_puerta AS lug_ent_nro_puerta,
       le.nro_med AS lug_ent_nro_med,
       le.piso AS lug_ent_piso,
       le.depto AS lug_ent_depto,
       le.loca AS lug_ent_loca,
       le.cod_postal AS lug_ent_cod_postal,
       led.descripcion AS lug_ent_loca_descripcion,
       pla.descripcion_cod AS descripcion_plazo_entrega,
       cp.DESC_PLAZO_ENT,
       nvl(planent.cantidad,0) AS Cant_plan_ent,
       sg.nro_ped,
       p.nro_pais_te1,
       p.nro_inte_te1,
       p.nro_tele_te1,
       p.fax,
       p.email,
       dep.descripcion AS dep_descripcion,
       c.plazo_ent,
       pe.descripcion_cod,
       sg.codigo_ff,
       FF.denominacion AS fuen_fin_desc,
       co.descripcion AS TCDescripcion,
       c.nro_cont AS TCNro_Cont,
       c.anio_cont AS TCAnio_Cont,
       sg.codigo_dep,
       sgdi.inciso,
       sgdi.par_prin,
       sgdi.par_parc,
       sgdi.tipo,
       sgdi.clase,
       cc.agrupa,
       c.tipo_cont,
       sgdi.codigo_um,
       cum.descripcion AS deno_uni_med,
       pos_iva.descripcion AS pos_iva_desc,
       sgdi.inciso||'.'||sgdi.par_prin||'.'||sgdi.par_parc||'.'||LTRIM (TO_Char(sgdi.clase,'00000'))||'.'||LTRIM(TO_CHAR(sgdi.tipo,'0000')) AS codigo,
       sgdi.programa||'.'||LTRIM(TO_Char(sgdi.activ_proy,'00'))||'.'||LTRIM(TO_Char(sgdi.activ_obra,'00')) AS cat_prog,
       p.NRO_HAB_MUN,
       oi.item_real,
       p.te_celular
FROM  owner_rafam.solic_gastos_def sg,
      owner_rafam.ped_cotizaciones c,
      owner_rafam.cotiza_prov cp,
      owner_rafam.adjudicaciones a,
      owner_rafam.orden_compra o,
      owner_rafam.proveedores p,
      owner_rafam.localidades lp,
      owner_rafam.localidades ll,
      owner_rafam.localidades led,
      owner_rafam.localidades lo,
      owner_rafam.tipo_doc_res da,
      owner_rafam.tipo_doc_res dr,
      owner_rafam.tipos_cont co,
      owner_rafam.jurisdicciones ju,
      owner_rafam.uni_ejec ue,
      owner_rafam.lugares_ent le,
      owner_rafam.plazos_condpago pla,
      owner_rafam.dependencias dep,
      owner_rafam.plazos_entrega pe,
      owner_rafam.pos_iva,
      owner_rafam.oc_items oi,
      owner_rafam.adjudicaciones_items adji,
      owner_rafam.cotiza_prov_items cotpi,
      owner_rafam.ped_cotizaciones_items pci,
      owner_rafam.solic_gastos_def_items sgdi,
     (SELECT ejercicio,
               uni_compra,
               nro_oc,
               count(*) AS cantidad
        FROM owner_rafam.oc_plan_ent pe
        GROUP BY ejercicio,
                 uni_compra,
                 nro_oc) planent,
      owner_rafam.fuen_fin ff,
      owner_rafam.cat_clas cc,
      owner_rafam.cat_uni_med cum,
      owner_rafam.oc_plan_ent ent
WHERE oi.ejercicio=adji.ejercicio
  and oi.deleg_solic=adji.deleg_solic
  and oi.nro_solic=adji.nro_solic
  and oi.item_real=adji.item_real
  and adji.ejercicio=cotpi.ejercicio
  and adji.nro_coti=cotpi.nro_coti
  and adji.cod_prov=cotpi.cod_prov
  and adji.item_real=cotpi.item_real
  and adji.nro_alter=cotpi.nro_alter
  and adji.nro_llamado=cotpi.nro_llamado
  and adji.ejercicio=a.ejercicio
  and adji.nro_adjudic=a.nro_adjudic
  and cotpi.ejercicio=pci.ejercicio
  and cotpi.item_real=pci.item_real
  and cotpi.nro_coti=pci.nro_coti
  and cotpi.ejercicio=cp.ejercicio
  and cotpi.nro_coti=cp.nro_coti
  and cotpi.nro_llamado=cp.nro_llamado
  and pci.nro_llamado=cotpi.nro_llamado
  and pci.ejercicio=sgdi.ejercicio
  and pci.deleg_solic=sgdi.deleg_solic
  and pci.nro_solic=sgdi.nro_solic
  and pci.item_real=sgdi.item_real
  and sg.ejercicio = c.ejercicio
  AND sg.deleg_solic = c.deleg_solic
  AND sg.nro_solic = c.nro_solic
  AND c.nro_llamado = cp.nro_llamado
  AND cp.ejercicio = a.ejercicio
  AND cp.nro_coti = a.nro_coti
  AND cp.cod_prov = a.cod_prov
  AND o.nro_adjud = a.nro_adjudic
  AND o.ejercicio = a.ejercicio
  AND a.nro_coti = c.nro_coti
  AND a.ejercicio = c.ejercicio
  AND a.nro_llamado = c.nro_llamado
   AND o.ejercicio = oi.ejercicio
  AND o.uni_compra = oi.uni_compra
  AND o.nro_oc = oi.nro_oc
/* AND oi.ejercicio = sgdi.ejercicio
  AND oi.deleg_solic = sgdi.deleg_solic
  AND oi.nro_solic = sgdi.nro_solic
  AND oi.item_real = sgdi.item_real*/
  AND p.cod_prov = o.cod_prov
  AND lp.codigo = p.loca_postal
  AND ll.codigo = p.loca_legal
  AND led.codigo = le.loca
  AND o.Lug_Emi = lo.codigo
  AND da.codigo (+) = o.tipo_doc_aprob
  AND dr.codigo (+) = c.tipo_doc_res
  AND co.cod_cont = c.tipo_cont
  AND ju.jurisdiccion = sg.jurisdiccion
  AND ue.codigo_UE = sg.codigo_UE
  AND le.codigo = o.cod_lug_ent
  AND pla.codigo = o.cond_pago
  AND sg.codigo_dep = dep.codigo
  AND cp.plazo_ent = pe.codigo
  and p.cod_iva   = pos_iva.codigo
AND planent.ejercicio (+) = oi.ejercicio
  AND planent.uni_compra (+) = oi.uni_compra
  AND planent.nro_oc (+) = oi.nro_oc
  AND ff.anio_presup = sg.ejercicio
  AND ff.codigo_ff = sg.codigo_ff
  AND cc.clase = sgdi.clase
  AND cotpi.codigo_um = cum.codigo
  AND ent.ejercicio (+) = oi.ejercicio
  AND ent.uni_compra (+) = oi.uni_compra
  AND ent.nro_oc (+) = oi.nro_oc
  AND ent.item_oc(+)=oi.item_oc
  AND ent.oc_plan_sec(+)=0
  AND o.nro_OC > 0
) O
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

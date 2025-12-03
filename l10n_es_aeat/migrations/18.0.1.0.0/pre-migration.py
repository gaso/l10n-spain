# Copyright 2025 GS - Remove obsolete views before upgrade
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

_logger = logging.getLogger(__name__)

# Importar remove_view de Odoo upgrade utils
try:
    from odoo.upgrade import util
    remove_view = util.remove_view
except ImportError:
    remove_view = None


def migrate(cr, version):
    _logger.info("=" * 80)
    _logger.info("L10N_ES_AEAT PRE-MIGRATION: Eliminando vistas obsoletas de res.partner")
    _logger.info("=" * 80)
    
    # Vistas a eliminar (orden: primero las que heredan, luego la base)
    views_to_remove = [
        "l10n_es_aeat_mod347.view_partner_form_mod347",
        "l10n_es_aeat_sii_oca.view_partner_form",
        "l10n_es_aeat.view_partner_form",
    ]
    
    for xml_id in views_to_remove:
        if remove_view:
            try:
                remove_view(cr, xml_id=xml_id, silent=True)
                _logger.info("Vista %s eliminada correctamente", xml_id)
            except Exception as e:
                _logger.info("Vista %s no encontrada o ya eliminada: %s", xml_id, e)
        else:
            _logger.warning("remove_view no disponible, usando fallback SQL")
            _remove_view_sql(cr, xml_id)
    
    _logger.info("=" * 80)
    _logger.info("L10N_ES_AEAT PRE-MIGRATION: Completado")
    _logger.info("=" * 80)


def _remove_view_sql(cr, xml_id):
    """Fallback: eliminar vista con SQL directo"""
    try:
        module, name = xml_id.split(".", 1)
        # Obtener el view_id
        cr.execute("""
            SELECT res_id FROM ir_model_data 
            WHERE module = %s AND name = %s AND model = 'ir.ui.view'
        """, (module, name))
        result = cr.fetchone()
        if result:
            view_id = result[0]
            # Eliminar vistas hijas recursivamente
            cr.execute("""
                WITH RECURSIVE view_tree AS (
                    SELECT id FROM ir_ui_view WHERE id = %s
                    UNION ALL
                    SELECT v.id FROM ir_ui_view v
                    JOIN view_tree vt ON v.inherit_id = vt.id
                )
                DELETE FROM ir_ui_view WHERE id IN (SELECT id FROM view_tree)
            """, (view_id,))
            # Eliminar referencia en ir_model_data
            cr.execute("""
                DELETE FROM ir_model_data 
                WHERE model = 'ir.ui.view' AND res_id = %s
            """, (view_id,))
            _logger.info("Vista %s eliminada con SQL", xml_id)
        else:
            _logger.info("Vista %s no encontrada", xml_id)
    except Exception as e:
        _logger.info("No se pudo eliminar %s: %s", xml_id, e)

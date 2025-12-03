# Copyright 2025 GS - Fix boolean to jsonb migration
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    _logger.info("=" * 80)
    _logger.info("L10N_ES_AEAT_MOD347 PRE-MIGRATION: INICIANDO conversión de not_in_mod347")
    _logger.info("=" * 80)
    
    cr.execute("""
        ALTER TABLE public.res_partner 
        ALTER COLUMN not_in_mod347 TYPE json 
        USING not_in_mod347::text::json;
    """)
    
    _logger.info("=" * 80)
    _logger.info("L10N_ES_AEAT_MOD347 PRE-MIGRATION: COMPLETADA conversión de not_in_mod347")
    _logger.info("=" * 80)

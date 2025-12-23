"""Módulo de páginas - exporta todas las clases de página"""

from pages.base_page import BasePage
from pages.main_page import MainPage
from pages.lead_in_page import LeadInPage
from pages.lead_out_page import LeadOutPage
from pages.shape_page import ShapePage
from pages.translation_page import TranslationPage

__all__ = [
    'BasePage',
    'MainPage',
    'LeadInPage',
    'LeadOutPage',
    'ShapePage',
    'TranslationPage'
]

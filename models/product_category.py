import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)

class product_categ(models.Model):
    _inherit = "product.category"

    code=fields.Char("Group Code")

class PriceListItem(models.Model):
    _inherit = "product.pricelist.item"

    price_list_start_date = fields.Date("Start Date", related='pricelist_id.start_date', store=True)
    price_list_end_date = fields.Date("End Date", related='pricelist_id.end_date', store=True)

import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)

class CFRCRMLead(models.Model):
    _inherit = "crm.lead"

    contact_type = fields.Selection([('Direct Customer', 'Direct Customer'),
                                     ('Distributors', 'Distributors'),
                                     ('Distributors Customer', 'Distributors Customer')],
                                     string="Contact Type", related="partner_id.contact_type", store=True)
    partner_id = fields.Many2one(
        'res.partner', string='End User Name', check_company=True, index=True, tracking=10,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")
    end_user_location = fields.Char("End User Location(city, state)")
    date_deadline = fields.Date('Close Date', help="Estimate of the date on which the opportunity will be won.")
    cfr_po_date = fields.Date("CFR PO Date")
    probability = fields.Float(
        'Get % (CFR will get an order)', group_operator="avg", copy=False,
        compute='_compute_probabilities', readonly=False, store=True)
    probability_of_project_happening = fields.Float("Go % (project happening)", copy=False)
    current_status_and_action_to_win = fields.Text("Current Status and Action to Win")
    cfr_ship_date = fields.Date("CFR Ship Date")

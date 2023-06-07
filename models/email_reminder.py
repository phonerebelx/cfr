import logging
from datetime import timedelta
from odoo import api, models, fields
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def send_reminder_email(self):
        pending_orders = self.search([('state', '=', 'waiting')])
        team_members = self.env['crm.team'].search([])
        
        mail = None
        for team_member in team_members:
                if team_member.member_ids:
                    # raise UserError(str(team_member.user_id))
                    mail = team_member.user_id.login
                    
                        
                    if mail:
                        
                        for members in team_member.member_ids:
                            pending_orders=self.search([('state', '=', 'waiting'),('user_id','=',members.name)])
                            for order in pending_orders:
                                    # raise UserWarning(str(order))
                                    template = self.env.ref('cfr.sale_order_email_template')
                                    # template = self.env.ref('sale.email_template_edi_sale')
                                    # raise UserError(template)
                                    menu_id=self.env['ir.ui.menu'].sudo().search([('name','=','Sales'),('parent_id','=',False)],limit=1)
                                    menu_id=menu_id.id if menu_id else 0

                                    # raise UserError(str(order.id))

                                    action=self.env['ir.actions.actions'].sudo().search([('name','=','Sales Orders')],limit=1)
                                    action=action.id if action else 0
                                    order_id=order.id
                                    # raise UserError(order_id)
                                    template.write({
                                        'email_from': self.company_id.email,
                                        'email_to': mail,
                                        'body_html': template.body_html.replace('sid', "LALA")
                                                            .replace('menu_ids', str(menu_id))
                                                            .replace('action_id', str(action))
                                                            .replace('sale_order.id', str(order_id))
                                    })

                                    # raise UserError(str(template['body_html']))
                                    template.send_mail(order.id, force_send=True)
                    
    @api.model
    def send_pending_approval_email(self):
        sale_order = self.env['sale.order']
        sale_order.send_reminder_email()

    def init(self):
        ext=self.env['ir.cron'].sudo().search([('name','=','Send Pending Approval Email')])
        if not ext:
            self.env['ir.cron'].sudo().create({
                'name': 'Send Pending Approval Email',
                'model_id': self.env['ir.model'].search([('model','=','sale.order')]).id,
                'interval_number': 1,
                'interval_type': 'days',
                'numbercall': -1,
                'doall': False,
                'active': True,
                'code': 'model.send_pending_approval_email()',
            })         
            

            



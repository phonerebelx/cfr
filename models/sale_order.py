import logging
from odoo import api, fields, models,_
from odoo.addons.base.models.ir_mail_server import MailDeliveryException
from odoo.tools import html2plaintext
from odoo.exceptions import UserError
from odoo.http import request
from werkzeug.urls import url_encode, url_join
import jinja2
_logger = logging.getLogger(__name__)



class SaleOrder(models.Model):
    _inherit = "sale.order"

    payment_term_id2 = fields.Many2one('cfr.terms', string="Payment Terms", compute="term_compute")
    delivery_set = fields.Boolean(compute='_compute_delivery_state')
    recompute_delivery_price = fields.Boolean('Delivery cost should be recomputed')
    is_all_service = fields.Boolean("Service Product", compute="_compute_is_service_products")

    def term_compute(self):
        self.payment_term_id2=self.partner_id.terms_code

    open_order = fields.Boolean("Open Order")
    # order_number = fields.Integer("Order Number")
    l10n_in_company_country_code = fields.Char(
        string='Company Country Code',
    )
    customer_num = fields.Integer("Customer Number")
    ship_to_num = fields.Char('Ship to Number')
    fob = fields.Selection([('CIF', 'CIF'),
                            ('DDP', 'DDP'),
                            ('EXW', 'EXW'),
                            ('FCA', 'FCA'),
                            ('FOB Destination', 'FOB Destination'),
                            ('OTH', 'OTH')
                            ], string="FOB")
    entry_person = fields.Many2one('res.partner', string="Entry person")
    ship_via_code = fields.Selection([('BW', 'BW'),
                                      ('IC', 'IC'),
                                      ('GFX', 'GFX'),
                                      ('OTHE', 'OTHE'),
                                     ], string="Ship Via Code")
    order_comment = fields.Char("Order Comment")              
    need_by_date  = fields.Date("Need By Date")
    ship_order_complete = fields.Boolean("Ship Order Complete")              
    web_order = fields.Boolean("Web Order")              
    linked = fields.Boolean("Linked")              
    ic_po_num = fields.Boolean("IC PO Number")              
    ext_company = fields.Many2one('res.company', string="Ext Company")              
    total_lines = fields.Integer("Total Lines")
    total_invoiced = fields.Float("Total Invoiced")
    order_amt = fields.Float("Order Amount")
    proforma_inv_comment = fields.Char("ProForma Invoice Comment")
    sold_to_address = fields.Char("Sold To Address")
    original_customer_po = fields.Char("Original Customer PO")
    order_type = fields.Selection([('Customer', 'Customer'),
                                   ('Service', 'Service'),
                                   ('Stock', 'Stock'),
                                   ('Repair', 'Repair'),
                                   ('Warranty', 'Warranty'),
                                   ('Emergency', 'Emergency'),
                                   ('Program', 'Program'),
                                  ], string="Order Type")
    ep_request_date = fields.Char(
        string='Request Date',
    )
    ep_void_order = fields.Char(
        string='Void Order',
    )
    ep_terms_code = fields.Char(
        string='Terms Code',
    )
    ep_discount_percent = fields.Char(
        string='Discount Percent',
    )
    ep_sales_rep_list = fields.Char(
        string='Sales Rep List ',
    )
    ep_ship_comment = fields.Text(
        string='Ship Comment',
    )
    ep_invoice_comment = fields.Text(
        string='Invoice Comment',
    )
    ep_picklist_comment = fields.Text(
        string='PickList Comment',
    )
    ep_edi_order= fields.Char(
        string='EDI Order',
    )
    ep_edi_ack = fields.Char(
        string=' EDI ACK',
    )
    ep_web_entry_person = fields.Char(
        string='Web Entry Person',
    )
    ep_drop_ship = fields.Char(
        string='Drop Ship',
    )
    ep_commercial_invoice = fields.Char(
        string='Commercial Invoice',
    )
    ep_ship_exprt_declartn = fields.Char(
        string='Ship Exprt Declation',
    )
    ep_cert_of_origin = fields.Char(
        string='Cert of Origin',
    )
    ep_latter_of_instr = fields.Char(
        string='Later Of Instr',
    )
    ep_change_date = fields.Char(
        string='Change Date ',
    )
    ep_total_charges = fields.Char(
        string='Total Changes ',
    )
    
    
    
    ep_order = fields.Char(
            string='Order',
        )
    ep_purchase_order = fields.Char(
            string='Purchase Order',
        )
    ep_customer = fields.Char(
            string='Customer',
        )
    
    ep_bill_to_customer_entry = fields.Char(
            string='Bill To Customer Entry',
        )
    ep_one_time = fields.Boolean(
            string='One Time',
        )
    ep_attn = fields.Char(
            string='Attn',
        )
    ep_ship_to = fields.Char(
            string='Ship To',
        )
    ep_need_by = fields.Char(
            string='Need By',
        )
    ep_ship_by = fields.Char(
            string='Ship By',
        )
    ep_ship_by_time = fields.Char(
            string='Ship By Time',
        )
    ep_counter_sale = fields.Boolean(
            string='Counter Sale ',
        )
    ep_Packing_slip = fields.Boolean(
            string='Packing Slip',
        )
    ep_reday_to_process = fields.Boolean(
            string='Ready To Process',
        )
    ep_ready_to_fullfill = fields.Boolean(
            string='Ready To Fullfill',
        )
    ep_hold = fields.Boolean(
            string='Hold',
        )
    ep_invoice = fields.Boolean(
            string='Invoice',
        )
    ep_charges = fields.Char(
            string='Charges',
        )
    ep_discount = fields.Char(
            string='Discount',
        )
    ep_misc = fields.Char(
            string='Misc',
        )
    ep_tax = fields.Char(
            string='Tax',
        )
        
    ep_rounding = fields.Char(
            string='Rounding',
        )
    ep_order_total = fields.Char(
            string='Order Total',
        )
    ep_order_address = fields.Text(
        string='Address',
    )
    ep_order_phone = fields.Char(
            string='Phone',
        )

    lead_time = fields.Char(string="Lead Time")


    mail_team_lead = fields.Char(compute='_inside_call')

    def _inside_call(self):
        self.compute_team_lead_button_compute()
        self.mail_team_lead ='inside'


    def mail_compute(self):

        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        template = self.env.ref('cfr.sale_order_email_template')
        context = {'object': self}
        team_members = self.env['crm.team'].search([])
        mail = None

        for team_member in team_members:
                if team_member.member_ids:
                    for members in team_member.member_ids:
                        if members.name == self.user_id.name:
                            mail = team_member.user_id.login


        if not mail:
            raise UserError('Email of Team lead not exist')

        menu_id = self.env.ref('sale.menu_sale_quotations').id
        action = self.env.ref('sale.action_orders').read()[0]['id']
        #

        # self.mail_team_lead = str(email_body)
        template.write({
                'email_from': self.company_id.email,
                'email_to': mail,
                'body_html': template.body_html.replace('sale_order.id', str(self.id))
                                     .replace('menu_ids', str(menu_id))
                                     .replace('action_id', str(action))
            })


        context = dict(
            default_model='sale.order',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            mark_so_as_sent=True
        )
        self.mail_team_lead = str(menu_id)
        return {
            'name': 'Compose Email',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': context,
        }



    send_to_manager_button = fields.Boolean(string='Send to Team Leader', type='object',
                                           help='Send order to manager for approval.',
                                           icon='fa-send-o')

    @api.depends('order_line.price_total')
    def _amount_all(self):
        print(self,'return none')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('waiting', 'Waiting Approval'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    discount_percent = fields.Float(string='Discount in %', digits=(16, 2))
    discount = fields.Float(string='Discount',store=True, digits=(16, 2))
    SubTotal = fields.Float(string='Sub Total', store=True,track_visibility='always',digits=(16, 2))
    SubTotal_fuel = fields.Float(string='Fuels Amount', store=True,track_visibility='always',digits=(16, 2))
    Products_amount = fields.Float(string='Products Amount', store=True,track_visibility='always',digits=(16, 2))
    Total = fields.Float(string='Total', store=True,track_visibility='always',digits=(16, 2))
    amount_total = fields.Monetary(string='Total', store=True, readonly=True,
                                   track_visibility='always',compute='_amount_all')

    @api.model
    def fields_view_get(self,view_id=None, view_type='form', toolbar=False, submenu=False):

        res = super(SaleOrder, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
                                                     submenu=submenu)

        if self._context.get('params'):


            if 'id' in self._context.get('params'):
                if view_type == 'form' and self._context.get('params')['model'] == 'sale.order':

                    self.compute_team_lead_button(self._context.get('params')['id'])



        return res


    def compute_team_lead_button_compute(self):
        current_user = request.env.user
        username = current_user.name

        if self.state == 'waiting':
            team_members = self.env['crm.team'].search([])

            for team_member in team_members:
                if team_member.user_id.name == username:
                    self.send_to_manager_button = True
                    break
                else:
                    self.send_to_manager_button = False
        else:
            self.send_to_manager_button = False

    def compute_team_lead_button(self, id):
        current_user = request.env.user
        username = current_user.name
        sale_object = self.env['sale.order'].search([('id', '=', id)])
        if sale_object.state == 'waiting':
            team_members = self.env['crm.team'].search([])
            for team_member in team_members:
                if team_member.user_id.name == username:
                    sale_object.send_to_manager_button = True
                    break
                else:
                    sale_object.send_to_manager_button = False
        else:
            sale_object.send_to_manager_button = False

    def button_send_to_manager(self):
        if self.state == 'waiting':
            self.state = 'sale'


    @api.onchange('order_line','pricelist_id','sale_order_option_ids')
    def sub_total_insert(self):

        


        # for order in self:
        stotal = self.order_line.mapped(
            lambda line: (line.price_subtotal)
        )
        
        options = self.sale_order_option_ids.mapped(
            lambda line: (line.price_unit * line.quantity)
        )
        stotal = sum(stotal)
        options=sum(options)
        self.SubTotal_fuel=options
        self.Products_amount=stotal
        self.SubTotal = stotal + options

        self.action_confirm_button()
        # raise UserError("OK so")



    # @api.model
    # def _before_confirm_sale_order(self, order):
    #     if 
    #     pass


    # def update_prices(self):
    # return super(SaleOrder, self).update_prices()
    
    def action_confirm(self):
        
        if self.state=='draft':
            if self.discount_percent>0:
                self.state='waiting'
                return
        
        return super(SaleOrder, self).action_confirm()
    

            # calc_discount = order.SubTotal * (order.discount_percent or 0.0) / 100.0
            # order.discount = calc_discount

            # order.amount_total = order.SubTotal - order.discount
    @api.onchange('discount_percent')
    def dis_change(self):
        if self.state in 'draft':
            self.action_confirm_button()
        else:
            raise UserError("Can't apply discount in this stage, reset to draft first")
        
        self.sub_total_insert()

        # if self.discount>0:
        #     self.state='waiting'

        # self.write({'state': 'waiting'})
        

    # @api.model
    # def action_check(self, record_id):

        # record = self.browse(record_id)
        # if self.discount_percent > 0.0:

        #     state_check = 'waiting'
        #     record.state = state_check
        # else:
        #     state_check = 'draft'
        #     record.state = state_check
        # record.write({'state': state_check})


    def action_confirm_button(self):
        record = self.browse(self.id)
        # self.action_check(self.id)
        calc_discount = self.SubTotal * (self.discount_percent or 0.0) / 100.0
        self.discount = calc_discount
        # record.write({'discount': calc_discount})

        self.amount_total = self.SubTotal - self.discount
        record.amount_untaxed = self.SubTotal - self.discount
        # record.write({'amount_total': self.SubTotal - self.discount})

        # self.action_check(self.id)
    #

    @api.model
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        print(invoice_vals)
        invoice_vals.update({
            'amount_total': self.amount_total,
            'tax_totals_json': self.amount_total,
        })
        # invoice_vals.write({'amount_total': self.amount_total})
        print(self.amount_total, invoice_vals.get('tax_totals_json', 0))

        return invoice_vals

    def open_so_line(self):
        # vendor_bill_id = self.create_single_vendor_bill()
        so_id = self.id
        tree_view = self.env.ref('cfr.cfr_open_sale_order_line_tree', False)
        action = self.env.ref('cfr.cfr_sale_order_line_action').read()[0]
        action['views'] = [(tree_view.id, 'tree')]

        action['context'] = {
            'default_order_id': self._origin.id,
        }
        action['domain'] = "[('order_id', '=', " + str(self._origin.id) + ")]"

        _logger.debug(f'action {action}')

        return action


class SaleOrderLine(models.Model):
    _inherit = "sale.order.option"

    quote_type=fields.Selection(string="Quote Type",related="order_id.quote_type")

    @api.onchange('quote_type')
    def qt_change(self):
        #  raise UserError("Test")

        ids=[]
        tmp_ids=[]

        for line in self.order_id.pricelist_id.item_ids:
            
            if line.product_id:
                if line.product_id.id not in ids:
                    ids.append(line.product_id.id)

                if line.product_id.product_tmpl_id.id not in tmp_ids:
                    tmp_ids.append(line.product_id.product_tmpl_id.id)
            
            if line.product_tmpl_id:
                if line.product_tmpl_id.id not in tmp_ids:
                    tmp_ids.append(line.product_tmpl_id.id)

                for varients in line.product_tmpl_id.product_variant_ids:
                    if varients.id not in ids:
                        ids.append(varients.id)
                        
        return {'domain': {
                        'product_id': [('id','in',ids),('categ_id','=', 'Rating Reference Fuels')],
                        }
            }

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    open_line = fields.Boolean("Open Line") 
    order_line = fields.Integer("Order Line") 
    line_type = fields.Char("Line Type") 
    part_num = fields.Char("Part Number") 
    revision_num = fields.Char("Revision Number") 
    doc_unit_price = fields.Float("Doc Unit Price")
    request_date = fields.Date("Request Date")
    prod_code = fields.Char("Product Code")
    order_comment = fields.Char("Order Comment")
    ship_comment = fields.Char("Ship Comment")
    invoice_comment = fields.Char("Invoice Comment")
    pickList_comment = fields.Char("PickList Comment")
    need_by_date = fields.Date("Need By Date")
    warranty = fields.Boolean("Warranty")
    ship_line_complete = fields.Boolean("Ship Line Complete")
    linked = fields.Boolean("Linked")
    ic_po_num = fields.Integer("IC PO Number")
    ic_po_line = fields.Integer("IC PO Line")
    price_list_code = fields.Char("PickList Comment")
    doc_ord_based_price = fields.Float("Doc Ord Based Price")
    ext_price_dtl = fields.Float("Ext Price Dtl")
    doc_ext_price_dtl = fields.Float("Doc Ext Price Dtl")
    void_line = fields.Char(
        string='Void Line',
    )
    quote_num = fields.Char(
        string='Quote Number',
    )
    quote_line = fields.Char(
        string='Quote Line ',
    )
    cust_num = fields.Char(
        string='Customer Number',
    )
    contact_num = fields.Char(
        string='Contact Number ',
    )
    selling_quantity = fields.Char(
            string='Selling Quantity  ',
    )
    mktg_campaing_id = fields.Char(
         string='MKTG Compaingn ID',
    )
    mktg_evnt_seq = fields.Char(
        string='MKTG Evnt Seq',
    )
    link_to_contract = fields.Char(
        string='Link To Contract  ',
    )


    quote_type=fields.Selection(string="Quote Type",related="order_id.quote_type")

    @api.onchange('quote_type')
    def qt_change(self):
        #  raise UserError("Test")
        #  return {'domain': {
        #                     'product_id': [('categ_id','=' if self.quote_type=='unit' else '!=' , 'Unit Base')],
        #                     'product_template_id': [('categ_id','=' if self.quote_type=='unit' else '!=' , 'Unit Base')]
        #                     }
        #      }


        ids=[]
        tmp_ids=[]

        for line in self.order_id.pricelist_id.item_ids:
            
            if line.product_id:
                if line.product_id.id not in ids:
                    ids.append(line.product_id.id)

                if line.product_id.product_tmpl_id.id not in tmp_ids:
                    tmp_ids.append(line.product_id.product_tmpl_id.id)
            
            if line.product_tmpl_id:
                if line.product_tmpl_id.id not in tmp_ids:
                    tmp_ids.append(line.product_tmpl_id.id)

                for varients in line.product_tmpl_id.product_variant_ids:
                    if varients.id not in ids:
                        ids.append(varients.id)
    
            
            # if line.product_tmpl_id
        
        return {'domain': {
                            'product_id': [('id','in',ids),('categ_id','not in', 'Rating Reference Fuels')],
                            'product_template_id': [('id','in',tmp_ids),('categ_id','not in', 'Rating Reference Fuels')],
                            
                            }
             }


    @api.model
    def create(self, vals):
        line = super(SaleOrderLine, self).create(vals)
        # Call the method to update the subtotal and total
        line.order_id.sub_total_insert()
        return line

    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        # Call the method to update the subtotal and total
        self.order_id.sub_total_insert()
        return res
    


    # discount = fields.Float(string='Discount',store=True)
    # total = fields.Float(string='Total',digits=(16, 2))
    # @api.onchange('price_unit', 'product_uom_qty', 'discount_percent')
    # def _compute_discount(self):
    #     for line in self:
    #         global global_var
    #         line.discount = line.price_subtotal * (line.discount_percent or 0.0) / 100.0
    #         line.price_subtotal = line.price_unit - line.discount
    #         global_var = line.discount_percent
    #
    #
    #
    # def write(self, vals):
    #     print(vals)
    #     if 'discount_percent' in vals:
    #         for line in self:
    #             line.discount = line.price_subtotal * (vals['discount_percent'] or 0.0) / 100.0
    #             line.price_subtotal = line.price_unit - line.discount
    #     if 'qty_delivered_manual' in vals:
    #         for line in self:
    #             line.discount = line.price_subtotal * (global_var or 0.0) / 100.0
    #             line.price_subtotal = line.price_unit - line.discount
    #     return super(SaleOrderLine, self).write(vals)

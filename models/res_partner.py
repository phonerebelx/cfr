# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)

ADDRESS_FIELDS = ('street', 'street2', 'street3', 'zip', 'city', 'state_id', 'country_id')

class CFRResPartner(models.Model):
    _inherit = "res.partner"
    
    
    
    street3 = fields.Char(string="Street 3")
    tax_ids = fields.Many2many('account.tax', 'rel_customer_tax', 'customer_id', 'tax_id', string="Default Taxes")
    customer_id = fields.Char('Customer ID')
    customer_num = fields.Integer('Customer Number',readonly="1")
    territory_id = fields.Many2one('cfr.territory', string="Territory")
    ship_to_num = fields.Char('Ship to Number')
    terms_code = fields.Many2one('cfr.terms', string="Payment Terms")
    ship_via_code = fields.Many2one('cfr.shipvia', string="Ship Via")
    group_code = fields.Char('Group Code',readonly="1")
    est_date = fields.Date('EST Date',readonly="1")
    fax_num = fields.Char('Fax Number')
    tax_exempt = fields.Char('Tax Exempt',readonly="1")
    one_inv_per_ps = fields.Boolean('One Inv per PS',readonly="1",compute="fax_compute")
    default_fob  = fields.Many2one('cfr.fob',string='Shipping Terms')
    credit_include_orders = fields.Boolean('Credit Include Orders',readonly="1")
    credit_hold = fields.Boolean('Credit Hold',readonly="1")
    credit_hold_date = fields.Date('Credit Hold Date',readonly="1")
    credit_clear_user_id = fields.Many2one('res.users', string="Credit Clear User",readonly="1")
    credit_clear_date = fields.Date('Credit Clear Date',readonly="1")
    edi_code = fields.Char('EDI Code',readonly="1")
    cust_url = fields.Char('Customer URL')

    acronym = fields.Char('Acronym')
    business_as = fields.Char('Doing Business As')
    # same_bill_address = fields.Boolean('Bill Address same as Customer Address')

    @api.model
    def _address_fields(self):
        """Returns the list of address fields that are synced from the parent."""
        return list(ADDRESS_FIELDS)

    @api.model
    def _get_default_address_format(self):
        return "%(street)s\n%(street2)s\n%(street3)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s"


    def fax_compute(self):
        self.one_inv_per_ps=False
        fax=self.format_phone_number(self.fax_num) if self.fax_num else False
        self.fax_num=fax

        phone=self.format_phone_number(self.phone) if self.phone else False
        self.phone=phone

        mobile=self.format_phone_number(self.mobile) if self.mobile else False
        self.mobile=mobile

        self.write({'fax_num':fax,'phone':phone,'mobile':mobile})
    
    @api.onchange('phone','fax_num','mobile')
    def phone_fax_change(self):
        self.fax_compute()
        
    
    def format_phone_number(self,number):
        number = ''.join(filter(str.isdigit, number))
        
        if len(number) == 10:
            return f"{number[:3]}-{number[3:6]}-{number[6:]}"
        elif len(number) == 12 and '-' not in number and '(' not in number and ')' not in number:
            return f"({number[:2]}) {number[2:5]}-{number[5:8]}-{number[8:]}"
        elif len(number) == 11 and '-' not in number and '(' not in number and ')' not in number:
            return f"({number[:1]}) {number[1:4]}-{number[4:7]}-{number[7:]}"
        else:
            return number
    


    
    ship_to_terr_id = fields.Many2one('cfr.territory', string="Ship to Territory")
    credit_review_date = fields.Date('Credit Review Date',readonly="1")
    customer_type = fields.Selection([('CUS', 'CUS'), ('PRO', 'PRO'), ('SUS', 'SUS')], "Customer Type", default="CUS")
    preferred_bank = fields.Char("Preferred Bank")
    
    contact_type = fields.Selection([('Direct Customer', 'Direct Customer'),
                                     ('Distributors', 'Distributors'),
                                     ('Distributors Customer', 'Distributors Customer')], "Contact Type")
                                     
                                     
    ep_ic_trader = fields.Boolean('IC Trader',readonly="1")
    ep_sales_repcode= fields.Char(
            string='Sales Person',
        )
    ep_tax_exempt= fields.Char(
            string='Tax Exempt',
        )
    ep_currency_code= fields.Char(
            string='Currency Code',
        )
    ep_Country_num= fields.Char(
            string='Country Number',
        )
    bt_name= fields.Char(
            string='Bill to  Name',
        )
    bt_address1= fields.Char(
            string='Bill To Address 1 ',
        )
    bt_address2= fields.Char(
            string='Bill To Address2 ',
        )
    bt_address3= fields.Char(
            string='Bill To Address3',
        )
    bt_city= fields.Char(
            string='Bill to City ',
        )
    bt_state= fields.Char(
            string='Bill to State',
        )
    bt_zip= fields.Char(
            string='Bill To Zip',
        )
    bt_country_num= fields.Char(
            string='Bill to Country Num ',
        )
    bt_country= fields.Char(
            string='Bill to Country ',
        )
    bt_phone_num= fields.Char(
            string='Bill to Phone Number ',
        )
    
    bt_fax_num= fields.Char(
            string='Bill to Fax  ',
        )
    bt_formate_str= fields.Char(
            string='Bill to Formate Str ',
        )
   

    ep_cust_pi_limit= fields.Char(
            string='Customer PI Limit ',
        )
        
    ff_id= fields.Char(
            string='FF ID',readonly="1"
        )
    ff_name= fields.Char(
            string='FF Comp Name',
        )
    ff_address1= fields.Char(
            string='FF Address 1 ',
        )
    ff_address2= fields.Char(
            string='FF Address2 ',
        )
    ff_address3= fields.Char(
            string='FF Address3',
        )
    ff_city= fields.Char(
            string='FF City ',
        )
    ff_state= fields.Char(
            string='FF State',
        )
    
    ff_country= fields.Char(
            string='FF Country ',
        )
    ff_country_num= fields.Char(
            string='FF Country Number ',
        )
    ff_phone_num= fields.Char(
            string='FF Phone Number ',
            
        )
    ep_ship_to_terrlist = fields.Char(
        string='Ship to Territory List',
    )
        
    ep_number_of_employee = fields.Char(
        string='Number of Employees',
    )
    
    ep_inactive = fields.Boolean(
        string='Inactive'
    )
    ep_exclude_from_address_validation = fields.Boolean(
        string='Exclude From Address Validation',
    )
    
    ep_territory_locked = fields.Boolean(
            string='Territory Locked',
        )
    ep_sales_person = fields.Char(
            string='Sales Person',
        )
    ep_quote_markup = fields.Char(
            string='Quote Markup',
        )
    ep_reservation_priority = fields.Char(
            string='Reservation Priority ',readonly="1"
        )
    ep_shipping_qualifier = fields.Char(
            string='Shipping Qualifier  ',
        )
    ep_language = fields.Char(
            string='Language ',
        )
    ep_supplier_code = fields.Char(
            string='Supplier Code',
        )
    ep_save_ots_as = fields.Char(
            string='Save OTS As',
        )
    ep_acknowledgment = fields.Boolean(
            string='Acknowledgment',
        )
    ep_statments = fields.Boolean(
            string='Statments',
        )
    ep_labels= fields.Boolean(
            string='Labels',
        )
    
    ep_eori = fields.Char(
            string='EORI',
        )
    ep_supplier_id = fields.Char(
            string='Supplier Id',
        )
        
        
    ep_valid_player = fields.Boolean(
            string='Valid Payer',
        )
    ep_valid_sold_to= fields.Boolean(
            string='Valid Sold TO',
        )
    ep_valid_ship_to= fields.Boolean(
            string='Valid Ship To',
        )
    ep_allow_onetime_ship_to= fields.Boolean(
            string='Allow One Time Ship To',
        )
    ep_allow_shipto_third_party= fields.Boolean(
            string='Allow Ship To Third Party',
        )
    ep_no_contact= fields.Boolean(
            string='No Contact',
        )
    ep_global_lock = fields.Boolean(
            string='Global Lock',
        )
    ep_check_duplicate_PO = fields.Boolean(
            string='Check Duplicate Po',
        )
    ep_globle= fields.Boolean(
            string='Global',
        )
    ep_central_collection = fields.Boolean(
            string='Central Collection',
        )
    ep_web_customer = fields.Boolean(
            string='Web Customer',
        )
    ep_business_model = fields.Char(
            string='Business Model',
        )
    ep_comments = fields.Text(
        string='Comments',
    )
    ep_available_restrictions = fields.Boolean(
            string='Available Reservation',
        )
    
    
    
    
    

    
    # @api.onchange('same_bill_address')
    # def same_bill_onchenge(self):
    #     if self.same_bill_address:
    #         self.bt_address1=self.street
    #         self.bt_address2=self.street2
    #         self.bt_city=self.city
    #         self.bt_state=self.state_id.name
    #         self.bt_zip=self.zip
    #         self.bt_country=self.country_id.name

    # @api.onchange('street','street2','city','state_id','zip','country_id')
    # def onchange_ad(self):
    #     if self.same_bill_address:
    #         self.same_bill_onchenge()
            
            
        

    
class CFRTerritory(models.Model):
    _name = 'cfr.territory'
    _description = "CFR Territory"

    name = fields.Char('Territory Name', required="1")
    code = fields.Char('Territory Code', required="1")

class CFRShipvia(models.Model):
    _name = 'cfr.shipvia'
    _description = "CFR Ship Via"

    name = fields.Char('Description', required="1")
    code = fields.Char('Code', required="1")

class CFRTerms(models.Model):
    _name = 'cfr.terms'
    _description = "CFR Terms"

    name = fields.Char('Description', required="1")
    code = fields.Char('Code', required="1")

class CFRFob(models.Model):
    _name = 'cfr.fob'
    _description = "CFR Terms"

    name = fields.Char('Description', required="1")
    code = fields.Char('Code', required="1")

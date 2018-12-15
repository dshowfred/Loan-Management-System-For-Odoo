# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math


class crm_lead(models.Model):
    _inherit = 'crm.lead'

    loanType_id = fields.Many2one('loan.type', "Type")
    loanDuration_id = fields.Many2one('loan.duration', "Duration")
    alternateEmail = fields.Char("Alternative Email")
    loanAmount = fields.Float("Loan Amount")

    @api.multi
    def action_send_emaill(self):
        self.ensure_one()
        print("Mail Sended.............")
        template = self.env.ref(
            'loan_management.loan_document_upload_notification_email_template')
        self.env['mail.template'].browse(template.id).send_mail(self.id)


class loan_type(models.Model):
    _name = 'loan.type'

    name = fields.Char("Loan Type")


class loan_duration(models.Model):
    _name = 'loan.duration'

    name = fields.Char("Loan Durantion Name", compute='_compute_name')
    duration = fields.Integer("Loan Durantion")
    typee = fields.Selection([('Years', 'Years'), ('Months', 'Months')], required=True, default='Years')

    @api.depends('duration', 'typee')
    def _compute_name(self):
        for rec in self:
            rec.name = str(rec.duration) + " " + rec.typee

class loan_proof(models.Model):
    _name = 'loan.proof'

    name = fields.Char("Proof Type Name")
    shortcut = fields.Char("Shortcut")


class loan_installment(models.Model):
    _name = 'loan.installment'

    name = fields.Char("Installment")
    customer_id = fields.Many2one('loan.loan')
    loantype = fields.Char('Loan Type')


class loan_loan(models.Model):
    _name = 'loan.loan'
    _rec_name = 'customer_id'

    name = fields.Char("Loan ID")
    applyDate = fields.Datetime("Apply Date")
    approveDate = fields.Datetime("Approve Date")
    customer_id = fields.Many2one('res.partner')
    loanAmount = fields.Float("Loan Amount")
    duration_id = fields.Many2one('loan.duration')
    loantype_id = fields.Many2one('loan.type')
    totalInstallment = fields.Integer("Total Installment", compute="_totalInstallment")
    approveAmount = fields.Float("Approve Amount")
    interestRate = fields.Float("Interest Rate")
    processFees = fields.Float("Processing Fee")
    descriptionn = fields.Char("Description")

    loanAmount1 = fields.Float("Loan Amount", related="loanAmount")
    totalInstallment1 = fields.Integer("Total Installment", related="totalInstallment")
    interestRate1 = fields.Float("Installment Rate", related="interestRate")

    calc_monthly_emi = fields.Float("Calculated Monthly EMI")
    amount_with_interest = fields.Float("Total Amount With Interest")
    interest_PA = fields.Float("Flat Interest Rate PA")
    interest_PM = fields.Float("Float Interest Rate PM")
    total_interest_amount = fields.Float("Total Interest Amount")
    yearly_interest_amount = fields.Float("Yearly Interest Amount")

    @api.onchange('customer_id')
    def _onchange_customer_id(self):
        record = self.env['crm.lead'].search(
            [('partner_id', '=', self.customer_id.id)], limit=1)
        for rec in record:
            if rec.loanDuration_id != None:
                self.duration_id = rec.loanDuration_id
                self.applyDate = rec.date_open
            if rec.loanAmount != None:
                self.loanAmount = rec.loanAmount
            if rec.loanType_id != None:
                self.loantype_id = rec.loanType_id       

    @api.depends('duration_id')
    def _totalInstallment(self):
        duration = 0
        if self.duration_id.typee == 'Years':
            duration = self.duration_id.duration * 12
        elif self.duration_id.typee == 'Months':
            duration = self.duration_id.duration
        self.totalInstallment = duration

    @api.depends('loanAmount1', 'interestRate1', 'totalInstallment1')
    def calculate_emi(self):
        principal_amount = self.loanAmount1
        rate = self.interestRate1 / (12 * 100)
        time = self.totalInstallment1
        emi = (principal_amount * rate * pow(1 + rate, time)) / (pow(1 + rate, time) - 1)

        self.calc_monthly_emi = emi
        self.amount_with_interest = emi * time
        self.total_interest_amount = self.amount_with_interest - principal_amount
        if self.duration_id.typee == 'Years':
            self.yearly_interest_amount = self.total_interest_amount / self.duration_id.duration
        print("================>", emi)

# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Contains information about an offer on a property."

    name = fields.Char()
    description = fields.Text()
    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    create_date = fields.Date(default=lambda self: fields.Date.today())
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline",
                                inverse="_inverse_date_deadline")

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            curr_date = record.create_date \
                if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(
                curr_date, days=+record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today()

    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        self.validity = (self.date_deadline - self.create_date).days

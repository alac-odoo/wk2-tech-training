# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Contains information about an offer on a property."
    _order = "price desc"

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

    property_type_id = fields.Many2one("estate.property.type",
                                       related="property_id.property_type_id",
                                       store=True)

    _sql_constraints = [('check_offer',
                         'CHECK (price > 0)',
                         'The offer must be higher than 0.00.')]

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

    # note: do not use api.onchange() to add business logic
    # because onchange only works in form view
    # TODO: rework to use api.depends()
    @api.onchange('date_deadline')
    def _onchange_validity(self):
        self.validity = (self.date_deadline - self.create_date).days
        self.validity = self.validity if self.validity > 0 else 0

    @api.depends('property_id', 'price', 'partner_id')
    def action_accept_offer(self):
        for record in self:
            if (record.property_id.state == 'accepted') | \
                    (record.property_id.state == 'sold') | \
                    (record.property_id.state == 'cancelled'):
                raise exceptions.UserError(
                    "An offer was already accepted or the property has sold.")
            else:
                record.status = 'accepted'
                record.property_id.state = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True

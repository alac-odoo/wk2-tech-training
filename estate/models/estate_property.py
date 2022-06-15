# -*- coding: utf-8 -*-

from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Contains information about an estate property."

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Date.add(
        fields.Date.today(), months=+3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('east', 'East'),
                   ('south', 'South'), ('west', 'West')],
        help="If in between directions, choose North or South."
    )
    total_area = fields.Integer(compute="_compute_total_area")
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='Status',
        selection=[('new', 'New'), ('received', 'Offer Received'),
                   ('accepted', 'Offer Accepted'), ('sold', 'Sold'),
                   ('cancelled', 'Cancelled')],
        help="The current status of this property.",
        default='new',
    )
    property_type_id = fields.Many2one("estate.property.type",
                                       string="Property Type")
    buyer = fields.Many2one("res.partner", copy=False)
    salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag",
                               string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer",
                                "property_id",
                                string="Offer")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            # catches properties with no offers
            record.best_price = max(record.mapped('offer_ids.price')) \
                if record.mapped('offer_ids.price') else 0.00

# -*- coding: utf-8 -*-

from odoo import api, fields, models, exceptions, tools


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Contains information about an estate property."
    _order = "property_type_id"
    # also equivalent <[view] default_order="[field] [options]">
    # works for many2one but not one2many

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
    garden = fields.Boolean(default=False)
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
                                string="Offers")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [('check_expected_price',
                         'CHECK (expected_price > 0)',
                         'The expected price must be higher than 0.00.'),
                        ('check_selling_price',
                         'CHECK (selling_price > 0)',
                         'The selling price must be higher than 0.00.')]

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

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = 'north' if self.garden else ''

    def action_status_sold(self):
        for record in self:
            if not record.state == 'cancelled':
                record.state = 'sold'
            else:
                raise exceptions.UserError(
                    "Canceled properties cannot be sold.")
        return True

    def action_status_cancel(self):
        for record in self:
            if not record.state == 'sold':
                record.state = 'cancelled'
            else:
                raise exceptions.UserError(
                    "Sold properties cannot be cancelled.")
        return True

    # SQL constraints are more efficient than python constraints
    # try to stick with SQL when performance matters
    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if tools.float_compare(record.offer_ids.price,
                                   (record.expected_price * 9) / 10,
                                   precision_digits=2) == -1:
                raise exceptions.ValidationError("""The selling price must be
                    90% of the expected price! You must reduce the expected
                    price if you want to accept this offer.""")

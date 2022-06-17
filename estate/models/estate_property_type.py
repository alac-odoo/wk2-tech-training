# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The type of building the property is."
    _order = "sequence, name"

    name = fields.Char(required=True)
    description = fields.Text()
    property_ids = fields.One2many("estate.property",
                                   "property_type_id",
                                   string="Title")

    offer_ids = fields.One2many("estate.property.offer",
                                "property_type_id",
                                string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    sequence = fields.Integer(string="Sequence", default=1,
                              help="Order the property types manually.")

    _sql_constraints = [('unique_type',
                         'unique (name)',
                         'This type of property already exists.')]

    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

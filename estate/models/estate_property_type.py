# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The type of building the property is."

    name = fields.Char(required=True)
    description = fields.Text()

    _sql_constraints = [('unique_type',
                         'unique (name)',
                         'This type of property already exists.')]

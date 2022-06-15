# -*- coding: utf-8 -*-

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Extraneous features associated with the property"

    name = fields.Char(required=True)
    description = fields.Text()

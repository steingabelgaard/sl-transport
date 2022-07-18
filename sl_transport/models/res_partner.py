# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    bus_stop_isport = fields.Boolean(string='Bus stop is a Port',)
    webtour_tourpoint_xml = fields.Char(string='Tour point XML')

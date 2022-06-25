# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class EventSubcamp(models.Model):
    _inherit = 'event.subcamp'

    transport_busstop_id = fields.Many2one("res.partner", "Closest Bus Stop",domain=[('bus_stop_number', '>', 0)])
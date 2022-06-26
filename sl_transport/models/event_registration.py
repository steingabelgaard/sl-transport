# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class EventRegistration(models.Model):
    _inherit = 'event.registration'

    transport_ticket_in_id = fields.Many2one("transport.ticket", "Ticket to Camp",domain=[('ticket_type', '=', "in")])
    transport_ticket_out_id = fields.Many2one("transport.ticket", "Ticket From Camp",domain=[('ticket_type', '=', "out")])
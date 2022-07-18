# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
from os.path import join as opj

from odoo import api, fields, models, tools

class TransportTicketView(models.Model):

    _name = "transport.ticket.view"
    _description = "SL Transport Ticket Sum"
    _auto = False

    name = fields.Char()
    ticket_type = fields.Char(string="Ticket type")
    registration_id = fields.Many2one("event.registration", "Registration",domain=['&',('state','=','open'),'|',('event_id', '=', 9),('event_id', '=', 11)])
    webtour_tour_id = fields.Many2one("transport.webtourtour", "Webtour Tour")
    from_rp_id = fields.Many2one("res.partner", string='From stop')
    to_rp_id = fields.Many2one("res.partner", string='To stop')
    note = fields.Char(string="Note")
    etd = fields.Datetime(string='ETD')
    eta = fields.Datetime(string='ETA')
    pax = fields.Integer(string="PAX")

    @api.model_cr
    def init(self):
        script = opj(os.path.dirname(__file__), "transport_ticket_view.sql")
        with open(script) as f:
            tools.drop_view_if_exists(self._cr, self._table)
            self.env.cr.execute(f.read())

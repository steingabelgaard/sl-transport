# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
from os.path import join as opj

from odoo import api, fields, models, tools

class TransportTicket(models.Model):

    _name = "transport.ticket"
    _description = "SL Transport Ticket"
    _auto = True

    name = fields.Char()
    ticket_type = fields.Selection([("in","To Camp"),("out","From Camp"),("extra","Extra"),])
    registration_id = fields.Many2one("event.registration", "Master Registration",domain=['&',('state','=','open'),'|',('event_id', '=', 9),('event_id', '=', 11)])
    webtour_tour_id = fields.Many2one("transport.webtourtour", "Webtour Tour")
 

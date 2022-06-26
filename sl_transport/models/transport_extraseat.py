# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
from os.path import join as opj

from odoo import api, fields, models, tools

class TransportExtraSeat(models.Model):

    _name = "transport.extraseat"
    _description = "SL Transport Extra Seat"
    _auto = True

    name = fields.Char()
    master_id = fields.Many2one("event.registration", "Master Registration",domain=[('event_id', '=', 9)])
    in_date = fields.Date()
    out_date = fields.Date()
    in_transport = fields.Selection([(None,"Ingen"),("in_camp","in_camp"),])
    out_transport = fields.Selection([(None,"Ingen"),("out_camp","out_camp"),])
    transport_in_from_id = fields.Many2one("res.partner", "In From Stop",domain=[('bus_stop_number', '>', 0)])
    transport_out_to_id = fields.Many2one("res.partner", "Out To Stop",domain=[('bus_stop_number', '>', 0)])
    arrival_time = fields.Char()
    departure_time = fields.Char()
    arrival_flight = fields.Char()
    departure_flight = fields.Char()

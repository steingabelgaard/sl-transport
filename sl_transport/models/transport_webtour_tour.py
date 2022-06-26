# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
from os.path import join as opj

from odoo import api, fields, models, tools

class TransportWebtourtour(models.Model):
    _name = "transport.webtourtour"
    _description = "SL Transport Webtour Tour"
    _auto = True

    name = fields.Char()
    day = fields.Date("Day")
    needed_pax = fields.Integer("Needed PAX") 
    from_rp_id = fields.Many2one("res.partner", "From Bus Stop",domain=[('bus_stop_number', '>', 0)])
    to_rp_id = fields.Many2one("res.partner", "To Bus Stop",domain=[('bus_stop_number', '>', 0)])
    depart_after = fields.Char("Depart After")
    arrive_before = fields.Char("Arrive Before")
    webtour_tourid = fields.Char("Tour Id")
    webtour_pax = fields.Integer("Tour PAX")
    webtour_etd = fields.Datetime("Tour ETD")
    webtour_eta = fields.Datetime("Tour ETA")
    webtour_note = fields.Char("Tour Note")
    webtour_xml = fields.Char("Tour XML")
    webtour_lastupdate = fields.Datetime("Webtour last update")

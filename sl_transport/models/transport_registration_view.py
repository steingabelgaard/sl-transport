# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
from os.path import join as opj

from odoo import api, fields, models, tools

class EventRegistration(models.Model):
    _inherit = 'event.registration'

class TransportRegistrationView(models.Model):

    _name = "transport.registration.view"
    _description = "SL Transport Registration View"
    _auto = False

    name = fields.Char()
    master_id = fields.Many2one("event.registration", "Master Registration")
    partner_id = fields.Many2one("res.partner", "Customer")
    country_id = fields.Many2one("res.country", "Country")
    event_id = fields.Many2one("event.event", "Event")
    in_transport = fields.Char()
    out_transport = fields.Char()
    transport_in_from_id = fields.Many2one("res.partner", "In From Stop")
    transport_out_to_id = fields.Many2one("res.partner", "Out To Stop")
    arrival_time = fields.Char()
    departure_time = fields.Char()
    arrival_flight = fields.Char()
    departure_flight = fields.Char()
    in_date = fields.Date()
    out_date = fields.Date()

    @api.model_cr
    def init(self):
        script = opj(os.path.dirname(__file__), "transport_registration_view.sql")
        with open(script) as f:
            tools.drop_view_if_exists(self._cr, self._table)
            self.env.cr.execute(f.read())

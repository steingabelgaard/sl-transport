# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
from os.path import join as opj

from odoo import api, fields, models, tools


class TransportRegistrationView(models.Model):

    _name = "transport.registration.view"
    _description = "SL Transport Registration View"
    _auto = False

    name = fields.Char()
    participant_id = fields.Many2one("event.registration", "Participant")
    camp_day_id = fields.Many2one("event.question.option", "Lejrdøgn")
    registration_master_id = fields.Many2one(
        "event.registration", "Master registration"
    )
    subcamp_id = fields.Many2one("event.subcamp", string="Subcamp")
    subcamp_area_id = fields.Many2one("event.subcamp.area", string="Subcamp area")
    scout_organization = fields.Char("National association/organization")
    master_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("moved", "Moved"),
            ("manual", "Requires approval"),
            ("waitinglist", "Waiting list"),
            ("open", "Confirmed"),
            ("done", "Attended"),
            ("notdone", "Not completed"),
            ("cancel", "Unregistered"),
            ("noshow", "No show"),
            ("annul", "Annulled"),
        ],
        string="Master Status",
    )
    participant_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("moved", "Moved"),
            ("manual", "Requires approval"),
            ("waitinglist", "Waiting list"),
            ("open", "Confirmed"),
            ("done", "Attended"),
            ("notdone", "Not completed"),
            ("cancel", "Unregistered"),
            ("noshow", "No show"),
            ("annul", "Annulled"),
        ],
        string="Participant Status",
    )

    @api.model_cr
    def init(self):
        script = opj(os.path.dirname(__file__), "transport_registration_view.sql")
        with open(script) as f:
            tools.drop_view_if_exists(self._cr, self._table)
            self.env.cr.execute(f.read())

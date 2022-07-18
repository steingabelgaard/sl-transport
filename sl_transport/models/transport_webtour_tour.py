# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
from os.path import join as opj

from odoo import api, fields, models, tools
from odoo.addons.queue_job.job import job

from ..interface import webtourinterface
from collections import OrderedDict

import logging
_logger = logging.getLogger(__name__)

class TransportWebtourtour(models.Model):
    _name = "transport.webtourtour"
    _description = "SL Transport Webtour Tour"
    _auto = True

    name = fields.Char()
    day = fields.Date("Day")
    needed_pax = fields.Integer("Needed PAX", compute ='_compute_ticket_count')
    from_rp_id = fields.Many2one("res.partner", "From Bus Stop",domain=[('bus_stop_number', '>', 0)])
    to_rp_id = fields.Many2one("res.partner", "To Bus Stop",domain=[('bus_stop_number', '>', 0)])
    depart_after = fields.Char("Depart After")
    arrive_before = fields.Char("Arrive Before")
    note = fields.Char("Note")
    webtour_tourid = fields.Char("Tour Id")
    webtour_pax = fields.Integer("Tour PAX")
    webtour_etd = fields.Datetime("Tour ETD")
    webtour_eta = fields.Datetime("Tour ETA")
    webtour_note = fields.Char("Tour Note")
    webtour_xml = fields.Char("Tour XML")
    webtour_lastupdate = fields.Datetime("Webtour last update")
    tickets_id = fields.One2many("transport.ticket","webtour_tour_id","Tickets",ondelete='restricted')

    def _compute_ticket_count(self):
        for rec in self:
            rec.needed_pax = self.env['transport.ticket'].search_count([['webtour_tour_id','=',rec.id]]) - rec.webtour_pax

    @api.multi
    @job(default_channel="root")
    def updatewebtourtourjob(self):
        _logger.info('Here we go updatewebtourtourjob')
        for tour in self:
            _logger.info(tour.name)
        #raise Warning("Doit")

    @api.multi
    def updatewebtourtour(self):
        _logger.info('Here we go updatewebtourtour')

     #   _logger.info(webtourinterface.login())
     #   res = webtourinterface.tour_GetFromLastUpdated('2022-07-06T00:00:00.00000+02:00')
     #   _logger.info(res)
     #   _logger.info(self)
        for tour in self:
            _logger.info(tour.name)
"""
            _logger.info(tour.webtour_tourid)
            _logger.info(tour.from_rp_id.name)
            _logger.info(tour.to_rp_id.name)
            if ((tour.webtour_tourid is False) and (not tour.webtour_etd is False) and (not tour.webtour_eta is False)):
                webtour = webtourinterface.tour_Create(tour.name,str(tour.webtour_pax+tour.needed_pax),tour.webtour_etd,tour.webtour_eta)
                tourid = webtour['a:Content']['b:TourIDno']
                _logger.info(tourid)
                tour.webtour_tourid=tourid
                
                cus = webtourinterface.Customer_GetFromSearchPattern('42438838')
                cusres = webtourinterface.tour_SetCustomer(tourid,cus['a:Content']['b:Customers']['b:CustomerItem'])
                
                if tour.from_rp_id.webtour_tourpoint_xml is False and not(tour.from_rp_id.webtour_tourpoint_xml == ''):
                    a = tour.from_rp_id
                    if (a.street2 is False):
                        tp1res = webtourinterface.tourPoint_CreateFromAddressWithLatLong(a.name,a.street,a.zip,a.city,'DK',str(a.partner_latitude).replace('.','.'),str(a.partner_longitude).replace('.','.'))
                    else :
                        tp1res = webtourinterface.tourPoint_CreateFromAddress2WithLatLong(a.name,a.street,a.street2,a.zip,a.city,'DK',str(a.partner_latitude).replace('.','.'),str(a.partner_longitude).replace('.','.'))
                    tour.from_rp_id.webtour_tourpoint_xml = tp1res
                
                tp = dict(eval(tour.from_rp_id.webtour_tourpoint_xml))

                res2 = webtourinterface.tour_SetLocation_NewTourPoint('StartLocation',tourid,tp)

                if tour.to_rp_id.webtour_tourpoint_xml is False and not(tour.to_rp_id.webtour_tourpoint_xml == ''):
                    a = tour.to_rp_id
                    if (a.street2 is False):
                        tp2res = webtourinterface.tourPoint_CreateFromAddressWithLatLong(a.name,a.street,a.zip,a.city,'DK',str(a.partner_latitude).replace('.','.'),str(a.partner_longitude).replace('.','.'))
                    else :
                        tp2res = webtourinterface.tourPoint_CreateFromAddress2WithLatLong(a.name,a.street,a.street2,a.zip,a.city,'DK',str(a.partner_latitude).replace('.','.'),str(a.partner_longitude).replace('.','.'))
                    tour.to_rp_id.webtour_tourpoint_xml = tp2res
                
                tp2 = dict(eval(tour.to_rp_id.webtour_tourpoint_xml))
                res2 = webtourinterface.tour_SetLocation_NewTourPoint('EndLocation',tourid,tp2)

            if (tour.webtour_tourid is not False):
                if tour.needed_pax:
                    webtourinterface.tour_SetNoPersons(tour.webtour_tourid, str(tour.webtour_pax+tour.needed_pax))
                
                tourdict = webtourinterface.tour_Get(tour.webtour_tourid)
                tour.webtour_pax = tourdict['a:Content']['b:NoPersons']
                _logger.info(tourdict)
                #tour.webtour_xml = 
"""
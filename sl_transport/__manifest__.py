# Copyright 2022 Stein & Gabelgaard ApS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sl Transport',
    'description': """
        SL2022 Transport interface""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Jesper Darum,Stein & Gabelgaard ApS',
    'website': 'www.steingabelgaard.dk',
    'application':True,
    'depends': ["sl2022"],
    'data': [   "security/transport_registration_view.xml",
                "security/transport_webtourtour.xml",
                "security/transport_ticket.xml",
                "views/sl_transportation_view.xml",
                "views/event_registration_view.xml",
                "views/res_partner_view.xml"],
    'demo': [
    ],
}

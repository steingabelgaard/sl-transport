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
    'depends': ["sg_member_event"],
    'data': [ "security/transport_registration_view.xml"],
    'demo': [
    ],
}

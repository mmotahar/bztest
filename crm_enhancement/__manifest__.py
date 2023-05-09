{
    "category": "CRM Customization",
    "name": "CRM Customization",
    "license": "AGPL-3",
    "author": "WaoConnect",
    "sequence": 1,
    "summary": "CRM Customization",
    "application": True,
    "depends": ['crm', 'sale_crm','mail'],
    "version": "15.11",
    "auto_install": False,
    "data": ['security/ir.model.access.csv', 'views/main_concern.xml', 'views/matter_type.xml', 'views/crm_lead.xml', 'views/res_partner.xml'],
    "installable": True,
}

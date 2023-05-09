{
    "category": "Biztech Customization",
    "name": "Biztech Customization",
    "license": "AGPL-3",
    "author": "WaoConnect",
    "sequence": 1,
    "demo": [],
    "summary": "Biztech Customization",
    "application": True,
    "depends": ['sale_timesheet', 'hr_timesheet', 'web', 'mail'],
    "version": "15.56",
    "auto_install": False,
    "data": [
        'views/sale_config_settings.xml',
        'data/mail_template.xml',
        'data/so_email_templates.xml',
        'views/account_analytic_line.xml',
        'views/sale_order.xml',
        'views/account_move.xml',
        'report/inherit_invoice_final.xml',
        'report/report_header_footer.xml'
    ],
    'assets': {
        'web.assets_qweb': [
            'biztech_customiztion/static/src/components/chatter_topbar/chatter_topbar.xml'
        ],
    },
    "installable": True,
}

{
    "name": "Invoice Reports",
    "summary": "Invoice Reports",
    "version": "15.0.0.58",
    "maintainers": ["WAO"],
    "category": "Accounting",
    "website": "http://www.waoconnect.com",
    "author": "WAO",
    "depends": ['web','account'],
    "data": [
        "views/views.xml",
        "reports/tax_invoice.xml",
        "reports/reports.xml",
        "reports/report_invoice_document_inh.xml",
    ],
    "application": False,
    'auto_install': False,
    "installable": True
}
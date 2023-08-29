

{
    "name": "Generate Barcodes (Abstract)",
    "summary": "Generate Barcodes for Any Models",
    "version": "16.0.3.0.1",
    "category": "Tools",
    "author": "GRAP, La Louve, LasLabs, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/stock-logistics-barcode",
    "license": "AGPL-3",
    "depends": ["barcodes"],
    "data": [
        "security/res_groups.xml",
        "views/view_barcode_rule.xml",
        "views/view_barcode_nomenclature.xml",
        "views/menu.xml",
    ],
    "demo": ["demo/res_users.xml"],
    "external_dependencies": {"python": ["barcode"]},
}

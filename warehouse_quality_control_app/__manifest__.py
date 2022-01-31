# -*- coding: utf-8 -*-
{
    'name': 'Inventory Quality Control Management in Odoo',
    "author": "Edge Technologies",
    'version': '12.0.1.0',
    'live_test_url': "https://youtu.be/1VgJKTJCx5U",
    "images":['static/description/main_screenshot.png'],
    'summary': " Quality Control (QC) management for Warehouse.",
    'description': """ This app help to user for Quality Control like Quality Check and Quality Alert for Warehouse. Also Generate Quality Check and Alert Report. 
   
Quality Control Inspections
Internal Validation and Verification
QC features of warehouse management
QC warehouse management
QA warehouse management
WMS QUALITY ASSURANCE
Quality control
WMS Quality assurance
QUALITY CONTROL WMS
Inventory Control and Quality Control
Inventory Quality Control
Quality Control Inventory 
Quality Control Management
Inventory control
warehouse quality control
 Inventory Management 
 Stock Control and Inventory Management
 warehouse quality control
 Warehouse Performance Management
 Improve Quality and Productivity in Warehouse Operations
 Warehouse Operations - Quality Inspection
 Quality Inspection
 Quality Systems Warehouse Management
 Quality Assurance
 quality management
 Quality Management in Warehouse Management
 stock control
 inventory cost management
 multiple location support
 Inventory control systems
Purchase Product Quality Instpection
Quality alerts and Quality Inspections
incoming Product Quality Instpection
inventory inspection
shipment inspection
Pre-shipment inspection
shipment inspection
Pre Shipment Inspection

quality control inspections 
product quality control inspections 
wms quality control inspections 
warehouse quality control inspections 
Quality Control and Preshipment Inspection
Warehouse quality audit checklist
Quality Management
purchase quality control management
picking quality control management
delivery quality control management
incoming shipment quanlity control management
quality control team
quality control alerts
quality control points
purchase quality Inspection management
picking quality Inspection management
delivery quality Inspection management
incoming shipment quanlity Inspection management
quality Inspection team
quality Inspection alerts
quality Inspection points
warehouse QC control qc Control team purchase qc management warehouse qc management picking qc management




    """,
    "license" : "OPL-1",
    'depends': ['base','sale_management','stock','purchase','account'],
    'data': [
            
            'security/ir.model.access.csv',
            'wizard/wizard_views.xml',
            'views/quality_point.xml',
            'views/picking_inherit.xml',
            'views/quality_team_viewe.xml',
            'views/quality_alert_view.xml',
            'report/check_quality_reports.xml'
            ],
    'installable': True,
    'auto_install': False,
    'price': 75,
    'currency': "EUR",
    'category': 'Warehouse',

}


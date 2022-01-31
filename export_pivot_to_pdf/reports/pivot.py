from odoo import api, fields, models
from odoo.exceptions import ValidationError



class Pivot(models.AbstractModel):
    _name = 'report.export_pivot_to_pdf.pivot_report'
    @api.model
    def _get_report_values(self, docids, data=None):
        report_name = data.get('display_name')
        docargs = {
            'table_data':data.get('data'),
            "report_name":report_name
        }
        return docargs



class PivotReport(models.Model):
    _name='pivot.print'

    @api.model
    def call_pdf(self,data="",model_name="",display_name=""):
        print(">>>",data)
        data={'data':data,'model_name':model_name,'display_name':display_name}
        return self.env.ref('export_pivot_to_pdf.action_report_pivot_pdf').report_action(self, data=data,config=False)


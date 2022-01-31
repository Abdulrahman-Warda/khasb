from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    @api.model
    def get_html(self, bom_id=False, searchQty=1, searchVariant=False):
        res = self._get_report_data(bom_id=bom_id, searchQty=searchQty, searchVariant=searchVariant)
        res['lines']['report_type'] = 'html'
        res['lines']['report_structure'] = 'all'
        res['lines']['has_attachments'] = res['lines']['attachments'] or any(
            component['attachments'] for component in res['lines']['components'])
        labours=self.get_labours(bom_id)
        print("data",res['lines'])
        res['lines'] = self.env.ref('mrp.report_mrp_bom').render({'data': res['lines'],'labours':labours})
        return res



    def get_labours(self,bom_id):
        labours=[]
        bom_id=self.env[
            'mrp.bom'
        ].browse(bom_id)
        for lab in bom_id.bom_labour_cost_ids:
            labours.append({
                'cost':lab.cost
            })
        return labours




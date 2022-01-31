from odoo import api, fields, models



class AssignEmployees(models.TransientModel):
    _name='project.assign.employees'

    def get_domain(self):
        employe_ids = []
        res = self.env['project.project'].browse(self._context.get('active_ids'))
        for project in res:
            for employee in project.employe_ids.ids:
                employe_ids.append(employee)
        return [(4,id) for id in employe_ids]



    selected_employe_ids = fields.Many2many(comodel_name="hr.employee",default=get_domain)
    employe_ids = fields.Many2many(comodel_name="hr.employee",domain=get_domain)


    @api.onchange('selected_employe_ids')
    def onchange_selected_employe_ids(self):
        print ("DDDDDDDDDDDDDdd")
        domain = [('id', 'not in', self.selected_employe_ids.ids)]
        return {
                'domain': {'employe_ids': domain}
            }


    def assign(self):
        res=self.env['project.project'].browse(self._context.get('active_ids'))
        employe_ids=self.employe_ids.ids
        for project in res:
            project.employe_ids=[(4,id) for id in employe_ids]

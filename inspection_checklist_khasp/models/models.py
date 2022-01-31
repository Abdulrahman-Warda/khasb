# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RepairRequest(models.Model):
    _name = 'inspection.checklist'

    # model's fields
    building = fields.Char(string="Building")
    foa = fields.Char(string="FOA")
    location = fields.Char(string="Location")
    supervisor_name = fields.Char(string="Supervisor Name")
    supervisor_signature = fields.Char(string="Supervisor Signature")
    manager_name = fields.Char(string="Manager Name")
    manager_signature = fields.Char(string="Manager Signature")
    employee_name = fields.Char(string="Employee Name")
    employee_signature = fields.Char(string="Employee Signature")

    area = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Area is tidy and well kept')

    comment1 = fields.Text()

    adequate = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Adequate storage area provided')

    comment2 = fields.Text()

    floor = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Floor is free of obstructions and not-slippery')

    comment3 = fields.Text()

    opening = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Any opening in the floor are guarded or covered')

    comment4 = fields.Text()

    walkways = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Walkways clearly marked and guarded if necessary ')

    comment5 = fields.Text()
    action1 = fields.Text(string="Action")

    temp = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Temperature is comfortable')

    comment6 = fields.Text()

    lighting = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Lighting is adequate')

    comment7 = fields.Text()

    fittings = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Lighting covers and fittings are secure')

    comment8 = fields.Text()

    odours = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Area is free from odours ')

    comment9 = fields.Text()

    noise = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Noise level is acceptable/adequately controlled')

    comment10 = fields.Text()

    ventilation = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Ventilation is adequate')

    comment11 = fields.Text()
    action2 = fields.Text(string="Action")

    procedures = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Written procedures posted')

    comment12 = fields.Text()

    extinguisher = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Extinguisher of appropriate type easily accessible')

    comment13 = fields.Text()

    visitor = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Visitor Emergency Guides are available (where required)')

    comment14 = fields.Text()

    alarm = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Alarm can be heard in the area (if applicable)')

    comment15 = fields.Text()

    escape = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Escape routes are clear')

    comment16 = fields.Text()

    emergency = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Emergency and hazard signage is clearly visible')

    comment17 = fields.Text()

    evacuation = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Evacuation drills carried out')

    comment18 = fields.Text()
    action3 = fields.Text(string="Action")

    kits = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Kits accessible within 5 minutes')

    comment19 = fields.Text()

    stocked = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Kits are stocked and contents are in-date ')

    comment20 = fields.Text()

    contacts = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Names and contacts of first aiders displayed ')

    comment21 = fields.Text()
    action4 = fields.Text(string="Action")

    washing = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Washing facilities are clean and functional ')

    comment22 = fields.Text()

    lockers = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Lockers or equivalent available for staff')

    comment23 = fields.Text()

    eating_areas = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Eating areas clean, hygienic and adequately serviced ')

    comment24 = fields.Text()
    action5 = fields.Text(string="Action")

    equipment = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Portable equipment has current test tags')

    comment25 = fields.Text()

    power_leads = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Power leads in good condition ')

    comment26 = fields.Text()

    power_leads2 = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Power leads are off the floor or placed away from walkways')

    comment27 = fields.Text()

    power_boards = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Power boards used (not double adaptors) ')

    comment28 = fields.Text()

    faulty_equipment = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Faulty equipment is tagged out ')

    comment29 = fields.Text()
    action6 = fields.Text(string="Action")

    warning = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Warning and safety signage in good condition')

    comment30 = fields.Text()

    plant = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Procedure, plant and equipment manuals are current and available')

    comment31 = fields.Text()

    workshop = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Workshop free of food and drink ')

    comment32 = fields.Text()
    action7 = fields.Text(string="Action")

    waste_containers = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Waste containers are provided and labelled with Class Diamonds')

    comment33 = fields.Text()

    segregated = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Waste is segregated and stored appropriately away from drains')

    comment34 = fields.Text()

    spill_kits = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Spill kits are available ')

    comment35 = fields.Text()
    action8 = fields.Text(string="Action")

    correctly_stored = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Correctly stored ')

    comment36 = fields.Text()

    well_maintained = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Well maintained and in good condition ')

    comment37 = fields.Text()

    signage = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Signage of PPE requirements displayed ')

    comment38 = fields.Text()

    required_ppe = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Required PPE available')

    comment39 = fields.Text()
    action9 = fields.Text(string="Action")

    ventilation = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Ventilation is adequate for spray painting operations')

    comment40 = fields.Text()

    respiratory_equipment = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Respiratory equipment is maintained')

    comment41 = fields.Text()

    paint = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Paint and thinners labelled')

    comment42 = fields.Text()

    thinners = fields.Selection([
        ('y', 'Y'),
        ('n', 'N'),
        ('na', 'NA')], string='Paint and thinners stored correctly, bunded and segregated from drains')

    comment43 = fields.Text()

    action10 = fields.Text(string="Action")

    other_comments = fields.Text(string="Other Comments")

    recommendations = fields.Text(string="General Recommendations")



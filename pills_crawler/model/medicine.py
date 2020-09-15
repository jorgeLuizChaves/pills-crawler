from marshmallow import Schema, fields


class Medicine(Schema):
    name = fields.Str()
    company_name = fields.Str()
    publish_date = fields.Date()
    expedient_number = fields.Str()
    anvisa_id = fields.Str()
    leaflet_patient_id = fields.Str()
    leaftlet_professional_id = fields.Str()

import unittest
import jsonschema
import json
from xlsx2json import xlsx2json

SCHEMA_PATH = "data/invoices_schema.json"
XLSX_PATH = "data/Ejemplo Excel.xlsx"


class TestSchemaConformity(unittest.TestCase):

    def test_schema(self):
        with open(SCHEMA_PATH, "rb") as s:
            schema = json.load(s)
            out_json = xlsx2json(XLSX_PATH)
            out_obj = json.loads(out_json)
            jsonschema.validate(out_obj, schema)

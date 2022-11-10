import xlrd
import pandas as pd
from datetime import datetime

XLSX_PATH = "Ejemplo Excel.xlsx"


def xlsx2json(path, sheet=0, skip=1):
    """
    Convierte una hoja de excel a json

    :param sheet int: Número de hoja en la que se encuentran los datos 
    :param skip int: Número de filas que va a ignorar antes de procesar los datos 
    """
    # NOTA: La lectura de XLSX se considera una vulnerabilidad en xlrd >= 2.0
    # Más información al respecto aquí
    # https://groups.google.com/g/python-excel/c/IRa8IWq_4zk/m/Af8-hrRnAgAJ?pli=1
    # Sin embargo, la rama de odoo vauxoo/13.0 utiliza xlrd == '1.1.0'
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(sheet)

    for row_idx in range(skip, sheet.nrows):
        cell = sheet.cell(row_idx, 1)
        cell.ctype = 3
        #  print(cell.value)


def xlsx2jsonPandas(path):
    fields = ["purchase_order_id.partner_ref",
              "invoice_line_ids.name",
              "check_in_date",
              "max_cancel_date",
              "purchase_order_id.price_unit",
              "currency_id",
              "invoice_line_ids.price_unit",
              "purchase_order_id.currency_id",
              "ref",
              "purchase_order_id.partner_id",
              "partner_id.ref",
              "partner_id.name",
              "partner_id.vat",
              "journal_id",
              "partner_id.country_id",
              "invoice_date",
              "company_id",
              "invoice_line_ids.product_id",
              "is_refundable"]

    def get_date(s): return datetime.strptime(s, "%d/%m/%Y")
    workbook = pd.read_excel(path,
                             # Usar solo las columnas que nos interesan
                             usecols=[0, 2, 3, 5, 6, 7, 8, 9, 10,
                                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                             # Usar los nombres del modelo
                             names=fields)

    pd.set_option('display.max_columns', None)
    print(workbook)
    workbook["purchase_order_id"] = workbook.apply(lambda row: {
        "partner_ref": row["purchase_order_id.partner_ref"],
        "price_unit": row["purchase_order_id.price_unit"],
        "partner_id": row["purchase_order_id.partner_id"]
    }, axis=1)

    workbook.drop(["purchase_order_id.partner_ref",
                   "purchase_order_id.price_unit",
                   "purchase_order_id.partner_id"], axis=1, inplace=True)

    workbook["invoice_line_ids"] = workbook.apply(lambda row: [{
        "name": row["invoice_line_ids.name"],
        "price_unit": row["invoice_line_ids.price_unit"],
        "product_id": row["invoice_line_ids.product_id"],
    }], axis=1)

    workbook.drop(["invoice_line_ids.name",
                   "invoice_line_ids.price_unit",
                   "invoice_line_ids.product_id"], axis=1, inplace=True)

    workbook["partner_id"] = workbook.apply(lambda row: {
        "ref": row["partner_id.ref"],
        "name": row["partner_id.name"],
        "country_id": row["partner_id.country_id"],
    }, axis=1)

    workbook.drop([
        "partner_id.ref",
        "partner_id.name",
        "partner_id.country_id"
    ], axis=1, inplace=True)

    #  for record in workbook.to_dict():
    #  print(workbook.to_json(orient="records"))

    #  print(workbook["check_in_date"])
    # Forzar tipos de datos
    # NOTA: Aquí no podemos usar un strformat por que los tipos de datos están combinados para esta columna, pero
    # sí podemos pedirle a pandas que infiera la fecha.
    #  print(workbook["invoice_date"])


if __name__ == "__main__":

    xlsx2jsonPandas(XLSX_PATH)

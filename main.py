import pandas as pd
import dateutil
from dateutil.parser import ParserError
import sys
import json
import os
from datetime import datetime
import argparse

XLSX_PATH = "Ejemplo Excel.xlsx"


def warning(s):
    print(f"WARNING: {s}", file=sys.stderr)


def error(s):
    print(f"ERROR: {s}", file=sys.stderr)
    sys.exit(-1)


def check_date(s):
    """Intenta hacer parse una fecha y emite un warning
    o detiene el programa completamente si no se puede 
    acoplar al formato esperado"""
    OUT_FORMAT = "%Y-%m-%d"

    if 'datetime.datetime' in str(type(s)):
        return s.strftime(OUT_FORMAT)
    elif "str" in str(type(s)):
        warning(
            f"El objeto {s} no es una fecha en Excel. "
            "Intentando interpretar como fecha")
        # Tratar de interpretar rígidamente en formato "%d/%m/%Y"
        try:
            date = datetime.strptime(s, "%d/%m/%Y")
            return date.strftime(OUT_FORMAT)
        except ValueError:
            warning(
                f"El objeto {s} no pudo ser interpredado en el formato dd/mm/YYYY")
        try:
            warning(f"Haciendo un intento final de interpretar {s}")
            date = dateutil.parser.parse(s)
            return date.strftime(OUT_FORMAT)
        except ParserError:
            error(
                f"Imposible determinar una fecha de {s}. Deteniendo proceso.")
            pass
    else:
        error(f"Un objeto de tipo {type(s)} no es interpretable como fecha")


def xlsx2json(path):
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

    workbook = pd.read_excel(path,
                             # Usar solo las columnas que nos interesan
                             usecols=[0, 2, 3, 5, 6, 7, 8, 9, 10,
                                      11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                             # Usar los nombres del modelo
                             names=fields, parse_dates=False,
                             converters={
                                 "check_in_date": check_date,
                                 "invoice_date": check_date,
                                 "max_cancel_date": check_date})

    #  pd.set_option('display.max_columns', None)
    #  print(workbook)
    workbook["purchase_order_id"] = workbook.apply(lambda row: {
        "partner_ref": row["purchase_order_id.partner_ref"],
        "currency_id": row["purchase_order_id.currency_id"],
        "price_unit": row["purchase_order_id.price_unit"],
        "partner_id": row["purchase_order_id.partner_id"]
    }, axis=1)

    workbook.drop(["purchase_order_id.partner_ref",
                   "purchase_order_id.currency_id",
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

    data = workbook.to_dict(orient="records")
    object_count = len(data)
    # La última modificación del archivo
    last_mod_epoch = os.path.getmtime(path)
    timestamp = datetime.fromtimestamp(last_mod_epoch)
    return json.dumps({
        "date": timestamp.isoformat(),
        "object_count": object_count,
        "data": data
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="xlsx2json",
        description="Convierte un archivo .xlsx a json")
    parser.add_argument('FILE')
    parser.add_argument(
        '-o', "--output", help="Nombre de archivo de salida. STDOUT por default")
    namespace = parser.parse_args()
    outfile_is_stdout = namespace.output is None
    try:

        outfile = sys.stdout if outfile_is_stdout else open(
            namespace.output, "w")
        with open(namespace.FILE, "rb") as xlsx:
            pass
    except FileNotFoundError:
        error(
            f"El archivo {namespace.FILE} no existe o no se tienen permisos para leerlo.")

    #  dump = xlsx2json(XLSX_PATH)
    #  print(dump)

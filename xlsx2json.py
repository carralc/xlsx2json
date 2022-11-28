#!/usr/bin/env python3
import pandas as pd
import dateutil
from dateutil.parser import ParserError
import sys
import json
import os
from datetime import datetime
from collections import OrderedDict
import argparse


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
            # Hacer el mejor esfuerzo por interpretarlo, aún cuando no se ajusta
            # a la entrada esperada.
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
              "is_refundable",
              "l10n_mx_edi_payment_method_id"]

    workbook = pd.read_excel(path,
                             # Usar solo las columnas que nos interesan
                             usecols=[0, 2, 3, 5, 6, 7, 8, 9, 10,
                                      11, 12, 13, 14, 15, 16, 17,
                                      18, 19, 20, 21],
                             # Usar los nombres del modelo
                             names=fields, parse_dates=False,
                             converters={
                                 "check_in_date": check_date,
                                 "invoice_date": check_date,
                                 "max_cancel_date": check_date})

    workbook["type"] = "out_invoice"

    workbook["invoice_date_due"] = workbook["invoice_date"]

    workbook["multicurrency"] = workbook.apply(lambda row: {
        "currency": row["currency_id"],
        "currency_amount": row["invoice_line_ids.price_unit"],
        "rate": 0,
        "conversion_value": row["invoice_line_ids.price_unit"],
        "comission_fixed": 0
    }, axis=1)

    workbook["purchase_order_id"] = workbook.apply(lambda row: {
        "partner_id": row["purchase_order_id.partner_id"],
        "partner_ref": row["purchase_order_id.partner_ref"],
        "price_unit": row["purchase_order_id.price_unit"],
        "currency_id": row["purchase_order_id.currency_id"],
        "date_order": row["invoice_date"],
        "due_date": row["check_in_date"]
    }, axis=1)

    workbook.drop(["purchase_order_id.partner_ref",
                   "purchase_order_id.currency_id",
                   "purchase_order_id.price_unit",
                   "purchase_order_id.partner_id"], axis=1, inplace=True)

    workbook["invoice_line_ids"] = workbook.apply(lambda row: [{
        "product_id": row["invoice_line_ids.product_id"],
        "name": row["invoice_line_ids.name"],
        "price_unit": row["invoice_line_ids.price_unit"],
        "sales_channel": row["partner_id.ref"]
    }], axis=1)

    workbook.drop(["invoice_line_ids.name",
                   "invoice_line_ids.price_unit",
                   "invoice_line_ids.product_id"], axis=1, inplace=True)

    workbook["partner_id"] = workbook.apply(lambda row: {
        "ref": row["partner_id.ref"],
        "name": row["partner_id.name"],
        "vat": row["partner_id.vat"],
        "country_id": row["partner_id.country_id"],
    }, axis=1)

    workbook.drop([
        "partner_id.ref",
        "partner_id.name",
        "partner_id.vat",
        "partner_id.country_id"
    ], axis=1, inplace=True)

    # Reordenar columnas
    workbook = workbook[["ref", "partner_id", "company_id",
                         "invoice_date", "currency_id",
                         "check_in_date", "is_refundable",
                         "max_cancel_date", "l10n_mx_edi_payment_method_id",
                         "type", "invoice_line_ids", "multicurrency",
                         "purchase_order_id", "journal_id",
                         "invoice_date_due"]]

    data = workbook.to_dict(orient="records", into=OrderedDict)
    object_count = len(data)
    # La última modificación del archivo
    last_mod_epoch = os.path.getmtime(path)
    timestamp = datetime.fromtimestamp(last_mod_epoch)
    metadata = {
        "date": timestamp.isoformat(),
        "object_count": object_count,
        "type": "invoices"
    }
    return json.dumps({
        "meta": metadata,
        "data": data
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="xlsx2json",
        description="Convierte un archivo .xlsx a json")
    parser.add_argument('file')
    parser.add_argument(
        '-o', "--output", help="Nombre de archivo de salida. STDOUT por default")
    namespace = parser.parse_args()
    outfile_is_stdout = namespace.output is None
    try:

        outfile = sys.stdout if outfile_is_stdout else open(
            namespace.output, "w")
        dump = xlsx2json(namespace.file)
        print(dump, file=outfile)
        if outfile_is_stdout:
            outfile.close()
    except FileNotFoundError:
        error(
            f"El archivo {namespace.file} no existe o no se tienen permisos para leerlo.")

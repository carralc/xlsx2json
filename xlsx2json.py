#!/usr/bin/env python3
import pandas as pd
import dateutil
from dateutil.parser import ParserError
import sys
import json
import os
from datetime import datetime
from collections import OrderedDict
import xlrd
import argparse

XLSX_PATH = "./Ejemplo Excel.xlsx"


def warning(s):
    print(f"WARNING: {s}", file=sys.stderr)


def error(s):
    print(f"ERROR: {s}", file=sys.stderr)
    sys.exit(-1)


def check_date(s):
    """Intenta hacer parse una fecha y emite un warning
    o detiene el programa completamente si no se puede
    acoplar al formato esperado"""

    try:
        date = datetime.strptime(s, "%d/%m/%Y")
        return date
    except ValueError:
        warning(
            f"El objeto {s} no pudo ser interpredado en el formato dd/mm/YYYY")
    try:
        warning(f"Haciendo un intento final de interpretar {s}")
        # Hacer el mejor esfuerzo por interpretarlo, aún cuando no se ajusta
        # a la entrada esperada.
        date = dateutil.parser.parse(s)
        return date
    except ParserError:
        error(
            f"Imposible determinar una fecha de {s}. Deteniendo proceso.")


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
              "l10n_mx_edi_payment_method_id",
              "invoice_line_ids.commission_id"]

    workbook = pd.read_excel(path,
                             # Usar solo las columnas que nos interesan
                             usecols=[0, 2, 3, 5, 6, 7, 8, 9, 10,
                                      11, 12, 13, 14, 15, 16, 17,
                                      18, 19, 20, 21, 22],
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
        "commission_id": row["invoice_line_ids.commission_id"],
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


def xlsx2jsonxlrd(path):
    book = xlrd.open_workbook(path)
    datemode = book.datemode
    sheet = book.sheet_by_index(0)

    data = [transform_row(sheet, row_idx, datemode)
            for row_idx in range(1, sheet.nrows)]

    # La última modificación del archivo
    last_mod_epoch = os.path.getmtime(path)
    timestamp = datetime.fromtimestamp(last_mod_epoch)
    metadata = {
        "date": timestamp.isoformat(),
        "object_count": len(data),
        "type": "invoices"
    }

    return json.dumps({
        "meta": metadata,
        "data": data
    })


def transform_row(sheet, row, datemode):
    PURCHASE_ORDER_ID_PARTNER_REF = 0
    INVOICE_LINE_IDS_NAME = 2
    CHECK_IN_DATE = 3
    MAX_CANCEL_DATE = 5
    PURCHASE_ORDER_ID_PRICE_UNIT = 6
    CURRENCY_ID = 7
    INVOICE_LINE_IDS_PRICE_UNIT = 8
    PURCHASE_ORDER_ID_CURRENCY_ID = 9
    REF = 10
    PURCHASE_ORDER_ID_PARTNER_ID = 11
    PARTNER_ID_REF = 12
    PARTNER_ID_NAME = 13
    PARTNER_ID_VAT = 14
    JOURNAL_ID = 15
    PARTNER_ID_COUNTRY_ID = 16
    INVOICE_DATE = 17
    COMPANY_ID = 18
    INVOICE_LINE_IDS_PRODUCT_ID = 19
    IS_REFUNDABLE = 20
    L10N_MX_EDI_PAYMENT_METHOD_ID = 21
    INVOICE_LINE_IDS_COMMISSION_ID = 22

    DATE_OUT_FORMAT = "%Y-%m-%d"

    out = {}

    out["ref"] = sheet.cell_value(row, REF)
    out["partner_id"] = {
        "ref": sheet.cell_value(row, PARTNER_ID_REF),
        "name": sheet.cell_value(row, PARTNER_ID_NAME),
        "vat": sheet.cell_value(row, PARTNER_ID_VAT),
        "country_id": sheet.cell_value(row, PARTNER_ID_COUNTRY_ID)
    }
    out["company_id"] = sheet.cell_value(row, COMPANY_ID)

    def get_date(cell_val):
        if "float" in str(type(cell_val)):
            # Tratar de interpretarlo como fecha de excel (float)
            try:
                invoice_date = xlrd.xldate_as_datetime(
                    cell_val, datemode)
                return invoice_date
            except Exception as e:
                print(e)
                error(
                    f"Campo de fecha mal formada en fila {row}, col {INVOICE_DATE}")
        elif "str" in str(type(cell_val)):
            # Tratar de interpretar como cadena
            invoice_date = check_date(cell_val)
            return invoice_date
        else:
            print(type(cell_val))
            error(
                f"Campo de fecha mal formada en fila {row}, col {INVOICE_DATE}")

    invoice_date_cell_val = sheet.cell_value(row, INVOICE_DATE)
    invoice_date = get_date(invoice_date_cell_val)
    out["invoice_date"] = invoice_date.strftime(DATE_OUT_FORMAT)

    out["currency_id"] = sheet.cell_value(row, CURRENCY_ID)

    check_in_date_cell_value = sheet.cell_value(row, CHECK_IN_DATE)
    check_in_date = get_date(check_in_date_cell_value)
    out["check_in_date"] = check_in_date.strftime(DATE_OUT_FORMAT)

    out["is_refundable"] = bool(sheet.cell_value(row, IS_REFUNDABLE))

    out["max_cancel_date"] = sheet.cell_value(row, MAX_CANCEL_DATE)

    out["l10n_mx_edi_payment_method_id"] = sheet.cell_value(
        row, L10N_MX_EDI_PAYMENT_METHOD_ID)

    out["type"] = "out_invoice"

    out["invoice_line_ids"] = [{
        "product_id": sheet.cell_value(row, INVOICE_LINE_IDS_PRODUCT_ID),
        "name": sheet.cell_value(row, INVOICE_LINE_IDS_NAME),
        "price_unit": sheet.cell_value(row, INVOICE_LINE_IDS_PRICE_UNIT),
        "commission_id": sheet.cell_value(row, INVOICE_LINE_IDS_COMMISSION_ID),
        "sales_channel": sheet.cell_value(row, PARTNER_ID_REF)
    }]

    out["multicurrency"] = {
        "currency": sheet.cell_value(row, CURRENCY_ID),
        "currency_amount": sheet.cell_value(row, INVOICE_LINE_IDS_PRICE_UNIT),
        "rate": 0,
        "conversion_value": sheet.cell_value(row, INVOICE_LINE_IDS_PRICE_UNIT),
        "commission_fixed": 0
    }

    out["purchase_order_id"] = {
        "partner_id": sheet.cell_value(row, PURCHASE_ORDER_ID_PARTNER_ID),
        "partner_ref": sheet.cell_value(row, PURCHASE_ORDER_ID_PARTNER_REF),
        "price_unit": sheet.cell_value(row, PURCHASE_ORDER_ID_PRICE_UNIT),
        "currency_id": sheet.cell_value(row, PURCHASE_ORDER_ID_CURRENCY_ID),
        "date_order": invoice_date.strftime(DATE_OUT_FORMAT),
        "due_date": check_in_date.strftime(DATE_OUT_FORMAT)
    }

    out["journal_id"] = sheet.cell_value(row, JOURNAL_ID)

    out["invoce_date_due"] = invoice_date.strftime(DATE_OUT_FORMAT)

    return out


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
        dump = xlsx2jsonxlrd(namespace.file)
        print(dump, file=outfile)
        if outfile_is_stdout:
            outfile.close()
    except FileNotFoundError:
        error(
            f"El archivo {namespace.file} no existe o no se tienen permisos para leerlo.")

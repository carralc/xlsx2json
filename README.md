# xlsx2json

`xlsx2json` es un script de python que permite la conversión de un archivo de excel a json.

## Instalación
```bash
pip install -r requirements.txt
```

## Utilización
```bash
./xlsx2json.py ARCHIVO.xlsx -o salida.json
```

# TODO:
- [x] Orden de los campos
- [ ] Validación de estructura de xlsx

## Ejemplo de salida
```json
{
  "meta": {
    "date": "2022-12-28T11:30:11.576170",
    "object_count": 4,
    "type": "invoices"
  },
  "data": [
    {
      "ref": "22BB00021MX001000014",
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "vat": "NCR2001161R6",
        "country_id": "MX"
      },
      "company_id": "PAO",
      "invoice_date": "2022-01-11",
      "currency_id": "USD",
      "check_in_date": "2022-01-11",
      "is_refundable": true,
      "max_cancel_date": "2022-01-11",
      "l10n_mx_edi_payment_method_id": "99",
      "type": "out_invoice",
      "invoice_line_ids": [
        {
          "product_id": "1",
          "quantity": 1,
          "name": "Hôtel Villa Cosy",
          "price_unit": 577.0,
          "commission_id": 20,
          "sales_channel": "BB00021"
        }
      ],
      "multicurrency": {
        "currency": "USD",
        "currency_amount": 577.0,
        "rate": 0,
        "conversion_value": 577.0,
        "commission_fixed": 0
      },
      "purchase_order_id": {
        "partner_id": "57",
        "partner_ref": "197-7181117",
        "price_unit": 559.6,
        "currency_id": "USD",
        "date_order": "2022-01-11",
        "due_date": "2022-01-11"
      },
      "journal_id": "BB00021",
      "invoce_date_due": "2022-01-11"
    },
    {
      "ref": "22BB00021MX001000015",
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "vat": "NCR2001161R6",
        "country_id": "MX"
      },
      "company_id": "PAO",
      "invoice_date": "2022-01-11",
      "currency_id": "USD",
      "check_in_date": "2022-02-11",
      "is_refundable": true,
      "max_cancel_date": "2022-01-11",
      "l10n_mx_edi_payment_method_id": "98",
      "type": "out_invoice",
      "invoice_line_ids": [
        {
          "product_id": "1",
          "quantity": 1,
          "name": "Hilton Madrid Airport",
          "price_unit": 138.0,
          "commission_id": 21,
          "sales_channel": "BB00021"
        }
      ],
      "multicurrency": {
        "currency": "USD",
        "currency_amount": 138.0,
        "rate": 0,
        "conversion_value": 138.0,
        "commission_fixed": 0
      },
      "purchase_order_id": {
        "partner_id": "57",
        "partner_ref": "102-12850026",
        "price_unit": 133.26,
        "currency_id": "USD",
        "date_order": "2022-01-11",
        "due_date": "2022-02-11"
      },
      "journal_id": "BB00021",
      "invoce_date_due": "2022-01-11"
    },
    {
      "ref": "22BB00021MX001000016",
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "vat": "NCR2001161R6",
        "country_id": "MX"
      },
      "company_id": "PAO",
      "invoice_date": "2022-01-11",
      "currency_id": "USD",
      "check_in_date": "2022-06-11",
      "is_refundable": true,
      "max_cancel_date": "2022-01-11",
      "l10n_mx_edi_payment_method_id": "97",
      "type": "out_invoice",
      "invoice_line_ids": [
        {
          "product_id": "6",
          "quantity": 1,
          "name": "Lo mejor de la Toscana en grupo reducido: Montepulciano y Pienza con maridaje de vino y comida",
          "price_unit": 217.0,
          "commission_id": 70,
          "sales_channel": "BB00021"
        }
      ],
      "multicurrency": {
        "currency": "USD",
        "currency_amount": 217.0,
        "rate": 0,
        "conversion_value": 217.0,
        "commission_fixed": 0
      },
      "purchase_order_id": {
        "partner_id": "57",
        "partner_ref": "207-8287559",
        "price_unit": 210.1,
        "currency_id": "USD",
        "date_order": "2022-01-11",
        "due_date": "2022-06-11"
      },
      "journal_id": "BB00021",
      "invoce_date_due": "2022-01-11"
    },
    {
      "ref": "22BB00021MX001000017",
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "vat": "NCR2001161R6",
        "country_id": "MX"
      },
      "company_id": "PAO",
      "invoice_date": "2022-01-11",
      "currency_id": "USD",
      "check_in_date": "2022-11-22",
      "is_refundable": true,
      "max_cancel_date": "2022-01-11",
      "l10n_mx_edi_payment_method_id": "96",
      "type": "out_invoice",
      "invoice_line_ids": [
        {
          "product_id": "6",
          "quantity": 1,
          "name": "Museos Vaticanos, Capilla Sixtina y basílica de San Pedro - Acceso prioritario",
          "price_unit": 105.0,
          "commission_id": 422,
          "sales_channel": "BB00021"
        }
      ],
      "multicurrency": {
        "currency": "USD",
        "currency_amount": 105.0,
        "rate": 0,
        "conversion_value": 105.0,
        "commission_fixed": 0
      },
      "purchase_order_id": {
        "partner_id": "57",
        "partner_ref": "207-8287557",
        "price_unit": 101.14,
        "currency_id": "USD",
        "date_order": "2022-01-11",
        "due_date": "2022-11-22"
      },
      "journal_id": "BB00021",
      "invoce_date_due": "2022-01-11"
    }
  ]
}
```

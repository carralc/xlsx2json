# xlsx2json

`xlsx2json` es un script de python que permite la conversión de un archivo de excel a json.

## Instalación
```bash
pip install -r requirements.txt
```

## Utilización
```bash
./xlsx2json ARCHIVO.xlsx -o salida.json
```

## Ejemplo de salida
```json
{
  "date": "2022-11-14T13:10:16.710346",
  "object_count": 4,
  "data": [
    {
      "check_in_date": "2022-01-11",
      "max_cancel_date": "2022-01-11",
      "currency_id": "USD",
      "ref": "22BB00021MX001000014",
      "partner_id.vat": "NCR2001161R6",
      "journal_id": "BB00021",
      "invoice_date": "2022-01-11",
      "company_id": "PAO",
      "is_refundable": true,
      "purchase_order_id": {
        "partner_ref": "197-7181117",
        "currency_id": "USD",
        "price_unit": 559.6,
        "partner_id": 57
      },
      "invoice_line_ids": [
        {
          "name": "Hôtel Villa Cosy",
          "price_unit": 577,
          "product_id": 1
        }
      ],
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "country_id": "MX"
      }
    },
    {
      "check_in_date": "2022-02-11",
      "max_cancel_date": "2022-01-11",
      "currency_id": "USD",
      "ref": "22BB00021MX001000015",
      "partner_id.vat": "NCR2001161R6",
      "journal_id": "BB00021",
      "invoice_date": "2022-01-11",
      "company_id": "PAO",
      "is_refundable": true,
      "purchase_order_id": {
        "partner_ref": "102-12850026",
        "currency_id": "USD",
        "price_unit": 133.26,
        "partner_id": 57
      },
      "invoice_line_ids": [
        {
          "name": "Hilton Madrid Airport",
          "price_unit": 138,
          "product_id": 1
        }
      ],
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "country_id": "MX"
      }
    },
    {
      "check_in_date": "2022-06-11",
      "max_cancel_date": "2022-01-11",
      "currency_id": "USD",
      "ref": "22BB00021MX001000016",
      "partner_id.vat": "NCR2001161R6",
      "journal_id": "BB00021",
      "invoice_date": "2022-01-11",
      "company_id": "PAO",
      "is_refundable": true,
      "purchase_order_id": {
        "partner_ref": "207-8287559",
        "currency_id": "USD",
        "price_unit": 210.1,
        "partner_id": 57
      },
      "invoice_line_ids": [
        {
          "name": "Lo mejor de la Toscana en grupo reducido: Montepulciano y Pienza con maridaje de vino y comida",
          "price_unit": 217,
          "product_id": 6
        }
      ],
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "country_id": "MX"
      }
    },
    {
      "check_in_date": "2022-11-29",
      "max_cancel_date": "2022-01-11",
      "currency_id": "USD",
      "ref": "22BB00021MX001000017",
      "partner_id.vat": "NCR2001161R6",
      "journal_id": "BB00021",
      "invoice_date": "2022-01-11",
      "company_id": "PAO",
      "is_refundable": true,
      "purchase_order_id": {
        "partner_ref": "207-8287557",
        "currency_id": "USD",
        "price_unit": 101.14,
        "partner_id": 57
      },
      "invoice_line_ids": [
        {
          "name": "Museos Vaticanos, Capilla Sixtina y basílica de San Pedro - Acceso prioritario",
          "price_unit": 105,
          "product_id": 6
        }
      ],
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "country_id": "MX"
      }
    }
  ]
}
```

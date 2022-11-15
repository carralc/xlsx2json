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

# TODO:
- [x] Orden de los campos
- [ ] Validación de estructura de xlsx

## Ejemplo de salida
```json
{
  "meta": {
    "date": "2022-11-14T13:10:16.710346",
    "object_count": 4,
    "type": "invoices"
  },
  "data": [
    {
      "ref": "22BB00021MX001000014",
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "country_id": "MX"
      },
      "company_id": "PAO",
      "invoice_date": "2022-01-11",
      "currency_id": "USD",
      "check_in_date": "2022-01-11",
      "is_refundable": true,
      "max_cancel_date": "2022-01-11",
      "invoice_line_ids": [
        {
          "product_id": 1,
          "name": "Hôtel Villa Cosy",
          "price_unit": 577
        }
      ],
      "purchase_order_id": {
        "partner_id": 57,
        "partner_ref": "197-7181117",
        "price_unit": 559.6,
        "currency_id": "USD"
      },
      "journal_id": "BB00021"
    },
    {
      "ref": "22BB00021MX001000015",
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "country_id": "MX"
      },
      "company_id": "PAO",
      "invoice_date": "2022-01-11",
      "currency_id": "USD",
      "check_in_date": "2022-02-11",
      "is_refundable": true,
      "max_cancel_date": "2022-01-11",
      "invoice_line_ids": [
        {
          "product_id": 1,
          "name": "Hilton Madrid Airport",
          "price_unit": 138
        }
      ],
      "purchase_order_id": {
        "partner_id": 57,
        "partner_ref": "102-12850026",
        "price_unit": 133.26,
        "currency_id": "USD"
      },
      "journal_id": "BB00021"
    },
    {
      "ref": "22BB00021MX001000016",
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "country_id": "MX"
      },
      "company_id": "PAO",
      "invoice_date": "2022-01-11",
      "currency_id": "USD",
      "check_in_date": "2022-06-11",
      "is_refundable": true,
      "max_cancel_date": "2022-01-11",
      "invoice_line_ids": [
        {
          "product_id": 6,
          "name": "Lo mejor de la Toscana en grupo reducido: Montepulciano y Pienza con maridaje de vino y comida",
          "price_unit": 217
        }
      ],
      "purchase_order_id": {
        "partner_id": 57,
        "partner_ref": "207-8287559",
        "price_unit": 210.1,
        "currency_id": "USD"
      },
      "journal_id": "BB00021"
    },
    {
      "ref": "22BB00021MX001000017",
      "partner_id": {
        "ref": "BB00021",
        "name": "NAO CRUISES S.A.P.I. DE C.V.",
        "country_id": "MX"
      },
      "company_id": "PAO",
      "invoice_date": "2022-01-11",
      "currency_id": "USD",
      "check_in_date": "2022-11-29",
      "is_refundable": true,
      "max_cancel_date": "2022-01-11",
      "invoice_line_ids": [
        {
          "product_id": 6,
          "name": "Museos Vaticanos, Capilla Sixtina y basílica de San Pedro - Acceso prioritario",
          "price_unit": 105
        }
      ],
      "purchase_order_id": {
        "partner_id": 57,
        "partner_ref": "207-8287557",
        "price_unit": 101.14,
        "currency_id": "USD"
      },
      "journal_id": "BB00021"
    }
  ]
}
```

import xmlrpc.client
from fastapi import HTTPException

ODOO_URL = "http://localhost:8069"
ODOO_DB = "Database"
ODOO_USERNAME = "rubenavalosmtz@gmail.com"
ODOO_PASSWORD = "pgmh-fzrd-gpkh"


def get_odoo_connection():
    try:
        common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        uid = common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
        if not uid:
            raise Exception("Autenticación fallida")

        models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
        return uid, models

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
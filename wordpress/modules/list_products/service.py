import os
import subprocess

import mysql.connector
from fastapi import HTTPException


def obtener_productos_wordpress():
    try:
        db_host = os.getenv("WORDPRESS_DB_HOST", "127.0.0.1")
        db_port = int(os.getenv("WORDPRESS_DB_PORT", "3306"))
        db_name = os.getenv("WORDPRESS_DB_NAME", "wordpress")
        db_user = os.getenv("WORDPRESS_DB_USER", "wpuser")
        db_password = os.getenv("WORDPRESS_DB_PASSWORD", "wppass")
        table_prefix = os.getenv("WORDPRESS_TABLE_PREFIX", "wp_")

        query = f"""
            SELECT
                p.ID AS id,
                p.post_title AS name,
                p.post_status AS status,
                COALESCE(sku.meta_value, '') AS sku,
                COALESCE(price.meta_value, '') AS price
            FROM {table_prefix}posts p
            LEFT JOIN {table_prefix}postmeta sku
                ON sku.post_id = p.ID AND sku.meta_key = '_sku'
            LEFT JOIN {table_prefix}postmeta price
                ON price.post_id = p.ID AND price.meta_key = '_price'
            WHERE p.post_type = 'product'
              AND p.post_status NOT IN ('trash', 'auto-draft')
            ORDER BY p.post_date DESC, p.ID DESC
        """.strip()

        try:
            connection = mysql.connector.connect(
                host=db_host,
                port=db_port,
                database=db_name,
                user=db_user,
                password=db_password,
            )

            try:
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query)
                productos = cursor.fetchall()
            finally:
                connection.close()

        except Exception:
            db_container = os.getenv("WORDPRESS_DB_CONTAINER", "word-press-db-1")
            db_root_user = os.getenv("WORDPRESS_DB_ROOT_USER", "root")
            db_root_password = os.getenv("WORDPRESS_DB_ROOT_PASSWORD", "rootpass")

            command = [
                "docker",
                "exec",
                db_container,
                "mysql",
                f"-u{db_root_user}",
                f"-p{db_root_password}",
                "-N",
                "-B",
                db_name,
                "-e",
                query,
            ]

            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            if process.returncode != 0:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error al listar productos de WordPress: {process.stderr.strip() or process.stdout.strip()}",
                )

            productos = []
            for line in process.stdout.splitlines():
                if not line.strip():
                    continue
                partes = line.split("\t")
                if len(partes) < 5:
                    continue
                productos.append(
                    {
                        "id": int(partes[0]),
                        "name": partes[1],
                        "status": partes[2],
                        "sku": partes[3] or None,
                        "price": partes[4] or None,
                    }
                )

        resultado = []
        for producto in productos:
            resultado.append(
                {
                    "id": producto.get("id"),
                    "name": producto.get("name"),
                    "sku": producto.get("sku"),
                    "price": producto.get("price"),
                    "status": producto.get("status"),
                }
            )

        return {"total": len(resultado), "data": resultado}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar productos de WordPress: {str(e)}")

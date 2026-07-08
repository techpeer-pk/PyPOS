"""Product, Invoice CRUD operations."""
from datetime import datetime

from database import get_connection


class StockError(Exception):
    pass


class Product:
    @staticmethod
    def add(name, sku, price, stock=0, reorder_level=5):
        conn = get_connection()
        try:
            cur = conn.execute(
                "INSERT INTO products (name, sku, price, stock, reorder_level) "
                "VALUES (?, ?, ?, ?, ?)",
                (name, sku, price, stock, reorder_level),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            conn.close()

    @staticmethod
    def get_by_sku(sku):
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT * FROM products WHERE sku = ?", (sku,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        try:
            rows = conn.execute("SELECT * FROM products ORDER BY name").fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def search(term):
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM products WHERE name LIKE ? OR sku LIKE ? ORDER BY name",
                (f"%{term}%", f"%{term}%"),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def update_stock(sku, new_qty):
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE products SET stock = ? WHERE sku = ?", (new_qty, sku)
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def update(sku, name=None, price=None, reorder_level=None):
        fields, values = [], []
        if name is not None:
            fields.append("name = ?")
            values.append(name)
        if price is not None:
            fields.append("price = ?")
            values.append(price)
        if reorder_level is not None:
            fields.append("reorder_level = ?")
            values.append(reorder_level)
        if not fields:
            return
        values.append(sku)
        conn = get_connection()
        try:
            conn.execute(f"UPDATE products SET {', '.join(fields)} WHERE sku = ?", values)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def low_stock():
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM products WHERE stock <= reorder_level ORDER BY stock"
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


class Invoice:
    @staticmethod
    def _next_id(conn, date_str):
        prefix = f"INV-{date_str}-"
        row = conn.execute(
            "SELECT id FROM invoices WHERE id LIKE ? ORDER BY id DESC LIMIT 1",
            (f"{prefix}%",),
        ).fetchone()
        if row:
            seq = int(row["id"].rsplit("-", 1)[-1]) + 1
        else:
            seq = 1
        return f"{prefix}{seq:03d}"

    @staticmethod
    def create(items, payment_method):
        """items: list of dicts {sku, quantity}. Returns the created invoice dict."""
        if not items:
            raise ValueError("Cannot create an invoice with no items")

        conn = get_connection()
        try:
            now = datetime.now()
            date_str = now.strftime("%Y%m%d")
            invoice_id = Invoice._next_id(conn, date_str)

            total = 0.0
            resolved_items = []
            for item in items:
                product = conn.execute(
                    "SELECT * FROM products WHERE sku = ?", (item["sku"],)
                ).fetchone()
                if not product:
                    raise ValueError(f"Product not found: {item['sku']}")
                qty = item["quantity"]
                if product["stock"] < qty:
                    raise StockError(f"Not enough stock for {product['name']}")
                unit_price = product["price"]
                total += unit_price * qty
                resolved_items.append((product["id"], product["name"], qty, unit_price))

            conn.execute(
                "INSERT INTO invoices (id, date, total, items_count, payment_method) "
                "VALUES (?, ?, ?, ?, ?)",
                (invoice_id, now.strftime("%Y-%m-%d %H:%M:%S"), total, len(resolved_items), payment_method),
            )
            for product_id, _name, qty, unit_price in resolved_items:
                conn.execute(
                    "INSERT INTO invoice_items (invoice_id, product_id, quantity, unit_price) "
                    "VALUES (?, ?, ?, ?)",
                    (invoice_id, product_id, qty, unit_price),
                )
                conn.execute(
                    "UPDATE products SET stock = stock - ? WHERE id = ?", (qty, product_id)
                )
            conn.commit()

            return {
                "id": invoice_id,
                "date": now.strftime("%Y-%m-%d %H:%M:%S"),
                "total": total,
                "items_count": len(resolved_items),
                "payment_method": payment_method,
                "items": [
                    {"name": name, "quantity": qty, "unit_price": unit_price}
                    for _pid, name, qty, unit_price in resolved_items
                ],
            }
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def get_today_total():
        conn = get_connection()
        try:
            row = conn.execute(
                "SELECT COALESCE(SUM(total), 0) AS total, COUNT(*) AS count "
                "FROM invoices WHERE date LIKE ?",
                (f"{datetime.now().strftime('%Y-%m-%d')}%",),
            ).fetchone()
            return {"total": row["total"], "count": row["count"]}
        finally:
            conn.close()

    @staticmethod
    def get_by_date(date_str):
        """date_str format: YYYY-MM-DD"""
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM invoices WHERE date LIKE ? ORDER BY date",
                (f"{date_str}%",),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_recent(limit=1):
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT * FROM invoices ORDER BY date DESC LIMIT ?", (limit,)
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def get_items(invoice_id):
        conn = get_connection()
        try:
            rows = conn.execute(
                "SELECT ii.*, p.name AS product_name FROM invoice_items ii "
                "JOIN products p ON p.id = ii.product_id WHERE ii.invoice_id = ?",
                (invoice_id,),
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

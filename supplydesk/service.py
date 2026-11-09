"""Operations used by the command-line order desk."""

from supplydesk.storage import JsonStore


STUDENT_DISCOUNT_THRESHOLD_CENTS = 5000
STUDENT_DISCOUNT_PERCENT = 10
FREE_DELIVERY_THRESHOLD_CENTS = 10000
STANDARD_DELIVERY_CENTS = 600
EXPRESS_DELIVERY_CENTS = 1200


class OrderService:
    def __init__(self, state_path=".supplydesk/state.json"):
        self.store = JsonStore(state_path)

    def catalog(self):
        return self.store.load()["catalog"]

    def quote(self, customer_type, items, fulfillment="pickup"):
        return self._build_quote(self.store.load(), customer_type, items, fulfillment)

    @staticmethod
    def _build_quote(state, customer_type, items, fulfillment):
        if customer_type not in ("regular", "student"):
            raise ValueError("Customer type must be regular or student.")
        if fulfillment not in ("pickup", "delivery", "express"):
            raise ValueError("Fulfillment must be pickup, delivery or express.")
        if not isinstance(items, list) or not items:
            raise ValueError("An order must contain at least one item.")
        lines = []
        subtotal_cents = 0
        requested_quantities = {}
        for item in items:
            if not isinstance(item, dict):
                raise ValueError("Each item must contain a product_id and quantity.")
            product = None
            for candidate in state["catalog"]:
                if candidate["product_id"] == item.get("product_id"):
                    product = candidate
                    break
            if product is None:
                raise ValueError("Unknown product.")
            quantity = item.get("quantity")
            if type(quantity) is not int or quantity < 1 or quantity > 99:
                raise ValueError("Quantity must be an integer from 1 to 99.")
            product_id = product["product_id"]
            requested_quantities[product_id] = requested_quantities.get(product_id, 0) + quantity
            if requested_quantities[product_id] > product["stock"]:
                raise ValueError("Not enough stock for " + product["product_id"] + ".")
            line_total_cents = product["unit_price_cents"] * quantity
            subtotal_cents += line_total_cents
            lines.append({
                "product_id": product["product_id"],
                "name": product["name"],
                "unit_price_cents": product["unit_price_cents"],
                "quantity": quantity,
                "line_total_cents": line_total_cents,
            })
        discount_cents = 0
        if customer_type == "student" and subtotal_cents >= STUDENT_DISCOUNT_THRESHOLD_CENTS:
            discount_cents = (subtotal_cents * STUDENT_DISCOUNT_PERCENT + 50) // 100
        delivery_cents = 0
        if fulfillment == "delivery" and subtotal_cents - discount_cents < FREE_DELIVERY_THRESHOLD_CENTS:
            delivery_cents = STANDARD_DELIVERY_CENTS
        elif fulfillment == "express":
            delivery_cents = EXPRESS_DELIVERY_CENTS
        return {
            "customer_type": customer_type,
            "fulfillment": fulfillment,
            "items": lines,
            "subtotal_cents": subtotal_cents,
            "discount_cents": discount_cents,
            "delivery_cents": delivery_cents,
            "total_cents": subtotal_cents - discount_cents + delivery_cents,
        }

    def place_order(self, customer_type, items, fulfillment="pickup"):
        state = self.store.load()
        quote = self._build_quote(state, customer_type, items, fulfillment)
        order = {
            "order_id": "ORD-" + str(state["next_order_number"]).zfill(4),
            "status": "placed",
            **quote,
        }
        self._change_stock(state, order["items"], -1)
        state["next_order_number"] += 1
        state["orders"].append(order)
        self.store.save(state)
        return order

    def list_orders(self):
        return self.store.load()["orders"]

    @staticmethod
    def _find_order(state, order_id):
        for order in state["orders"]:
            if order["order_id"] == order_id:
                return order
        raise ValueError("Unknown order: " + order_id)

    @staticmethod
    def _change_stock(state, lines, direction):
        products = {product["product_id"]: product for product in state["catalog"]}
        for line in lines:
            products[line["product_id"]]["stock"] += direction * line["quantity"]

    def get_order(self, order_id):
        return self._find_order(self.store.load(), order_id)

    def cancel_order(self, order_id):
        state = self.store.load()
        order = self._find_order(state, order_id)
        if order["status"] == "cancelled":
            return order
        self._change_stock(state, order["items"], 1)
        order["status"] = "cancelled"
        self.store.save(state)
        return order

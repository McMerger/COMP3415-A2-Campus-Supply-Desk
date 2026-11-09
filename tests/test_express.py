"""CR-01 acceptance tests across pricing, persistence and rejection paths."""

from tests.support import ServiceTestCase, item
from supplydesk.service import OrderService


class ExpressTests(ServiceTestCase):
    def test_client_examples_quote_and_place(self):
        cases = [
            ("regular", [item(quantity=2)], 0, 2200),
            ("student", [item("hoodie", 2)], 800, 8400),
            ("regular", [item("hoodie", 3)], 0, 13200),
        ]
        for customer, items, discount, total in cases:
            with self.subTest(customer=customer, total=total):
                quote = self.service.quote(customer, items, "express")
                order = self.service.place_order(customer, items, "express")
                self.assertEqual(quote["delivery_cents"], 1200)
                self.assertEqual(quote["discount_cents"], discount)
                self.assertEqual(quote["total_cents"], total)
                self.assertEqual({key: order[key] for key in quote}, quote)

    def test_express_fee_not_waived_above_discounted_threshold(self):
        result = self.service.quote("student", [item("hoodie", 3)], "express")
        self.assertEqual(result["discount_cents"], 1200)
        self.assertEqual(result["delivery_cents"], 1200)
        self.assertEqual(result["total_cents"], 12000)

    def test_discount_at_exact_threshold_excludes_express_fee(self):
        result = self.service.quote("student", [item("bag", 2)], "express")
        self.assertEqual(result["discount_cents"], 500)
        self.assertEqual(result["total_cents"], 5700)

    def test_delivery_fee_does_not_make_merchandise_discount_eligible(self):
        result = self.service.quote("student", [item("hoodie")], "express")
        self.assertEqual(result["discount_cents"], 0)
        self.assertEqual(result["total_cents"], 5200)

    def test_express_snapshot_persists_through_reopen_and_cancel(self):
        order = self.service.place_order("student", [item("hoodie", 2)], "express")
        reopened = OrderService(self.path)
        self.assertEqual(reopened.get_order(order["order_id"]), order)
        self.assertEqual(reopened.list_orders(), [order])
        self.assertEqual(self.stock("hoodie"), 3)
        cancelled = reopened.cancel_order(order["order_id"])
        expected = {**order, "status": "cancelled"}
        self.assertEqual(cancelled, expected)
        self.assertEqual(OrderService(self.path).get_order(order["order_id"]), expected)
        before = self.path.read_bytes()
        self.assertEqual(reopened.cancel_order(order["order_id"]), expected)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.stock("hoodie"), 5)
        self.assertEqual(reopened.place_order("regular", [item()])["order_id"], "ORD-0002")

    def test_express_rejects_invalid_stock_quantity_and_customer(self):
        for operation in (self.service.quote, self.service.place_order):
            for customer, items in (("guest", [item()]), ("regular", [item(quantity=True)]),
                                    ("regular", [item(quantity=11), item(quantity=10)])):
                with self.subTest(operation=operation.__name__, items=items, customer=customer):
                    with self.assertRaises(ValueError):
                        operation(customer, items, "express")
                    self.assertFalse(self.path.exists())

    def test_other_fulfillment_values_remain_invalid(self):
        for fulfillment in ("overnight", "Express", "", None):
            for operation in (self.service.quote, self.service.place_order):
                with self.subTest(fulfillment=fulfillment, operation=operation.__name__):
                    with self.assertRaises(ValueError):
                        operation("regular", [item()], fulfillment)
        self.assertFalse(self.path.exists())

    def test_standard_and_pickup_preserved_alongside_express(self):
        for fulfillment, fee, total in (("pickup", 0, 12000), ("delivery", 0, 12000),
                                        ("express", 1200, 13200)):
            with self.subTest(fulfillment=fulfillment):
                result = self.service.quote("regular", [item("hoodie", 3)], fulfillment)
                self.assertEqual(result["delivery_cents"], fee)
                self.assertEqual(result["total_cents"], total)

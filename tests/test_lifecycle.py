"""Persistence and state-transition contracts across fresh service instances."""

from tests.support import ServiceTestCase, item
from supplydesk.service import OrderService


class LifecycleTests(ServiceTestCase):
    def test_quote_and_catalog_do_not_create_save_or_consume_id(self):
        before = self.service.catalog()
        self.service.quote("student", [item("hoodie", 2)], "delivery")
        self.assertFalse(self.path.exists())
        self.assertEqual(self.service.catalog(), before)
        self.assertEqual(self.service.list_orders(), [])
        self.assertEqual(self.service.place_order("regular", [item()])["order_id"], "ORD-0001")

    def test_quote_does_not_modify_existing_save(self):
        self.service.place_order("regular", [item()])
        before = self.path.read_bytes()
        self.service.quote("regular", [item("mug")])
        self.service.catalog()
        self.assertEqual(self.path.read_bytes(), before)

    def test_quote_and_placement_have_identical_pricing_and_items(self):
        request = ("student", [item("hoodie"), item("mug")], "delivery")
        quote = self.service.quote(*request)
        order = self.service.place_order(*request)
        self.assertEqual({key: order[key] for key in quote}, quote)
        self.assertEqual(self.stock("hoodie"), 4)
        self.assertEqual(self.stock("mug"), 7)

    def test_placement_rechecks_stock_after_quote(self):
        request = ("regular", [item("hoodie", 5)])
        self.service.quote(*request)
        self.service.place_order(*request)
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            self.service.place_order(*request)
        self.assertEqual(self.path.read_bytes(), before)

    def test_duplicate_lines_at_stock_limit_are_preserved_and_restored(self):
        items = [item(quantity=9), item(quantity=11)]
        order = self.service.place_order("regular", items)
        self.assertEqual([line["quantity"] for line in order["items"]], [9, 11])
        self.assertEqual(order["subtotal_cents"], 10000)
        self.assertEqual(self.stock("notebook"), 0)
        self.service.cancel_order(order["order_id"])
        self.assertEqual(self.stock("notebook"), 20)

    def test_repeated_cancellation_is_idempotent_after_reopening(self):
        order = self.service.place_order("regular", [item("mug", 2)])
        first = self.service.cancel_order(order["order_id"])
        before = self.path.read_bytes()
        reopened = OrderService(self.path)
        second = reopened.cancel_order(order["order_id"])
        self.assertEqual(first, second)
        self.assertEqual(self.stock("mug"), 8)
        self.assertEqual(self.path.read_bytes(), before)

    def test_history_preserves_order_totals_status_and_numbering(self):
        first = self.service.place_order("student", [item("hoodie", 2)], "delivery")
        cancelled = self.service.cancel_order(first["order_id"])
        self.assertEqual({k: v for k, v in cancelled.items() if k != "status"},
                         {k: v for k, v in first.items() if k != "status"})
        second = self.service.place_order("regular", [item("bag")])
        self.assertEqual(second["order_id"], "ORD-0002")
        reopened = OrderService(self.path)
        self.assertEqual(reopened.list_orders(), [cancelled, second])
        self.assertEqual(reopened.get_order(first["order_id"]), cancelled)
        self.assertEqual(self.stock("bag"), 3)

    def test_history_is_snapshot_after_catalog_price_change(self):
        order = self.service.place_order("regular", [item()])
        state = self.service.store.load()
        state["catalog"][0]["unit_price_cents"] = 900
        self.service.store.save(state)
        self.assertEqual(OrderService(self.path).get_order(order["order_id"]), order)

    def test_unknown_lookup_and_cancel_leave_saved_data_unchanged(self):
        self.service.place_order("regular", [item()])
        before = self.path.read_bytes()
        for operation in (self.service.get_order, self.service.cancel_order):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(ValueError):
                    operation("ORD-9999")
                self.assertEqual(self.path.read_bytes(), before)

    def test_malformed_and_unreadable_save_are_not_reset(self):
        self.path.write_text("{broken", encoding="utf-8")
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            self.service.catalog()
        self.assertEqual(self.path.read_bytes(), before)
        from unittest.mock import patch
        with patch("pathlib.Path.open", side_effect=PermissionError("Denied")):
            with self.assertRaises(PermissionError):
                self.service.catalog()
        self.assertEqual(self.path.read_bytes(), before)

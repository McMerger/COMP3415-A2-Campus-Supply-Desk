"""Rejected requests must preserve bytes, stock, history and numbering."""

from tests.support import ServiceTestCase, item


class ValidationTests(ServiceTestCase):
    def test_invalid_requests_do_not_modify_existing_state(self):
        self.service.place_order("regular", [item("mug")])
        before = self.path.read_bytes()
        cases = [
            ("guest", [item()], "pickup"),
            ("Regular", [item()], "pickup"),
            ("regular", [item()], "post"),
            ("regular", [], "pickup"),
            ("regular", None, "pickup"),
            ("regular", (item(),), "pickup"),
            ("regular", [None], "pickup"),
            ("regular", [{}], "pickup"),
            ("regular", [item("unknown")], "pickup"),
            ("regular", [item([])], "pickup"),
            ("regular", [item({})], "pickup"),
            ("regular", [{"product_id": "notebook"}], "pickup"),
            ("regular", [{"quantity": 1}], "pickup"),
        ]
        for quantity in (0, -1, 100, True, False, 1.5, "2", None):
            cases.append(("regular", [item(quantity=quantity)], "pickup"))
        for operation in (self.service.quote, self.service.place_order):
            for request in cases:
                with self.subTest(operation=operation.__name__, request=request):
                    with self.assertRaises(ValueError):
                        operation(*request)
                    self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(self.service.place_order("regular", [item()])["order_id"], "ORD-0002")

    def test_invalid_later_line_does_not_partially_save(self):
        with self.assertRaises(ValueError):
            self.service.place_order("regular", [item(), item("unknown")])
        self.assertFalse(self.path.exists())
        self.assertEqual(self.stock("notebook"), 20)
        self.assertEqual(self.service.place_order("regular", [item()])["order_id"], "ORD-0001")

    def test_combined_duplicate_quantity_cannot_exceed_stock(self):
        # Each line fits alone, but the complete request exceeds stock.
        for operation in (self.service.quote, self.service.place_order):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(ValueError):
                    operation("regular", [item(quantity=11), item(quantity=10)])
                self.assertFalse(self.path.exists())
                self.assertEqual(self.stock("notebook"), 20)

    def test_duplicate_rejection_preserves_prior_success(self):
        self.service.place_order("regular", [item("mug")])
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            self.service.place_order("regular", [item(quantity=11), item(quantity=10)])
        self.assertEqual(self.path.read_bytes(), before)

    def test_exact_stock_is_allowed_but_one_more_is_rejected(self):
        for operation in (self.service.quote, self.service.place_order):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(ValueError):
                    operation("regular", [item(quantity=21)])
        self.service.place_order("regular", [item(quantity=20)])
        self.assertEqual(self.stock("notebook"), 0)

    def test_quantity_upper_boundary_99_with_stock_fixture(self):
        from unittest.mock import patch
        state = self.service.store.load()
        state["catalog"][0]["stock"] = 100
        with patch.object(self.service.store, "load", return_value=state):
            self.assertEqual(self.service.quote("regular", [item(quantity=99)])["items"][0]["quantity"], 99)
            with self.assertRaises(ValueError):
                self.service.quote("regular", [item(quantity=100)])

"""Independent expected amounts at discount and delivery boundaries."""

from tests.support import ServiceTestCase, item


class PricingTests(ServiceTestCase):
    def test_student_discount_at_threshold_for_both_operations(self):
        for operation in (self.service.quote, self.service.place_order):
            with self.subTest(operation=operation.__name__):
                result = operation("student", [item("bag", 2)])
                self.assertEqual(result["subtotal_cents"], 5000)
                self.assertEqual(result["discount_cents"], 500)
                self.assertEqual(result["total_cents"], 4500)

    def test_student_discount_below_threshold(self):
        result = self.service.quote("student", [item("hoodie"), item("pen-pack")])
        self.assertEqual(result["subtotal_cents"], 4750)
        self.assertEqual(result["discount_cents"], 0)

    def test_regular_has_no_discount_at_threshold(self):
        result = self.service.quote("regular", [item("bag", 2)])
        self.assertEqual(result["discount_cents"], 0)
        self.assertEqual(result["total_cents"], 5000)

    def test_delivery_below_at_and_above_threshold(self):
        for quantity, expected_fee, expected_total in ((19, 600, 10100), (20, 0, 10000)):
            with self.subTest(quantity=quantity):
                result = self.service.quote("regular", [item(quantity=quantity)], "delivery")
                self.assertEqual(result["delivery_cents"], expected_fee)
                self.assertEqual(result["total_cents"], expected_total)
        result = self.service.quote("regular", [item("hoodie", 3)], "delivery")
        self.assertEqual(result["total_cents"], 12000)
        self.assertEqual(result["delivery_cents"], 0)

    def test_delivery_threshold_uses_discounted_subtotal(self):
        result = self.service.quote("student", [item("bag", 4)], "delivery")
        self.assertEqual(result["subtotal_cents"], 10000)
        self.assertEqual(result["discount_cents"], 1000)
        self.assertEqual(result["delivery_cents"], 600)
        self.assertEqual(result["total_cents"], 9600)

    def test_pickup_is_free_and_money_is_integer(self):
        result = self.service.quote("student", [item("hoodie", 2)])
        self.assertEqual(result["delivery_cents"], 0)
        for key in ("subtotal_cents", "discount_cents", "delivery_cents", "total_cents"):
            self.assertIs(type(result[key]), int)

    def test_half_cent_discount_rounds_up_with_catalog_fixture(self):
        # Bundled prices cannot produce a half-cent discount. Change only a
        # freshly loaded in-memory catalog, not the on-disk save-file schema.
        from unittest.mock import patch
        state = self.service.store.load()
        state["catalog"][0]["unit_price_cents"] = 5005
        with patch.object(self.service.store, "load", return_value=state):
            result = self.service.quote("student", [item()])
        self.assertEqual(result["discount_cents"], 501)
        self.assertEqual(result["total_cents"], 4504)

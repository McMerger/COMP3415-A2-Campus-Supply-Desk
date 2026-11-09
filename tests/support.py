"""Isolated application-generated state for requirements tests."""

from pathlib import Path
import tempfile
import unittest

from supplydesk.service import OrderService


class ServiceTestCase(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.path = Path(directory.name) / "state.json"
        self.service = OrderService(self.path)

    def stock(self, product_id):
        return next(p["stock"] for p in self.service.catalog()
                    if p["product_id"] == product_id)


def item(product_id="notebook", quantity=1):
    return {"product_id": product_id, "quantity": quantity}

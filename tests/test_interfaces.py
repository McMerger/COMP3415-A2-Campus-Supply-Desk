"""Real command processes and scripted menu input exercise public adapters."""

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

from supplydesk.menu import run_menu
from tests.support import ServiceTestCase, item


class CommandTests(ServiceTestCase):
    def command(self, *arguments):
        return subprocess.run(
            [sys.executable, "-m", "supplydesk", "--data", str(self.path), *arguments],
            cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True,
            timeout=15,
        )

    def test_default_quote_json_and_no_save(self):
        result = self.command("quote", "--item", "notebook:2")
        self.assertEqual(result.returncode, 0, result.stderr)
        quote = json.loads(result.stdout)
        self.assertEqual(quote["total_cents"], 1000)
        self.assertEqual((quote["customer_type"], quote["fulfillment"]), ("regular", "pickup"))
        self.assertFalse(self.path.exists())

    def test_cli_rejects_invalid_input_without_save(self):
        for arguments in (("quote", "--item", "notebook:abc"),
                          ("quote", "--item", "notebook"),
                          ("quote", "--item", "notebook:0"),
                          ("quote", "--item", "missing:1"),
                          ("quote", "--fulfillment", "overnight", "--item", "notebook:1"),
                          ("place", "--item", "notebook:11", "--item", "notebook:10")):
            with self.subTest(arguments=arguments):
                result = self.command(*arguments)
                self.assertEqual(result.returncode, 2)
                self.assertIn("error", result.stderr.lower())
                self.assertFalse(self.path.exists())

    def test_express_quote_from_client_example(self):
        result = self.command("quote", "--customer", "student", "--fulfillment", "express",
                              "--item", "hoodie:2")
        self.assertEqual(result.returncode, 0, result.stderr)
        quote = json.loads(result.stdout)
        self.assertEqual(quote["total_cents"], 8400)
        self.assertEqual(quote["delivery_cents"], 1200)
        self.assertFalse(self.path.exists())

    def test_immediate_express_place_history_show_and_repeated_cancel(self):
        placed = self.command("place", "--fulfillment", "express", "--item", "notebook:2")
        self.assertEqual(placed.returncode, 0, placed.stderr)
        order = json.loads(placed.stdout)
        self.assertEqual(order["total_cents"], 2200)
        shown = self.command("show", order["order_id"])
        self.assertEqual(shown.returncode, 0, shown.stderr)
        self.assertEqual(json.loads(shown.stdout), order)
        history = self.command("orders")
        self.assertEqual(json.loads(history.stdout), [order])
        for _ in range(2):
            cancelled = self.command("cancel", order["order_id"])
            self.assertEqual(cancelled.returncode, 0, cancelled.stderr)
            self.assertEqual(json.loads(cancelled.stdout), {**order, "status": "cancelled"})
        self.assertEqual(self.stock("notebook"), 20)

    def test_express_is_discoverable_in_both_command_help_screens(self):
        for operation in ("quote", "place"):
            with self.subTest(operation=operation):
                result = self.command(operation, "--help")
                self.assertEqual(result.returncode, 0)
                self.assertIn("express", result.stdout)

    def test_malformed_save_reports_error_without_reset(self):
        self.path.write_text("{broken", encoding="utf-8")
        result = self.command("catalog")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Error:", result.stderr)
        self.assertEqual(self.path.read_text(), "{broken")

    def test_actual_module_opens_menu_and_exits(self):
        result = subprocess.run([sys.executable, "-m", "supplydesk", "--data", str(self.path)],
                                input="0\n", capture_output=True, text=True, timeout=15,
                                cwd=Path(__file__).resolve().parents[1])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Campus Supply Desk", result.stdout)
        self.assertIn("Goodbye.", result.stdout)


class MenuTests(ServiceTestCase):
    def menu(self, answers):
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), redirect_stdout(output):
            self.assertEqual(run_menu(self.service), 0)
        return output.getvalue()

    def test_defaults_quote_and_retry_non_integer_quantity(self):
        output = self.menu(["2", "", "notebook", "abc", "notebook", "2", "", "", "0"])
        self.assertIn("Please enter a whole number", output)
        self.assertIn("Customer: regular | Fulfillment: pickup", output)
        self.assertIn("Total: $10.00", output)
        self.assertFalse(self.path.exists())

    def test_declining_placement_leaves_no_save(self):
        output = self.menu(["3", "", "notebook", "2", "", "", "n", "0"])
        self.assertIn("Order not placed.", output)
        self.assertFalse(self.path.exists())

    def test_express_prompt_and_confirmed_order(self):
        output = io.StringIO()
        answers = iter(["3", "student", "hoodie", "2", "", "express", "y", "0"])
        prompts = []
        def read(prompt):
            prompts.append(prompt)
            return next(answers)
        with patch("builtins.input", side_effect=read), redirect_stdout(output):
            self.assertEqual(run_menu(self.service), 0)
        self.assertTrue(any("express" in prompt for prompt in prompts))
        self.assertIn("Total: $84.00", output.getvalue())
        order = self.service.get_order("ORD-0001")
        self.assertEqual(order["fulfillment"], "express")
        self.assertEqual(order["delivery_cents"], 1200)

    def test_declining_cancel_preserves_save(self):
        order = self.service.place_order("regular", [item()])
        before = self.path.read_bytes()
        self.menu(["6", order["order_id"], "", "0"])
        self.assertEqual(self.path.read_bytes(), before)

    def test_confirmed_cancel_restores_stock(self):
        order = self.service.place_order("regular", [item("mug", 2)])
        self.menu(["6", order["order_id"], "y", "0"])
        self.assertEqual(self.stock("mug"), 8)
        self.assertEqual(self.service.get_order(order["order_id"])["status"], "cancelled")

    def test_invalid_request_returns_to_menu(self):
        output = self.menu(["2", "guest", "notebook", "2", "", "", "0"])
        self.assertIn("Error:", output)
        self.assertIn("Returning to the menu", output)
        self.assertIn("Goodbye.", output)
        self.assertFalse(self.path.exists())

    def test_eof_and_interrupt_exit_cleanly(self):
        for interruption in (EOFError(), KeyboardInterrupt()):
            with self.subTest(interruption=type(interruption).__name__):
                output = self.menu([interruption])
                self.assertIn("Goodbye.", output)

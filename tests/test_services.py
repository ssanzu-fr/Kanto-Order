"""
Phase 8 - Service Tests
Unit tests for all services to verify business logic.
"""
import unittest
import os
import json
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.order_service import OrderService
from services.payment_service import PaymentService
from services.workflow_service import WorkflowService
from services.storage_service import StorageService
from models.order_item import OrderItem
from models.enums import OrderStatus, PaymentStatus
from data.menu import get_item_by_id
from ui.receipt_formatter import format_receipt


class TestOrderService(unittest.TestCase):
    """Test OrderService functionality."""

    def setUp(self):
        self.service = OrderService()

    def test_create_order_pay_now(self):
        """Test creating order with immediate payment."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]

        order = self.service.create_order("Maria Santos", items, pay_now=True)

        self.assertEqual(order.customer_name, "Maria Santos")
        self.assertEqual(order.order_number, "001")
        self.assertEqual(order.status, OrderStatus.CONFIRMED)
        self.assertEqual(order.payment.status, PaymentStatus.PAID)
        self.assertEqual(order.total, 120)

    def test_create_order_pay_later(self):
        """Test creating order with deferred payment."""
        lugaw = get_item_by_id("lugaw")
        items = [OrderItem(menu_item=lugaw, quantity=2)]

        order = self.service.create_order("Juan Cruz", items, pay_now=False)

        self.assertEqual(order.status, OrderStatus.PENDING_PAYMENT)
        self.assertEqual(order.payment.status, PaymentStatus.UNPAID)
        self.assertEqual(order.total, 70)

    def test_calculate_total(self):
        """Test total calculation with multiple items."""
        chicken = get_item_by_id("chicken_meal")
        buko = get_item_by_id("buko_juice")
        items = [
            OrderItem(menu_item=chicken, quantity=1),
            OrderItem(menu_item=buko, quantity=2)
        ]

        total = self.service.calculate_total(items)
        self.assertEqual(total, 190)  # 120 + 35*2

    def test_order_number_increments(self):
        """Test order numbers increment correctly."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]

        order1 = self.service.create_order("Customer 1", items, True)
        order2 = self.service.create_order("Customer 2", items, True)

        self.assertEqual(order1.order_number, "001")
        self.assertEqual(order2.order_number, "002")

    def test_empty_name_raises_error(self):
        """Test that empty customer name raises error."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]

        with self.assertRaises(ValueError):
            self.service.create_order("", items, True)

    def test_empty_cart_raises_error(self):
        """Test that empty cart raises error."""
        with self.assertRaises(ValueError):
            self.service.create_order("Maria Santos", [], True)


class TestPaymentService(unittest.TestCase):
    """Test PaymentService functionality."""

    def setUp(self):
        self.service = PaymentService()
        self.order_service = OrderService()

    def test_mark_as_paid(self):
        """Test marking an order as paid."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]
        order = self.order_service.create_order("Maria", items, pay_now=False)

        self.assertFalse(self.service.is_paid(order))
        self.service.mark_as_paid(order)

        self.assertTrue(self.service.is_paid(order))
        self.assertEqual(order.status, OrderStatus.CONFIRMED)

    def test_mark_already_paid_raises_error(self):
        """Test that marking already paid order raises error."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]
        order = self.order_service.create_order("Maria", items, pay_now=True)

        with self.assertRaises(ValueError):
            self.service.mark_as_paid(order)


class TestWorkflowService(unittest.TestCase):
    """Test WorkflowService functionality."""

    def setUp(self):
        self.service = WorkflowService()
        self.order_service = OrderService()
        self.payment_service = PaymentService()

    def test_forward_only_transitions(self):
        """Test that orders can only move forward through statuses."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]
        order = self.order_service.create_order("Maria", items, pay_now=True)

        # Confirmed -> Preparing
        self.service.start_preparing(order)
        self.assertEqual(order.status, OrderStatus.PREPARING)

        # Preparing -> Ready
        self.service.mark_ready(order)
        self.assertEqual(order.status, OrderStatus.READY)

        # Ready -> Completed
        self.service.complete_order(order)
        self.assertEqual(order.status, OrderStatus.COMPLETED)

    def test_unpaid_cannot_be_prepared(self):
        """Test that unpaid orders cannot be prepared."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]
        order = self.order_service.create_order("Maria", items, pay_now=False)

        # Try to prepare unpaid order
        with self.assertRaises(ValueError):
            self.service.transition_to(order, OrderStatus.PREPARING)

    def test_no_skipping_statuses(self):
        """Test that statuses cannot be skipped."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]
        order = self.order_service.create_order("Maria", items, pay_now=True)

        # Try to skip from Confirmed to Ready
        with self.assertRaises(ValueError):
            self.service.transition_to(order, OrderStatus.READY)

    def test_completed_cannot_transition(self):
        """Test that completed orders cannot transition further."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]
        order = self.order_service.create_order("Maria", items, pay_now=True)

        # Move to completed
        self.service.start_preparing(order)
        self.service.mark_ready(order)
        self.service.complete_order(order)

        # Try to transition completed order
        with self.assertRaises(ValueError):
            self.service.start_preparing(order)


class TestStorageService(unittest.TestCase):
    """Test StorageService functionality."""

    def setUp(self):
        self.test_dir = "data_test"
        self.service = StorageService(self.test_dir)
        self.order_service = OrderService()

    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_save_and_load_orders(self):
        """Test saving and loading orders."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]
        order = self.order_service.create_order("Maria", items, pay_now=True)

        # Save
        self.service.save_orders([order])

        # Load
        loaded_orders = self.service.load_orders()

        self.assertEqual(len(loaded_orders), 1)
        self.assertEqual(loaded_orders[0].customer_name, "Maria")
        self.assertEqual(loaded_orders[0].order_number, "001")
        self.assertEqual(loaded_orders[0].total, 120)

    def test_load_missing_file_returns_empty(self):
        """Test loading when file doesn't exist."""
        orders = self.service.load_orders()
        self.assertEqual(orders, [])

    def test_corrupted_json_returns_empty(self):
        """Test loading corrupted JSON returns empty list."""
        # Create corrupted file
        with open(self.service.orders_file, 'w') as f:
            f.write("{corrupted json")

        orders = self.service.load_orders()
        self.assertEqual(orders, [])

    def test_get_highest_order_number(self):
        """Test getting highest order number from orders."""
        chicken = get_item_by_id("chicken_meal")
        items = [OrderItem(menu_item=chicken, quantity=1)]

        order1 = self.order_service.create_order("Maria", items, True)
        order2 = self.order_service.create_order("Juan", items, True)

        highest = self.service.get_highest_order_number([order1, order2])
        self.assertEqual(highest, 2)

    def test_default_storage_uses_app_data_folder(self):
        """Test default storage path is stable from any launch folder."""
        default_service = StorageService()
        expected_data_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "data")
        )

        self.assertEqual(os.path.abspath(default_service.data_dir), expected_data_dir)


class TestReceiptFormatter(unittest.TestCase):
    """Test required receipt output."""

    def setUp(self):
        self.order_service = OrderService()
        self.workflow_service = WorkflowService()

    def test_receipt_matches_required_single_item_format(self):
        """Test receipt has required labels in the required order."""
        chicken = get_item_by_id("chicken_meal")
        order = self.order_service.create_order(
            "Maria Santos",
            [OrderItem(menu_item=chicken, quantity=1)],
            pay_now=True
        )
        self.workflow_service.start_preparing(order)
        self.workflow_service.mark_ready(order)
        self.workflow_service.complete_order(order)

        receipt = format_receipt(order)

        self.assertEqual(
            receipt,
            "Customer: Maria Santos\n"
            "Order No.: 001\n"
            "Food: Chicken Meal\n"
            "Price: ₱120\n"
            "Payment: PAID\n"
            "Order Status: COMPLETED"
        )

    def test_receipt_shows_multiple_items_with_total(self):
        """Test receipt lists multiple items and keeps the six labels."""
        chicken = get_item_by_id("chicken_meal")
        buko = get_item_by_id("buko_juice")
        order = self.order_service.create_order(
            "Juan Cruz",
            [
                OrderItem(menu_item=chicken, quantity=1),
                OrderItem(menu_item=buko, quantity=2),
            ],
            pay_now=False
        )

        receipt = format_receipt(order)

        self.assertIn("Food:\n  Chicken Meal x1 - ₱120\n  Buko Juice x2 - ₱70", receipt)
        self.assertIn("Price: ₱190", receipt)
        self.assertIn("Payment: UNPAID", receipt)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestOrderService))
    suite.addTests(loader.loadTestsFromTestCase(TestPaymentService))
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowService))
    suite.addTests(loader.loadTestsFromTestCase(TestStorageService))
    suite.addTests(loader.loadTestsFromTestCase(TestReceiptFormatter))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

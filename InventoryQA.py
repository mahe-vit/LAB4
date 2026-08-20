import unittest
import threading
from InventoryManagement import InventorySystem


class InventoryQA(unittest.TestCase):

    def setUp(self):
        self.inventory = InventorySystem()

        self.inventory.add_product(
            "Warehouse A", "Laptop", 50, 10
        )

        self.inventory.add_product(
            "Warehouse B", "Laptop", 30, 10
        )

        self.inventory.add_product(
            "Warehouse C", "Mouse", 20, 5
        )

    # 1. Stock availability
    def test_stock_availability(self):
        self.assertEqual(
            self.inventory.get_total_stock("Laptop"),
            80
        )

    # 2. Insufficient inventory
    def test_insufficient_inventory(self):
        with self.assertRaises(ValueError):
            self.inventory.remove_product(
                "Warehouse A",
                "Laptop",
                100
            )

    # 3. Warehouse transfer
    def test_warehouse_transfer(self):
        self.inventory.transfer_stock(
            "Warehouse A",
            "Warehouse B",
            "Laptop",
            10
        )

        self.assertEqual(
            self.inventory.warehouses["Warehouse A"]["Laptop"],
            40
        )

        self.assertEqual(
            self.inventory.warehouses["Warehouse B"]["Laptop"],
            40
        )

    # 4. Concurrent orders
    def test_concurrent_orders(self):
        inventory = InventorySystem()

        inventory.add_product(
            "Warehouse A",
            "Laptop",
            100
        )

        def order():
            inventory.fulfill_order("Laptop", 10)

        threads = []

        for _ in range(10):
            thread = threading.Thread(target=order)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        self.assertEqual(
            inventory.get_total_stock("Laptop"),
            0
        )

    # 5. Reorder threshold
    def test_reorder_threshold(self):
        self.inventory.remove_product(
            "Warehouse A",
            "Laptop",
            45
        )

        self.assertTrue(
            self.inventory.check_low_stock(
                "Warehouse A",
                "Laptop"
            )
        )

    # 6. Invalid product
    def test_invalid_product(self):
        with self.assertRaises(ValueError):
            self.inventory.remove_product(
                "Warehouse A",
                "Phone",
                5
            )

    # 7. Negative inventory
    def test_negative_inventory(self):
        with self.assertRaises(ValueError):
            self.inventory.add_product(
                "Warehouse A",
                "Laptop",
                -10
            )

    # 8. Multiple warehouses
    def test_multiple_warehouses(self):
        self.assertEqual(
            self.inventory.select_warehouse(
                "Laptop",
                20
            ),
            "Warehouse A"
        )

        self.assertEqual(
            self.inventory.select_warehouse(
                "Mouse",
                10
            ),
            "Warehouse C"
        )


if __name__ == "__main__":
    unittest.main()
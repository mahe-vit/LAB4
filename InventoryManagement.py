import threading


class InventorySystem:
    def __init__(self):
        self.warehouses = {
            "Warehouse A": {},
            "Warehouse B": {},
            "Warehouse C": {}
        }

        self.suppliers = {}
        self.reorder_levels = {}
        self.lock = threading.Lock()

    def add_product(self, warehouse, product, quantity, reorder_level=10):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if quantity < 0:
            raise ValueError("Negative inventory not allowed")

        if not product:
            raise ValueError("Invalid product")

        with self.lock:
            self.warehouses[warehouse][product] = \
                self.warehouses[warehouse].get(product, 0) + quantity

            self.reorder_levels[product] = reorder_level

    def remove_product(self, warehouse, product, quantity):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if product not in self.warehouses[warehouse]:
            raise ValueError("Invalid product")

        if quantity < 0:
            raise ValueError("Negative quantity not allowed")

        with self.lock:
            if self.warehouses[warehouse][product] < quantity:
                raise ValueError("Insufficient inventory")

            self.warehouses[warehouse][product] -= quantity

    def transfer_stock(self, source, destination, product, quantity):
        if source not in self.warehouses or destination not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if quantity < 0:
            raise ValueError("Negative quantity not allowed")

        with self.lock:
            if product not in self.warehouses[source]:
                raise ValueError("Invalid product")

            if self.warehouses[source][product] < quantity:
                raise ValueError("Insufficient inventory")

            self.warehouses[source][product] -= quantity
            self.warehouses[destination][product] = \
                self.warehouses[destination].get(product, 0) + quantity

    def add_supplier(self, supplier, products):
        if not supplier:
            raise ValueError("Invalid supplier")

        self.suppliers[supplier] = products

    def check_low_stock(self, warehouse, product):
        if warehouse not in self.warehouses:
            raise ValueError("Invalid warehouse")

        if product not in self.warehouses[warehouse]:
            raise ValueError("Invalid product")

        quantity = self.warehouses[warehouse][product]
        reorder_level = self.reorder_levels.get(product, 10)

        return quantity <= reorder_level

    def reorder(self, warehouse, product, quantity):
        if quantity <= 0:
            raise ValueError("Invalid reorder quantity")

        self.add_product(
            warehouse,
            product,
            quantity,
            self.reorder_levels.get(product, 10)
        )

    def get_total_stock(self, product):
        total = 0

        for warehouse in self.warehouses.values():
            total += warehouse.get(product, 0)

        return total

    def select_warehouse(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Invalid order quantity")

        for warehouse_name, inventory in self.warehouses.items():
            if inventory.get(product, 0) >= quantity:
                return warehouse_name

        return None

    def fulfill_order(self, product, quantity):
        warehouse = self.select_warehouse(product, quantity)

        if warehouse is None:
            raise ValueError("Insufficient inventory")

        self.remove_product(warehouse, product, quantity)

        return warehouse


if __name__ == "__main__":
    inventory = InventorySystem()

    inventory.add_product("Warehouse A", "Laptop", 50, 10)
    inventory.add_product("Warehouse B", "Laptop", 30, 10)
    inventory.add_product("Warehouse C", "Mouse", 20, 5)

    inventory.add_supplier("Supplier A", ["Laptop", "Mouse"])

    selected = inventory.select_warehouse("Laptop", 20)
    print("Selected Warehouse:", selected)

    fulfilled = inventory.fulfill_order("Laptop", 20)
    print("Order fulfilled from:", fulfilled)

    print("Total Laptop Stock:",
          inventory.get_total_stock("Laptop"))

    print("Laptop low stock:",
          inventory.check_low_stock("Warehouse A", "Laptop"))
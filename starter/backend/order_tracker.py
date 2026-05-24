# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.

class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """
    def __init__(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(f"Storage object must implement a callable '{method}' method.")
        self.storage = storage

    def add_order(
            self,
            order_id: str,
            item_name: str,
            quantity: int,
            customer_id: str,
            status: str = "pending"
        ) -> dict[str, str | int]:
        if self.storage.get_order(order_id):
            raise ValueError(f"Order with ID '{order_id}' already exists.")

        order = {
            "order_id": order_id,
            "item_name": item_name,
            "quantity": quantity,
            "customer_id": customer_id,
            "status": status
        }
        self.storage.save_order(order_id=order_id, order_data=order)

    def get_order_by_id(self, order_id: str) -> dict[str, str | int]:
        return self.storage.get_order(order_id=order_id)

    def update_order_status(self, order_id: str, new_status: str) -> dict[str, str | int]:
        if not new_status or new_status not in ["pending", "processing", "shipped"]:
            raise ValueError(f"Invalid status update (Value: '{new_status}')")
        existing = self.get_order_by_id(order_id=order_id)
        if not existing:
            raise KeyError(f"Order '{order_id}' not found")        
        return self.storage.save_order(
            order_id=order_id,
            order_data={
                **existing,
                "status": new_status
            }
        )

    def list_all_orders(self) -> dict[str, dict[str, str | int]]:
        return self.storage.get_all_orders()

    def list_orders_by_status(self, status: str) -> dict[str, dict[str, str | int]]:
        if not status:
            raise ValueError(f"status is invalid. value: {status}")
        orders = self.storage.get_all_orders()
        return {
            key: order
            for key, order in orders.items() if order.get("status") == status.lower()
        }

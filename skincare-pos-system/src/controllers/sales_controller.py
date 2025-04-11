from src.models.transaction import Transaction

class SalesController:
    def __init__(self, product_controller, file_handler):
        self.product_controller = product_controller
        self.file_handler = file_handler

    def process_sale(self, cart_items):
        products = []
        quantities = []
        total_amount = 0

        for product_id, quantity in cart_items:
            if product_id < 0 or product_id >= len(self.product_controller.products):
                raise ValueError(f"Invalid product ID: {product_id}")

            product = self.product_controller.products[product_id]
            if product.quantity < quantity:
                raise ValueError(f"Insufficient stock for {product.name}")

            # Apply "Buy 3 Get 1 Free" promotion
            paid_quantity = quantity - (quantity // 4)
            total_amount += product.selling_price * paid_quantity

            products.append(product)
            quantities.append(quantity)
            
            # Update inventory
            self.product_controller.update_product_quantity(product_id, -quantity)

        # Create and save transaction
        transaction = Transaction(products, quantities, total_amount)
        self.file_handler.save_invoice(transaction)
        return transaction
import json
import os
from src.models.product import Product

class FileHandler:
    def __init__(self, inventory_file="data/inventory.txt"):
        self.inventory_file = inventory_file

    def read_inventory(self):
        try:
            with open(self.inventory_file, 'r') as file:
                data = json.load(file)
                return [Product.from_dict(item) for item in data]
        except FileNotFoundError:
            return []

    def write_inventory(self, products):
        with open(self.inventory_file, 'w') as file:
            json.dump([p.to_dict() for p in products], file, indent=4)

    def save_invoice(self, transaction, is_sale=True):
        folder = "invoices/sales" if is_sale else "invoices/restock"
        os.makedirs(folder, exist_ok=True)
        
        filename = f"{folder}/invoice_{transaction.transaction_id}.txt"
        with open(filename, 'w') as file:
            file.write(f"{'='*50}\n")
            file.write(f"WeCare Skin Care Products\n")
            file.write(f"Transaction ID: {transaction.transaction_id}\n")
            file.write(f"Date: {transaction.date.strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"{'='*50}\n\n")
            
            for i, product in enumerate(transaction.products):
                file.write(f"Product: {product.name}\n")
                file.write(f"Quantity: {transaction.quantities[i]}\n")
                file.write(f"Price per unit: ${product.selling_price:.2f}\n")
                file.write(f"{'-'*30}\n")
            
            file.write(f"\nTotal Amount: ${transaction.total_amount:.2f}\n")
            if is_sale:
                file.write("\nPromotion Applied: Buy 3 Get 1 Free\n")
            file.write(f"{'='*50}\n")
import json
import os
from datetime import datetime, timedelta
from collections import deque

class InventorySystem:
    def __init__(self):
        self.items_file = "data/items.txt"
        self.stock_in_file = "data/stock_in.txt"
        self.stock_out_file = "data/stock_out.txt"
        self.expired_file = "data/expired.txt"
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        if not os.path.exists("data"):
            os.makedirs("data")
            
    def load_data(self, filename):
        if not os.path.exists(filename):
            return []
            
        try:
            with open(filename, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
                
    def save_data(self, filename, data):
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
            
    def get_next_id(self, data):
        if not data:
            return 1
        return max(item["id"] for item in data) + 1
        
    # CRUD Operations
    def get_all_items(self):
        return self.load_data(self.items_file)
        
    def get_item(self, item_id):
        items = self.load_data(self.items_file)
        for item in items:
            if item["id"] == item_id:
                return item
        return None
        
def add_item(self, name, category, stock, unit, created_date, expiry_date, min_stock=10):
    items = self.load_data(self.items_file)
    
    new_item = {
        "id": self.get_next_id(items),
        "name": name,
        "category": category,
        "stock": stock,
        "unit": unit,
        "created_date": created_date,
        "expiry_date": expiry_date,
        "min_stock": min_stock  # Default minimum stock level
    }
    
    items.append(new_item)
    self.save_data(self.items_file, items)
    return True
    def update_item(self, item_id, name, category, stock, unit, created_date, expiry_date, min_stock=10):
        items = self.load_data(self.items_file)
        
        for item in items:
            if item["id"] == item_id:
                item["name"] = name
                item["category"] = category
                item["stock"] = stock
                item["unit"] = unit
                item["created_date"] = created_date
                item["expiry_date"] = expiry_date
                item["min_stock"] = min_stock
                
                self.save_data(self.items_file, items)
                return True
                
        return False
        
    def delete_item(self, item_id):
        items = self.load_data(self.items_file)
        
        for i, item in enumerate(items):
            if item["id"] == item_id:
                del items[i]
                self.save_data(self.items_file, items)
                return True
                
        return False
    
    # Stock In Operations
    def stock_in(self, item_id, quantity, date, supplier="", notes=""):
        items = self.load_data(self.items_file)
        stock_in = self.load_data(self.stock_in_file)
        
        for item in items:
            if item["id"] == item_id:
                item["stock"] += quantity
                
                # Add to stock in transactions
                new_transaction = {
                    "id": self.get_next_id(stock_in),
                    "item_id": item_id,
                    "item_name": item["name"],
                    "quantity": quantity,
                    "date": date,
                    "supplier": supplier,
                    "notes": notes,
                    "unit_price": 0,  # Can be extended for price tracking
                    "total_price": 0   # Can be extended for price tracking
                }
                
                stock_in.append(new_transaction)
                
                self.save_data(self.items_file, items)
                self.save_data(self.stock_in_file, stock_in)
                return True
                
        return False
        
    def get_stock_in_transactions(self, item_id=None, start_date=None, end_date=None):
        transactions = self.load_data(self.stock_in_file)
        
        # Filter transactions if parameters provided
        if item_id:
            transactions = [t for t in transactions if t["item_id"] == item_id]
            
        if start_date:
            transactions = [t for t in transactions if t["date"] >= start_date]
            
        if end_date:
            transactions = [t for t in transactions if t["date"] <= end_date]
            
        return transactions
    
    # Stock Out Operations with FIFO/LIFO
    def stock_out(self, item_id, quantity, method, date, customer="", notes=""):
        items = self.load_data(self.items_file)
        stock_out = self.load_data(self.stock_out_file)
        
        for item in items:
            if item["id"] == item_id:
                if item["stock"] < quantity:
                    return False, "Stok tidak mencukupi"
                    
                # Apply FIFO or LIFO based on method
                if method.upper() == "FIFO":
                    success = self.apply_fifo(item_id, quantity)
                elif method.upper() == "LIFO":
                    success = self.apply_lifo(item_id, quantity)
                else:
                    return False, "Metode tidak valid"
                
                if not success:
                    return False, "Gagal memproses stok keluar"
                
                item["stock"] -= quantity
                
                # Add to stock out transactions
                new_transaction = {
                    "id": self.get_next_id(stock_out),
                    "item_id": item_id,
                    "item_name": item["name"],
                    "quantity": quantity,
                    "method": method,
                    "date": date,
                    "customer": customer,
                    "notes": notes,
                    "unit_price": 0,  # Can be extended for price tracking
                    "total_price": 0   # Can be extended for price tracking
                }
                
                stock_out.append(new_transaction)
                
                self.save_data(self.items_file, items)
                self.save_data(self.stock_out_file, stock_out)
                return True, "Stok keluar berhasil"
                
        return False, "Barang tidak ditemukan"
        
    def get_stock_out_transactions(self, item_id=None, start_date=None, end_date=None):
        transactions = self.load_data(self.stock_out_file)
        
        # Filter transactions if parameters provided
        if item_id:
            transactions = [t for t in transactions if t["item_id"] == item_id]
            
        if start_date:
            transactions = [t for t in transactions if t["date"] >= start_date]
            
        if end_date:
            transactions = [t for t in transactions if t["date"] <= end_date]
            
        return transactions
    
    # FIFO Implementation
    def apply_fifo(self, item_id, quantity):
        """First In First Out - barang yang pertama masuk akan pertama keluar"""
        stock_in = self.load_data(self.stock_in_file)
        item_stock_in = [t for t in stock_in if t["item_id"] == item_id and t["quantity"] > 0]
        
        # Sort by date (oldest first)
        item_stock_in.sort(key=lambda x: x["date"])
        
        remaining = quantity
        for transaction in item_stock_in:
            if remaining <= 0:
                break
                
            available = transaction["quantity"]
            if available >= remaining:
                transaction["quantity"] -= remaining
                remaining = 0
            else:
                remaining -= available
                transaction["quantity"] = 0
        
        # Update stock in transactions
        for t in stock_in:
            for updated_t in item_stock_in:
                if t["id"] == updated_t["id"]:
                    t["quantity"] = updated_t["quantity"]
        
        self.save_data(self.stock_in_file, stock_in)
        return remaining == 0
    
    # LIFO Implementation  
    def apply_lifo(self, item_id, quantity):
        """Last In First Out - barang yang terakhir masuk akan pertama keluar"""
        stock_in = self.load_data(self.stock_in_file)
        item_stock_in = [t for t in stock_in if t["item_id"] == item_id and t["quantity"] > 0]
        
        # Sort by date (newest first)
        item_stock_in.sort(key=lambda x: x["date"], reverse=True)
        
        remaining = quantity
        for transaction in item_stock_in:
            if remaining <= 0:
                break
                
            available = transaction["quantity"]
            if available >= remaining:
                transaction["quantity"] -= remaining
                remaining = 0
            else:
                remaining -= available
                transaction["quantity"] = 0
        
        # Update stock in transactions
        for t in stock_in:
            for updated_t in item_stock_in:
                if t["id"] == updated_t["id"]:
                    t["quantity"] = updated_t["quantity"]
        
        self.save_data(self.stock_in_file, stock_in)
        return remaining == 0
    
    # Reporting Functions
    def generate_sales_report(self, start_date=None, end_date=None):
        """Generate sales report with total and average sales"""
        transactions = self.load_data(self.stock_out_file)
        
        # Filter by date range
        if start_date:
            transactions = [t for t in transactions if t["date"] >= start_date]
        if end_date:
            transactions = [t for t in transactions if t["date"] <= end_date]
            
        # Calculate sales per item
        sales_data = {}
        for trans in transactions:
            item_name = trans["item_name"]
            if item_name not in sales_data:
                sales_data[item_name] = {
                    "total_sold": 0,
                    "transaction_count": 0,
                    "dates": set()
                }
            
            sales_data[item_name]["total_sold"] += trans["quantity"]
            sales_data[item_name]["transaction_count"] += 1
            sales_data[item_name]["dates"].add(trans["date"])
        
        # Prepare report
        report = []
        for item_name, data in sales_data.items():
            days_count = len(data["dates"]) if data["dates"] else 1
            average_per_day = data["total_sold"] / days_count if days_count > 0 else 0
            
            report.append({
                "item_name": item_name,
                "total_sold": data["total_sold"],
                "transaction_count": data["transaction_count"],
                "average_per_day": round(average_per_day, 2),
                "days_count": days_count
            })
        
        return report
    
    def generate_stock_report(self):
        """Generate current stock status report"""
        items = self.load_data(self.items_file)
        
        report = {
            "total_items": len(items),
            "total_stock_value": 0,  # Would need price data
            "low_stock_items": [],
            "out_of_stock_items": [],
            "category_summary": {}
        }
        
        for item in items:
            # Check low stock
            if item["stock"] <= item.get("min_stock", 10):
                report["low_stock_items"].append(item)
            
            # Check out of stock
            if item["stock"] == 0:
                report["out_of_stock_items"].append(item)
            
            # Category summary
            category = item["category"]
            if category not in report["category_summary"]:
                report["category_summary"][category] = {
                    "count": 0,
                    "total_stock": 0
                }
            
            report["category_summary"][category]["count"] += 1
            report["category_summary"][category]["total_stock"] += item["stock"]
        
        return report
    
    def generate_expiry_report(self, days_threshold=30):
        """Generate report for items nearing expiry"""
        items = self.load_data(self.items_file)
        today = datetime.now().date()
        
        expiring_soon = []
        expired = []
        
        for item in items:
            try:
                expiry_date = datetime.strptime(item["expiry_date"], "%Y-%m-%d").date()
                days_until_expiry = (expiry_date - today).days
                
                if days_until_expiry < 0:
                    expired.append({
                        **item,
                        "days_until_expiry": days_until_expiry
                    })
                elif days_until_expiry <= days_threshold:
                    expiring_soon.append({
                        **item,
                        "days_until_expiry": days_until_expiry
                    })
            except (ValueError, KeyError):
                continue
        
        return {
            "expired": expired,
            "expiring_soon": expiring_soon,
            "threshold_days": days_threshold
        }
    
    def get_inventory_value(self):
        """Calculate total inventory value (requires price data)"""
        # This would need to be implemented with actual pricing data
        return 0
    
    def get_top_selling_items(self, limit=10, start_date=None, end_date=None):
        """Get top selling items by quantity"""
        report = self.generate_sales_report(start_date, end_date)
        report.sort(key=lambda x: x["total_sold"], reverse=True)
        return report[:limit]
    
    def get_stock_movement(self, item_id, days=30):
        """Get stock movement history for an item"""
        today = datetime.now().date()
        start_date = (today - timedelta(days=days)).strftime("%Y-%m-%d")
        
        stock_ins = self.get_stock_in_transactions(item_id, start_date)
        stock_outs = self.get_stock_out_transactions(item_id, start_date)
        
        # Combine and sort by date
        movements = []
        for movement in stock_ins:
            movements.append({
                **movement,
                "type": "in",
                "movement_date": movement["date"]
            })
        
        for movement in stock_outs:
            movements.append({
                **movement,
                "type": "out", 
                "movement_date": movement["date"]
            })
        
        movements.sort(key=lambda x: x["movement_date"])
        return movements
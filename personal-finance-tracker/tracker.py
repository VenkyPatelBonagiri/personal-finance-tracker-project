import json
import os
from datetime import datetime
import requests

class Transaction:
    def __init__(self, amount, category, trans_type, currency="EUR", date=None):
        self.amount = float(amount)
        self.category = category
        self.trans_type = trans_type  # "income" or "expense"
        self.currency = currency
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "type": self.trans_type,
            "currency": self.currency,
            "date": self.date,
        }


class FinanceTracker:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(BASE_DIR, "data", "transactions.json")
    BASE_CURRENCY = "EUR"
    API_URL = "https://api.frankfurter.app/latest"

    def __init__(self):
        self.transactions = []
        self.load_transactions()

    def load_transactions(self):
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    data = json.load(f)
                    self.transactions = data
            except json.JSONDecodeError:
                print("Error reading transactions file. Starting fresh.")
                self.transactions = []
        else:
            self.transactions = []

    def save_transactions(self):
        os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
        with open(self.DATA_FILE, "w") as f:
            json.dump(self.transactions, f, indent=4)

    def convert_currency(self, amount, from_currency):
        """Convert amount to BASE_CURRENCY using Frankfurter API."""
        if from_currency == self.BASE_CURRENCY:
            return amount
        try:
            response = requests.get(
                f"{self.API_URL}?amount={amount}&from={from_currency}&to={self.BASE_CURRENCY}"
            )
            data = response.json()
            converted = data["rates"].get(self.BASE_CURRENCY)
            return converted if converted else amount
        except Exception as e:
            print(f"Currency conversion failed: {e}")
            return amount  # fallback

    def add_transaction(self, transaction):
        converted_amount = self.convert_currency(transaction.amount, transaction.currency)
        transaction.amount = converted_amount
        transaction.currency = self.BASE_CURRENCY
        self.transactions.append(transaction.to_dict())
        self.save_transactions()

    def get_by_category(self):
        categories = {}
        for t in self.transactions:
            categories[t["category"]] = categories.get(t["category"], 0) + t["amount"]
        return categories
    
    def get_balance(self):
        income = sum(t["amount"] for t in self.transactions if t["type"] == "income")
        expenses = sum(t["amount"] for t in self.transactions if t["type"] == "expense")
        return income - expenses
    
    def get_total_expenses(self):
        return round(sum(t["amount"] for t in self.transactions if t["type"] == "expense"), 2)

    
    


from utils.calculator import Calculator
from typing import List
from langchain.tools import tool
import re

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        @tool
        def estimate_total_hotel_cost(price_per_night:str, total_days:float) -> float:
            """Calculate total hotel cost"""
            price = float(re.sub(r"[^\d.]", "", price_per_night))
            days = float(total_days)
            return self.calculator.multiply(price, days)

        
        @tool
        def calculate_total_expense(costs: float) -> float:
            """Calculate total expense of the trip"""
            cleaned_costs = [float(re.sub(r"[^\d.]", "", str(c))) for c in costs]
            return self.calculator.calculate_total(cleaned_costs)
        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            total = float(re.sub(r"[^\d.]", "", str(total_cost)))
            days = int(days)
            return self.calculator.calculate_daily_budget(total, days)
        
        return [estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]
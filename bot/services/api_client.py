import logging
import aiohttp

from datetime import date
from config import settings

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.base_url = settings.api_url
    
    async def _make_request(self, method, endpoint, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self.base_url}{endpoint}", **kwargs) as response:
                return await response.json()
    
    async def get_expenses(self, start_date: date = None, end_date: date = None):
        params = {}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()

        
        return await self._make_request("GET", "/expenses", params=params)
    
    async def get_expenses_report(self, start_date: date = None, end_date: date = None):
        params = {}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/expenses/report/", params=params) as response:
                if response.status == 404:
                    logger.info("--------------------------------")
                    logger.info("404 Error: No expenses found")
                    logger.info("--------------------------------")
                    return None
                return await response.read()
    
    async def create_expense(self, name: str, date: date, amount: float):
        data = {
            "name": name,
            "date": date.isoformat(),
            "amount_uah": amount
        }
        return await self._make_request("POST", "/expenses/", json=data)
    
    async def delete_expense(self, expense_id: int):
        response = await self._make_request("DELETE", f"/expenses/{expense_id}")
        return isinstance(response, dict) and response.get("message") == "Expense deleted successfully"
    
    async def update_expense(self, expense_id: int, name: str, amount: float):
        data = {
            "name": name,
            "date": date.today().isoformat(),
            "amount_uah": amount
        }
        return await self._make_request("PUT", f"/expenses/{expense_id}", json=data)
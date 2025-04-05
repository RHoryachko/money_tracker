import logging
import aiohttp

from datetime import date
from config import settings

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.base_url = settings.api_url
        self.api_secret_key = settings.api_secret_key
    
    async def _make_request(self, method, endpoint, **kwargs):
        headers = kwargs.get('headers', {})
        headers['X-API-Key'] = self.api_secret_key
        kwargs['headers'] = headers
        
        # Remove None values from params
        if 'params' in kwargs:
            kwargs['params'] = {k: v for k, v in kwargs['params'].items() if v is not None}
            
        async with aiohttp.ClientSession() as session:
            async with session.request(method, f"{self.base_url}{endpoint}", **kwargs) as response:
                return await response.json()
    
    async def get_expenses(self, user_id: int, start_date: date = None, end_date: date = None):
        params = {'user_id': user_id}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        return await self._make_request("GET", "/expenses", params=params)
    
    async def get_expenses_report(self, user_id: int, start_date: date = None, end_date: date = None):
        params = {'user_id': user_id}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        async with aiohttp.ClientSession() as session:
            headers = {'X-API-Key': self.api_secret_key}
            # Remove None values from params
            params = {k: v for k, v in params.items() if v is not None}
            async with session.get(f"{self.base_url}/expenses/report/", params=params, headers=headers) as response:
                if response.status == 404:
                    logger.info("--------------------------------")
                    logger.info("404 Error: No expenses found")
                    logger.info("--------------------------------")
                    return None
                return await response.read()
    
    async def create_expense(self, user_id: int, name: str, date: date, amount: float):
        data = {
            "user_id": user_id,
            "name": name,
            "date": date.isoformat(),
            "amount_uah": amount
        }
        return await self._make_request("POST", "/expenses/", json=data)
    
    async def delete_expense(self, user_id: int, expense_id: int):
        return await self._make_request("DELETE", f"/expenses/{expense_id}", params={'user_id': user_id})
    
    async def update_expense(self, user_id: int, expense_id: int, name: str, amount: float):
        data = {
            "user_id": user_id,
            "name": name,
            "date": date.today().isoformat(),
            "amount_uah": amount
        }
        return await self._make_request("PUT", f"/expenses/{expense_id}", json=data)
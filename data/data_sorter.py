import pandas as pd  
import os
from supabase import create_client, Client
# getting started

class DataSorter:
    def __init__(self) -> None:  
        
        url: str = "https://wrqkgoneqnrpavieozoa.supabase.co"
        self.supabase = create_client(url, os.environ.get("SUPABASE_KEY"))
        self.price_data = self.fetch_all_rows(self.supabase, "direx-db")


    def filter_by_strings(self, string_list: list) -> pd.DataFrame:
        mask = self.price_data['ticker'].isin(string_list)
        return self.price_data[mask]

    @staticmethod
    def fetch_all_rows(supabase: Client, table_name: str, batch_size: int = 1000) -> pd.DataFrame:
        all_rows = []
        offset = 0
        has_more = True

        while has_more:
            response = supabase.table(table_name).select("*").range(offset, offset + batch_size - 1).order('index').execute()

            data = response.data
            if data and len(data) > 0:
                all_rows.extend(data)
                offset += batch_size
            else:
                has_more = False

        return pd.DataFrame(all_rows)

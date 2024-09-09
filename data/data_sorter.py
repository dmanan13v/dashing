import pandas as pd  
import os

# getting started

class DataSorter:
    def __init__(self) -> None:  
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.price_data = pd.read_csv(
            os.path.join(current_dir, "combined_df.csv")
        )

    def filter_by_strings(self, string_list: list) -> pd.DataFrame:
        mask = self.price_data['ticker'].isin(string_list)
        return self.price_data[mask]
    

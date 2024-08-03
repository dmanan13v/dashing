import pandas as pd  # type: ignore
import os

# getting started

class DataSorter:
    def __init__(self) -> None:  # why typing?
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.price_data = pd.read_csv(
            os.path.join(current_dir, "data", "combined_df.csv")
        )

    def filter_by_strings(self, string_list: list) -> pd.DataFrame:
        """
        Create a mask for the DataFrame based on string values in a specific column.
        
        Args:
        column_name (str): The name of the column to filter on.
        string_list (list): A list of strings to match against.
        
        Returns:
        pandas.DataFrame: A new DataFrame containing only the rows that match the condition.
        """
        # Create a boolean mask where the column values are in the string_list
        mask = self.price_data['ticker'].isin(string_list)
        
        # Return the DataFrame with only the rows that satisfy the condition
        return self.price_data[mask]
    


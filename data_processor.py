"""Data processing and analysis functionality"""
import pandas as pd
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import concurrent.futures
from config import SHEET_CONFIG
from data_validator import DataValidator
from cache_manager import CacheManager

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.sheets_data: Dict[str, pd.DataFrame] = {}
        self.validator = DataValidator()
        self.cache_manager = CacheManager()

    def load_data(self) -> Tuple[bool, str]:
        """Load all sheets in parallel using ThreadPoolExecutor"""
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    executor.submit(self._load_sheet, sheet_name): sheet_name 
                    for sheet_name in SHEET_CONFIG.keys()
                }
                
                success = True
                error_message = ""
                
                for future in concurrent.futures.as_completed(futures):
                    sheet_name = futures[future]
                    try:
                        df = future.result()
                        if df is not None:
                            self.sheets_data[sheet_name] = self.cache_manager.cache_dataframe(df, sheet_name)
                    except Exception as e:
                        success = False
                        error_message = f"Error loading sheet {sheet_name}: {str(e)}"
                        logger.error(error_message)
                
                return success, error_message
                
        except Exception as e:
            error_message = f"Error loading data: {str(e)}"
            logger.error(error_message)
            return False, error_message

    def _load_sheet(self, sheet_name: str) -> Optional[pd.DataFrame]:
        """Load and validate a single sheet"""
        try:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            
            # Validate sheet structure
            config = SHEET_CONFIG[sheet_name]
            if not self.validator.validate_required_columns(df, [config['date_column']] + config['value_columns']):
                logger.error(f"Missing required columns in {sheet_name}")
                return None
                
            return self._preprocess_sheet(df, sheet_name)
        except Exception as e:
            logger.error(f"Failed to load sheet {sheet_name}: {e}")
            return None

    def _preprocess_sheet(self, df: pd.DataFrame, sheet_name: str) -> pd.DataFrame:
        """Preprocess sheet data with validation and cleaning"""
        config = SHEET_CONFIG[sheet_name]
        
        # Validate and convert date column
        date_col = config['date_column']
        if self.validator.validate_date_column(df, date_col):
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        
        # Validate and convert numeric columns
        numeric_validation = self.validator.validate_numeric_columns(df, config['value_columns'])
        for col, is_valid in numeric_validation.items():
            if is_valid:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Drop rows with missing critical data
        critical_columns = [date_col] + config['value_columns']
        df = df.dropna(subset=critical_columns)
        
        return df

    def filter_by_date(self, start_date: datetime, end_date: datetime) -> None:
        """Apply date filter to all sheets"""
        for sheet_name, df in self.sheets_data.items():
            date_col = SHEET_CONFIG[sheet_name]['date_column']
            mask = (df[date_col].dt.date >= start_date.date()) & (df[date_col].dt.date <= end_date.date())
            filtered_df = df[mask]
            self.sheets_data[sheet_name] = self.cache_manager.cache_dataframe(filtered_df, f"{sheet_name}_filtered")

    def get_sheet_data(self, sheet_name: str) -> Optional[pd.DataFrame]:
        """Safely retrieve sheet data"""
        return self.sheets_data.get(sheet_name)
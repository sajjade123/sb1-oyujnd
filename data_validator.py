"""Data validation functionality"""
import pandas as pd
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DataValidator:
    @staticmethod
    def validate_date_column(df: pd.DataFrame, date_column: str) -> bool:
        """Validate date column format and values"""
        try:
            if date_column not in df.columns:
                return False
            pd.to_datetime(df[date_column], errors='raise')
            return True
        except Exception as e:
            logger.error(f"Date validation error: {e}")
            return False

    @staticmethod
    def validate_numeric_columns(df: pd.DataFrame, numeric_columns: List[str]) -> Dict[str, bool]:
        """Validate numeric columns"""
        results = {}
        for col in numeric_columns:
            try:
                if col not in df.columns:
                    results[col] = False
                    continue
                pd.to_numeric(df[col], errors='raise')
                results[col] = True
            except Exception as e:
                logger.error(f"Numeric validation error in column {col}: {e}")
                results[col] = False
        return results

    @staticmethod
    def validate_required_columns(df: pd.DataFrame, required_columns: List[str]) -> bool:
        """Validate presence of required columns"""
        return all(col in df.columns for col in required_columns)
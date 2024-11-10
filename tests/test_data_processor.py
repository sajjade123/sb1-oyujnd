"""Tests for data processing functionality"""
import pytest
import pandas as pd
from datetime import datetime
from data_processor import DataProcessor

@pytest.fixture
def processor():
    return DataProcessor("test_data.xlsx")

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'ReceivedDate': ['2023-01-01', '2023-01-02'],
        'Value$': [100, 200],
        'ValueinAED': [367, 734],
        'Reference': ['REF1', 'REF2']
    })

def test_preprocess_sheet(processor, sample_df):
    sheet_name = 'Manual Orders Not Invoiced'
    processed_df = processor._preprocess_sheet(sample_df, sheet_name)
    
    assert not processed_df.empty
    assert pd.api.types.is_datetime64_any_dtype(processed_df['ReceivedDate'])
    assert pd.api.types.is_numeric_dtype(processed_df['Value$'])
    assert pd.api.types.is_numeric_dtype(processed_df['ValueinAED'])

def test_filter_by_date(processor, sample_df):
    sheet_name = 'Manual Orders Not Invoiced'
    processor.sheets_data[sheet_name] = sample_df
    
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 1)
    
    processor.filter_by_date(start_date, end_date)
    filtered_df = processor.sheets_data[sheet_name]
    
    assert len(filtered_df) == 1
    assert filtered_df.iloc[0]['Value$'] == 100
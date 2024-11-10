"""Tests for data validation functionality"""
import pytest
import pandas as pd
from data_validator import DataValidator

@pytest.fixture
def validator():
    return DataValidator()

@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'date_col': ['2023-01-01', '2023-01-02'],
        'numeric_col': [100, 200],
        'text_col': ['a', 'b']
    })

def test_validate_date_column(validator, sample_df):
    assert validator.validate_date_column(sample_df, 'date_col') == True
    assert validator.validate_date_column(sample_df, 'numeric_col') == False
    assert validator.validate_date_column(sample_df, 'missing_col') == False

def test_validate_numeric_columns(validator, sample_df):
    results = validator.validate_numeric_columns(sample_df, ['numeric_col', 'text_col'])
    assert results['numeric_col'] == True
    assert results['text_col'] == False

def test_validate_required_columns(validator, sample_df):
    assert validator.validate_required_columns(sample_df, ['date_col', 'numeric_col']) == True
    assert validator.validate_required_columns(sample_df, ['missing_col']) == False
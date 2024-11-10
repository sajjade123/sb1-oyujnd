"""Configuration settings for the dashboard"""

THEME_COLORS = {
    'primary': '#2E7D32',
    'secondary': '#212121',
    'background': '#FFFFFF',
    'accent': '#4CAF50'
}

SHEET_CONFIG = {
    'Manual Orders Not Invoiced': {
        'date_column': 'ReceivedDate',
        'value_columns': ['Value$', 'ValueinAED'],
        'key_columns': ['Reference', 'Partner', 'SO#', 'AutodeskOrder#', 'End-UserDetails'],
        'filter_columns': ['Partner', 'PDCstatus']
    },
    'Online Orders Not Invoiced': {
        'date_column': 'ReceivedDate',
        'value_columns': ['Value$', 'ValueinAED'],
        'key_columns': ['OrderID', 'Partner', 'EndCustomerCompany', 'SO', 'Invoice#'],
        'filter_columns': ['Partner', 'PDCstatus']
    },
    'Online-Invoiced orders': {
        'date_column': 'ReceivedDate',
        'value_columns': ['Value$', 'ValueinAED'],
        'key_columns': ['OrderID', 'Partner', 'EndCustomerCompany', 'SO', 'Invoice#'],
        'filter_columns': ['Partner', 'PDCstatus']
    },
    'Manual Orders-Invoiced': {
        'date_column': 'ReceivedDate',
        'value_columns': ['Value$', 'ValueinAED'],
        'key_columns': ['Reference', 'Partner', 'SO#', 'Invoice#', 'AutodeskOrder#', 'End-UserDetails'],
        'filter_columns': ['Partner', 'PDCstatus']
    }
}

CSS_STYLES = """
<style>
    .reportview-container { background: #f0f2f6 }
    .main { background: #f0f2f6 }
    .stmetric-container {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #2E7D32;
    }
    .stSelectbox label {
        font-size: 16px;
        font-weight: 500;
    }
    .plot-container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
</style>
"""
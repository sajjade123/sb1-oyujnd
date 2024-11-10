"""Analytics functionality for the dashboard"""
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List
from config import THEME_COLORS

def analyze_trends(df: pd.DataFrame, date_column: str, value_columns: List[str]) -> Dict:
    """Analyze trends with improved error handling and validation"""
    trends = {}
    
    for value_col in value_columns:
        if value_col not in df.columns:
            continue
            
        monthly_data = df.groupby(pd.Grouper(key=date_column, freq='M'))[value_col].agg(['sum', 'mean', 'count'])
        monthly_data['growth_rate'] = monthly_data['sum'].pct_change() * 100
        monthly_data['3_month_ma'] = monthly_data['sum'].rolling(window=3, min_periods=1).mean()
        trends[value_col] = monthly_data
        
    return trends

def create_trend_plot(trends_data: pd.DataFrame, value_column: str) -> go.Figure:
    """Create an enhanced trend visualization"""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=trends_data.index,
        y=trends_data['sum'],
        name='Monthly Total',
        marker_color=THEME_COLORS['primary']
    ))
    
    fig.add_trace(go.Scatter(
        x=trends_data.index,
        y=trends_data['3_month_ma'],
        name='3-Month Moving Average',
        line=dict(color=THEME_COLORS['accent'], width=2)
    ))
    
    fig.update_layout(
        title=f'{value_column} Trends Over Time',
        template='plotly_white',
        showlegend=True,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_distribution_plot(df: pd.DataFrame, value_column: str) -> go.Figure:
    """Create an enhanced distribution visualization"""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df[value_column],
        nbinsx=30,
        name='Distribution',
        marker_color=THEME_COLORS['primary']
    ))
    
    fig.update_layout(
        title=f'{value_column} Distribution',
        template='plotly_white',
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title=value_column,
        yaxis_title='Frequency'
    )
    
    return fig

def generate_summary_stats(df: pd.DataFrame, value_columns: List[str]) -> Dict:
    """Generate comprehensive summary statistics"""
    summary = {}
    
    for col in value_columns:
        if col not in df.columns:
            continue
            
        summary[col] = {
            'total': df[col].sum(),
            'average': df[col].mean(),
            'median': df[col].median(),
            'min': df[col].min(),
            'max': df[col].max(),
            'std_dev': df[col].std(),
            'count': df[col].count()
        }
    
    return summary
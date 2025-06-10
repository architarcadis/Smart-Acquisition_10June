import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def apply_cross_chart_filter(df, filter_type=None, filter_value=None):
    """Apply filtering to dataframe based on current filter state"""
    if not st.session_state.get('filter_active', False) or not filter_type or not filter_value:
        return df
    
    filtered_df = df.copy()
    
    if filter_type == 'rag_status' and 'rag_status' in df.columns:
        filtered_df = filtered_df[filtered_df['rag_status'] == filter_value]
    elif filter_type == 'procurement_category' and 'procurement_category' in df.columns:
        filtered_df = filtered_df[filtered_df['procurement_category'] == filter_value]
    elif filter_type == 'supplier' and 'supplier' in df.columns:
        filtered_df = filtered_df[filtered_df['supplier'] == filter_value]
    elif filter_type == 'risk_level' and 'risk_level' in df.columns:
        filtered_df = filtered_df[filtered_df['risk_level'] == filter_value]
    elif filter_type == 'current_stage' and 'current_stage' in df.columns:
        filtered_df = filtered_df[filtered_df['current_stage'] == filter_value]
    elif filter_type == 'team_member' and 'team_member' in df.columns:
        filtered_df = filtered_df[filtered_df['team_member'] == filter_value]
    elif filter_type == 'market_segment' and 'market_segment' in df.columns:
        filtered_df = filtered_df[filtered_df['market_segment'] == filter_value]
    
    return filtered_df

def create_filterable_chart(chart_func, df, chart_key, filter_column=None, *args, **kwargs):
    """Create a chart with cross-filtering capabilities using selectbox interaction"""
    
    # Apply existing filters to this chart's data
    filtered_df = apply_cross_chart_filter(df, 
                                         st.session_state.get('filter_type'), 
                                         st.session_state.get('filter_value'))
    
    # Create the chart with filtered data
    fig = chart_func(filtered_df, *args, **kwargs)
    
    # Add filter indicator if active
    if st.session_state.get('filter_active', False):
        filter_info = f"Filtered by {st.session_state.get('filter_type', '')}: {st.session_state.get('filter_value', '')}"
        fig.add_annotation(
            text=f"Filter: {filter_info}",
            xref="paper", yref="paper",
            x=0.02, y=0.98,
            showarrow=False,
            font=dict(size=10, color="yellow"),
            bgcolor="rgba(0,0,0,0.5)",
            bordercolor="yellow",
            borderwidth=1
        )
    
    # Display chart
    st.plotly_chart(fig, use_container_width=True, key=chart_key)
    
    # Add interactive filter selector below chart
    if filter_column and filter_column in df.columns:
        unique_values = df[filter_column].unique().tolist()
        
        # Create filter selector
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_value = st.selectbox(
                f"Filter by {filter_column.replace('_', ' ').title()}:",
                ['All'] + unique_values,
                key=f"{chart_key}_filter",
                index=0
            )
        with col2:
            if st.button(f"Apply Filter", key=f"{chart_key}_apply"):
                if selected_value != 'All':
                    st.session_state['filter_active'] = True
                    st.session_state['filter_type'] = filter_column
                    st.session_state['filter_value'] = selected_value
                    st.rerun()
    
    return filtered_df

def create_rag_pie_chart(df):
    """Create RAG status pie chart with filtering"""
    rag_counts = df['rag_status'].value_counts()
    
    colors = {
        'Green': '#28a745',
        'Amber': '#ffc107', 
        'Red': '#dc3545'
    }
    
    fig = px.pie(
        values=rag_counts.values,
        names=rag_counts.index,
        title="Contract RAG Status Distribution",
        color=rag_counts.index,
        color_discrete_map=colors
    )
    
    fig.update_layout(
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        showlegend=True
    )
    
    return fig

def create_category_bar_chart(df):
    """Create procurement category bar chart with filtering"""
    category_data = df.groupby('procurement_category').agg({
        'package_name': 'count',
        'total_value_gbp': 'sum'
    }).reset_index()
    category_data['total_value_gbp_m'] = category_data['total_value_gbp'] / 1_000_000
    
    fig = px.bar(
        category_data,
        x='procurement_category',
        y='package_name',
        title="Contracts by Procurement Category",
        color='total_value_gbp_m',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        xaxis_title="Procurement Category",
        yaxis_title="Number of Contracts",
        xaxis_tickangle=-45
    )
    
    return fig

def create_value_timeline_chart(df):
    """Create contract value timeline chart with filtering"""
    timeline_data = df.groupby('current_stage').agg({
        'package_name': 'count',
        'total_value_gbp': 'sum'
    }).reset_index()
    timeline_data['total_value_gbp_m'] = timeline_data['total_value_gbp'] / 1_000_000
    
    fig = px.bar(
        timeline_data,
        x='current_stage',
        y='total_value_gbp_m',
        title="Contract Value by Stage",
        color='package_name',
        color_continuous_scale='blues'
    )
    
    fig.update_layout(
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        xaxis_title="Contract Stage",
        yaxis_title="Total Value (£M)",
        xaxis_tickangle=-45
    )
    
    return fig

def create_risk_scatter_chart(df):
    """Create risk vs value scatter chart with filtering"""
    fig = px.scatter(
        df,
        x='total_value_gbp',
        y='days_in_current_stage',
        size='total_value_gbp',
        color='risk_level',
        hover_name='package_name',
        title="Risk vs Value Analysis",
        color_discrete_map={'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'}
    )
    
    fig.update_layout(
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        xaxis_title="Contract Value (£)",
        yaxis_title="Days in Current Stage"
    )
    
    return fig

def render_filter_controls():
    """Render filter control panel"""
    if st.session_state.get('filter_active', False):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.info(f"🔍 Active Filter: {st.session_state.get('filter_type', '')} = {st.session_state.get('filter_value', '')}")
        
        with col2:
            if st.button("🔄 Reset All Filters"):
                clear_all_filters()
                st.rerun()
        
        with col3:
            filter_count = 1 if st.session_state.get('filter_active') else 0
            st.metric("Active Filters", filter_count)

def clear_all_filters():
    """Clear all active filters"""
    st.session_state['filter_active'] = False
    st.session_state['filter_type'] = None
    st.session_state['filter_value'] = None
    st.session_state['selected_contracts'] = []
    st.session_state['selected_suppliers'] = []
    st.session_state['selected_categories'] = []

def get_filtered_summary_stats(df):
    """Get summary statistics for filtered data"""
    if st.session_state.get('filter_active', False):
        filtered_df = apply_cross_chart_filter(df, 
                                             st.session_state.get('filter_type'), 
                                             st.session_state.get('filter_value'))
        
        total_contracts = len(filtered_df)
        total_value = filtered_df['total_value_gbp'].sum() / 1_000_000 if 'total_value_gbp' in filtered_df.columns else 0
        
        return {
            'contracts': total_contracts,
            'value_m': total_value,
            'filtered': True
        }
    else:
        total_contracts = len(df)
        total_value = df['total_value_gbp'].sum() / 1_000_000 if 'total_value_gbp' in df.columns else 0
        
        return {
            'contracts': total_contracts,
            'value_m': total_value,
            'filtered': False
        }
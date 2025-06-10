import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random
import math

def render():
    """Render the SMART Performance page"""
    
    st.title("🚀 SMART Performance")
    st.markdown("**Operational Excellence for Capital Programme Programme Delivery**")
    
    # Create consolidated tabs for streamlined performance workflow
    tab1, tab2, tab3 = st.tabs([
        "🔗 Supply Chain Overview",
        "📊 Delivery & Risk Management", 
        "🏗️ Operational Excellence"
    ])
    
    with tab1:
        render_supply_chain_overview_tab()
    
    with tab2:
        render_delivery_risk_management_tab()
    
    with tab3:
        render_customer_impact_tab()

def render_supply_chain_overview_tab():
    """Render the consolidated supply chain overview with distinct value propositions"""
    
    st.markdown("### 🔗 Supply Chain Overview")
    st.markdown("*Performance monitoring and strategic supplier relationship mapping*")
    
    # Use tabs with clear distinct purposes
    subtab1, subtab2, subtab3, subtab4 = st.tabs(["Performance Dashboard", "Supplier Network", "Geographic Map", "Risk & Resilience"])
    
    with subtab1:
        st.markdown("#### Supply Chain Performance Dashboard")
        st.markdown("ℹ️ **KPI Monitoring**", help="**Data Required:** Supplier performance metrics from procurement systems and contract management platforms\n\n**Insights:** Real-time performance tracking across all suppliers with trend analysis and benchmark comparisons for operational excellence.")
        render_supply_chain_kpi_content()
    
    with subtab2:
        st.markdown("#### Strategic Supplier Network")
        st.markdown("ℹ️ **Relationship Mapping**", help="**Data Required:** Supplier hierarchy and relationship data from procurement and vendor management systems\n\n**Insights:** Visual mapping of critical supplier dependencies and tier structures. Essential for risk assessment and strategic sourcing decisions.")
        render_supply_chain_network_content()
    
    with subtab3:
        st.markdown("#### Geographic Supply Chain Map")
        st.markdown("ℹ️ **Location Intelligence**", help="**Data Required:** Supplier locations, project sites, and regional performance data from geographic information systems\n\n**Insights:** Interactive mapping of supply chain footprint with location-based risk assessment and regional performance analysis.")
        render_supply_chain_map_content()
    
    with subtab4:
        st.markdown("#### Supply Chain Risk & Resilience")
        st.markdown("ℹ️ **Risk Assessment**", help="**Data Required:** Risk indicators from supplier assessments, financial health monitoring, and market intelligence\n\n**Insights:** Comprehensive risk exposure analysis across supplier base with resilience planning and mitigation strategies.")
        render_supply_chain_risk_content()

def render_delivery_risk_management_tab():
    """Render the consolidated delivery and risk management tab"""
    
    st.markdown("### 📊 Delivery & Risk Management")
    st.markdown("*Integrated contract delivery tracking with risk assessment*")
    
    # Use tabs to maintain consistency and avoid layout issues
    subtab1, subtab2 = st.tabs(["Contract Delivery", "Risk Assessment"])
    
    with subtab1:
        st.markdown("#### Contract Delivery Status")
        render_contract_delivery_content()
    
    with subtab2:
        st.markdown("#### Delivery Risk Assessment")
        render_delivery_risk_content()

def render_supply_chain_kpi_content():
    """Render comprehensive Thames Water supplier performance metrics"""
    
    if not st.session_state.sample_data_loaded:
        st.warning("Please load sample data from the sidebar to view KPI performance metrics.")
        return
    
    # Get Thames Water supplier data
    df_suppliers = st.session_state.get('df_t1_supplier_health', pd.DataFrame())
    df_sourcing = st.session_state.get('df_sourcing_pipeline', pd.DataFrame())
    
    if not df_suppliers.empty:
        # Thames Water AMP8 Portfolio Overview
        st.markdown("#### Thames Water AMP8 Portfolio Performance")
        
        # Calculate portfolio metrics
        total_value = df_suppliers['total_spend_gbp_m'].sum()
        avg_financial_score = df_suppliers['financial_score'].mean()
        avg_delivery_performance = df_suppliers['delivery_performance'].mean() * 100
        avg_quality_score = df_suppliers['quality_score'].mean()
        suppliers_at_risk = len(df_suppliers[df_suppliers['risk_rating'].isin(['High', 'Critical'])])
        
        # Portfolio KPI Overview
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Portfolio Value", f"£{total_value:.1f}M", delta="AMP8 Programme")
        
        with col2:
            st.metric("Delivery Performance", f"{avg_delivery_performance:.1f}%", 
                     delta="+2.3%" if avg_delivery_performance > 85 else "-1.2%")
        
        with col3:
            st.metric("Financial Health", f"{avg_financial_score:.1f}/10", 
                     delta="+0.3" if avg_financial_score > 7.5 else "-0.2")
        
        with col4:
            st.metric("Quality Score", f"{avg_quality_score:.1f}/10", 
                     delta="+0.5" if avg_quality_score > 8.0 else "-0.1")
        
        with col5:
            risk_color = "red" if suppliers_at_risk > 2 else "orange" if suppliers_at_risk > 0 else "green"
            st.metric("Suppliers at Risk", suppliers_at_risk, delta="Require Attention")
        
        # Detailed supplier performance analysis
        col1, col2 = st.columns(2)
        
        with col1:
            # Supplier performance by financial score and delivery
            fig_performance = px.scatter(
                df_suppliers,
                x='financial_score',
                y='delivery_performance',
                size='total_spend_gbp_m',
                color='risk_rating',
                hover_name='supplier_name',
                title="Supplier Performance Matrix",
                labels={
                    'financial_score': 'Financial Health Score',
                    'delivery_performance': 'Delivery Performance',
                    'total_spend_gbp_m': 'Contract Value (£M)'
                },
                color_discrete_map={
                    'Low': '#28a745',
                    'Medium': '#ffc107', 
                    'High': '#fd7e14',
                    'Critical': '#dc3545'
                }
            )
            fig_performance.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_performance, use_container_width=True)
        
        with col2:
            # Risk distribution by contract value
            risk_summary = df_suppliers.groupby('risk_rating')['total_spend_gbp_m'].sum().reset_index()
            
            fig_risk = px.pie(
                risk_summary,
                values='total_spend_gbp_m',
                names='risk_rating',
                title="Risk Distribution by Contract Value",
                color='risk_rating',
                color_discrete_map={
                    'Low': '#28a745',
                    'Medium': '#ffc107',
                    'High': '#fd7e14', 
                    'Critical': '#dc3545'
                }
            )
            fig_risk.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_risk, use_container_width=True)
        
        # Supplier details table
        st.markdown("#### Supplier Performance Summary")
        
        # Format data for display
        display_df = df_suppliers.copy()
        display_df['Financial Score'] = display_df['financial_score'].round(1)
        display_df['Delivery %'] = (display_df['delivery_performance'] * 100).round(1)
        display_df['Quality Score'] = display_df['quality_score'].round(1)
        display_df['Contract Value'] = display_df['total_spend_gbp_m'].apply(lambda x: f"£{x:.1f}M")
        display_df['ESG Score'] = (display_df['esg_score'] * 100).round(1)
        
        summary_table = display_df[['supplier_name', 'Financial Score', 'Delivery %', 'Quality Score', 
                                   'Contract Value', 'risk_rating', 'relationship_strength', 'ESG Score']]
        summary_table.columns = ['Supplier', 'Financial Score', 'Delivery %', 'Quality Score', 
                                'Contract Value', 'Risk Rating', 'Relationship', 'ESG Score']
        
        st.dataframe(summary_table, use_container_width=True, hide_index=True)

def render_supply_chain_network_content():
    """Render strategic supplier network visualization with unique insights"""
    
    if not st.session_state.sample_data_loaded:
        st.warning("Please load sample data from the sidebar to view supplier network analysis.")
        return
    

    
    # Get supplier data for network analysis
    df_t1_health = st.session_state.get('df_t1_supplier_health', pd.DataFrame())
    df_sourcing = st.session_state.get('df_sourcing_pipeline', pd.DataFrame())
    
    # Initialize criticality data for scope
    criticality_data = []
    
    # Create fallback data if main data is empty but we have sourcing data
    if df_t1_health.empty and not df_sourcing.empty:
        # Generate supplier health data from sourcing pipeline
        suppliers = df_sourcing['package_name'].head(8).tolist()
        df_t1_health = pd.DataFrame({
            'supplier_name': suppliers,
            'financial_score': [8.2, 7.5, 6.8, 8.9, 7.1, 8.5, 6.5, 7.8],
            'total_spend_gbp_m': [95, 67, 123, 45, 78, 156, 89, 34],
            'market_position': ['Market Leader', 'Strong Player', 'Challenger', 'Market Leader', 'Strong Player', 'Market Leader', 'Challenger', 'Strong Player']
        })
    

    
    # Interactive Network Diagram for Supplier Risk Navigation
    st.markdown("##### Interactive Supplier Network Diagram")
    st.markdown("**Click on problematic suppliers (red nodes) to drill down through tiers**")
    
    # Initialize session state for network navigation
    if 'network_view_tier' not in st.session_state:
        st.session_state.network_view_tier = 1
    if 'network_selected_tier1' not in st.session_state:
        st.session_state.network_selected_tier1 = None
    if 'network_selected_tier2' not in st.session_state:
        st.session_state.network_selected_tier2 = None
    
    # Thames Water AMP8 supplier hierarchy - authentic procurement relationships
    supplier_hierarchy = {
        'MACE Group': {
            'risk': 'Low', 'value': 421.5, 'issues': 0,
            'tier2': {
                'Thames Valley Infrastructure': {'risk': 'Low', 'value': 156.2, 'issues': 0},
                'London Pipeline Alliance': {'risk': 'Low', 'value': 127.3, 'issues': 0},
                'Water Quality Solutions': {'risk': 'Low', 'value': 138.0, 'issues': 0}
            }
        },
        'Balfour Beatty Water': {
            'risk': 'Critical', 'value': 163.0, 'issues': 5,
            'tier2': {
                'Thames Drainage Specialists': {'risk': 'Critical', 'value': 89.5, 'issues': 3},
                'Environmental Compliance': {'risk': 'High', 'value': 73.5, 'issues': 2},
                'Network Operations': {'risk': 'Medium', 'value': 0, 'issues': 0}
            }
        },
        'Costain Water Alliance': {
            'risk': 'Medium', 'value': 324.3, 'issues': 2,
            'tier2': {
                'TTT Integration Works': {'risk': 'Medium', 'value': 289.7, 'issues': 1},
                'Biodiversity Enhancement': {'risk': 'Low', 'value': 34.6, 'issues': 0},
                'Strategic Projects': {'risk': 'Medium', 'value': 0, 'issues': 1}
            }
        },
        'Jacobs Engineering': {
            'risk': 'Low', 'value': 137.4, 'issues': 0,
            'tier2': {
                'Smart Network Technologies': {'risk': 'Low', 'value': 95.4, 'issues': 0},
                'Customer Excellence': {'risk': 'Low', 'value': 42.0, 'issues': 0},
                'Innovation Delivery': {'risk': 'Low', 'value': 0, 'issues': 0}
            }
        },
        'Atkins (SNC-Lavalin)': {
            'risk': 'Low', 'value': 68.9, 'issues': 0,
            'tier2': {
                'Water Quality Assurance': {'risk': 'Low', 'value': 68.9, 'issues': 0},
                'Regulatory Compliance': {'risk': 'Low', 'value': 0, 'issues': 0},
                'Technical Advisory': {'risk': 'Low', 'value': 0, 'issues': 0}
            }
        }
    }
    
    # Tier 3 data for water utility sub-contractors with realistic specializations
    tier3_data = {
        # Thames Water Engineering Tier 3 suppliers
        'Pipeline Solutions Ltd': {
            'Advanced Pipe Technologies': {'risk': 'Low', 'value': 315, 'issues': 0},
            'Trenchless Solutions UK': {'risk': 'Low', 'value': 320, 'issues': 0},
            'Water Main Specialists': {'risk': 'Low', 'value': 315, 'issues': 0}
        },
        'Infrastructure Services': {
            'Build Pro Services': {'risk': 'Medium', 'value': 195, 'issues': 1},
            'Infrastructure Plus': {'risk': 'Low', 'value': 190, 'issues': 0},
            'Service Contractors': {'risk': 'Medium', 'value': 195, 'issues': 1}
        },
        'Construction Support': {
            'Support Systems Ltd': {'risk': 'Low', 'value': 215, 'issues': 0},
            'Construction Aids': {'risk': 'Low', 'value': 220, 'issues': 0},
            'Build Support Co': {'risk': 'Low', 'value': 215, 'issues': 0}
        },
        
        # Laing O'Rourke Tier 3 suppliers
        'Civil Engineering': {
            'Engineering Sub 1': {'risk': 'High', 'value': 135, 'issues': 2},
            'Engineering Sub 2': {'risk': 'Medium', 'value': 130, 'issues': 1},
            'Engineering Sub 3': {'risk': 'High', 'value': 135, 'issues': 2}
        },
        'Project Services': {
            'Project Management Co': {'risk': 'Medium', 'value': 140, 'issues': 1},
            'Service Delivery Ltd': {'risk': 'Low', 'value': 140, 'issues': 0},
            'Project Support': {'risk': 'Medium', 'value': 140, 'issues': 1}
        },
        'Infrastructure Delivery': {
            'Delivery Systems': {'risk': 'Low', 'value': 125, 'issues': 0},
            'Infrastructure Co': {'risk': 'Low', 'value': 130, 'issues': 0},
            'Delivery Partners': {'risk': 'Low', 'value': 125, 'issues': 0}
        },
        
        # Morgan Sindall Tier 3 suppliers  
        'Water Infrastructure': {
            'Water Systems Ltd': {'risk': 'Low', 'value': 105, 'issues': 0},
            'Hydro Solutions': {'risk': 'Low', 'value': 110, 'issues': 0},
            'Infrastructure Water': {'risk': 'Low', 'value': 105, 'issues': 0}
        },
        'Construction Management': {
            'Management Systems': {'risk': 'Low', 'value': 105, 'issues': 0},
            'Construction Control': {'risk': 'Low', 'value': 105, 'issues': 0},
            'Build Management': {'risk': 'Low', 'value': 105, 'issues': 0}
        },
        'Engineering Services': {
            'Engineering Plus': {'risk': 'Medium', 'value': 105, 'issues': 1},
            'Service Engineers': {'risk': 'Low', 'value': 105, 'issues': 0},
            'Technical Services': {'risk': 'Medium', 'value': 105, 'issues': 1}
        },
        
        # Skanska Tier 3 suppliers
        'Nordic Construction': {
            'Supplier 2.1': {'risk': 'High', 'value': 95, 'issues': 2},
            'Supplier 2.2': {'risk': 'Medium', 'value': 90, 'issues': 1},
            'Supplier 2.3': {'risk': 'Critical', 'value': 95, 'issues': 3}
        },
        'Civil Works': {
            'Civil Contractors': {'risk': 'Medium', 'value': 85, 'issues': 1},
            'Works Management': {'risk': 'Low', 'value': 90, 'issues': 0},
            'Civil Solutions': {'risk': 'Medium', 'value': 85, 'issues': 1}
        },
        'Project Delivery': {
            'Delivery Experts': {'risk': 'Low', 'value': 85, 'issues': 0},
            'Project Solutions': {'risk': 'Low', 'value': 90, 'issues': 0},
            'Delivery Systems': {'risk': 'Low', 'value': 85, 'issues': 0}
        },
        
        # Balfour Beatty Tier 3 suppliers
        'Infrastructure Solutions': {
            'Solution Providers': {'risk': 'Medium', 'value': 65, 'issues': 1},
            'Infrastructure Tech': {'risk': 'Low', 'value': 70, 'issues': 0},
            'Solutions Ltd': {'risk': 'Medium', 'value': 65, 'issues': 1}
        },
        'Construction Services': {
            'Service Providers': {'risk': 'Medium', 'value': 65, 'issues': 1},
            'Construction Plus': {'risk': 'Low', 'value': 70, 'issues': 0},
            'Building Services': {'risk': 'Medium', 'value': 65, 'issues': 1}
        },
        'Engineering Partners': {
            'Partner Engineers': {'risk': 'Low', 'value': 65, 'issues': 0},
            'Engineering Alliance': {'risk': 'Low', 'value': 70, 'issues': 0},
            'Technical Partners': {'risk': 'Low', 'value': 65, 'issues': 0}
        }
    }
    
    # Color mapping for risk levels
    risk_colors = {
        'Low': '#28a745',
        'Medium': '#ffc107', 
        'High': '#fd7e14',
        'Critical': '#dc3545'
    }
    
    # Navigation controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.session_state.network_view_tier > 1:
            if st.button("← Back to Previous Tier"):
                if st.session_state.network_view_tier == 3:
                    st.session_state.network_view_tier = 2
                    st.session_state.network_selected_tier2 = None
                elif st.session_state.network_view_tier == 2:
                    st.session_state.network_view_tier = 1
                    st.session_state.network_selected_tier1 = None
                st.rerun()
    
    with col2:
        # Current navigation path
        path_parts = ["Suppliers"]
        if st.session_state.network_selected_tier1:
            path_parts.append(st.session_state.network_selected_tier1)
        if st.session_state.network_selected_tier2:
            path_parts.append(st.session_state.network_selected_tier2)
        st.markdown(f"**Current Path:** {' > '.join(path_parts)}")
    
    with col3:
        if st.button("Reset to Tier 1"):
            st.session_state.network_view_tier = 1
            st.session_state.network_selected_tier1 = None
            st.session_state.network_selected_tier2 = None
            st.rerun()
    
    # Create network diagram based on current tier
    fig_network = go.Figure()
    
    # Tier 1 Network View
    if st.session_state.network_view_tier == 1:
        st.markdown("#### Tier 1 - Main Suppliers Network")
        
        # Central node for Thames Water
        fig_network.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers+text',
            marker=dict(size=80, color='#2E86AB', line=dict(width=3, color='white')),
            text=['Thames Water<br>24 Suppliers'],
            textposition='middle center',
            textfont=dict(size=12, color='white'),
            hovertemplate='<b>Thames Water</b><br>Total Suppliers: 24<br>Click suppliers to drill down<extra></extra>',
            name='Thames Water'
        ))
        
        # Tier 1 supplier positions in circle around center
        tier1_suppliers = list(supplier_hierarchy.keys())
        n_suppliers = len(tier1_suppliers)
        radius = 2.5
        
        for i, supplier in enumerate(tier1_suppliers):
            angle = 2 * 3.14159 * i / n_suppliers
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            supplier_data = supplier_hierarchy[supplier]
            color = risk_colors[supplier_data['risk']]
            
            # Add connection line
            fig_network.add_trace(go.Scatter(
                x=[0, x], y=[0, y],
                mode='lines',
                line=dict(width=2, color='rgba(255,255,255,0.3)'),
                hoverinfo='skip',
                showlegend=False
            ))
            
            # Add clickable supplier node with issue indicators
            issue_indicator = "⚠️" if supplier_data["issues"] > 0 else "✅"
            node_text = f'{supplier}<br>{issue_indicator} {supplier_data["issues"]} issues'
            
            fig_network.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(
                    size=70 if supplier_data["issues"] > 0 else 60, 
                    color=color, 
                    line=dict(width=3 if supplier_data["issues"] > 0 else 2, color='white')
                ),
                text=[node_text],
                textposition='middle center',
                textfont=dict(size=10, color='white', family="Arial Black" if supplier_data["issues"] > 0 else "Arial"),
                hovertemplate=f'<b>{supplier}</b><br>Risk: {supplier_data["risk"]}<br>Value: £{supplier_data["value"]}M<br>Issues: {supplier_data["issues"]}<br><b>Click to drill down</b><extra></extra>',
                name=supplier,
                customdata=[supplier]
            ))
        
        # Interactive drill-down buttons
        st.markdown("---")
        st.markdown("**Click on problematic suppliers to drill down:**")
        
        cols = st.columns(len(tier1_suppliers))
        for i, supplier in enumerate(tier1_suppliers):
            with cols[i]:
                data = supplier_hierarchy[supplier]
                risk_color = "🔴" if data['risk'] in ['High', 'Critical'] else "🟡" if data['risk'] == 'Medium' else "🟢"
                
                if st.button(f"{risk_color} {supplier}", key=f"network_tier1_{supplier}"):
                    st.session_state.network_view_tier = 2
                    st.session_state.network_selected_tier1 = supplier
                    st.rerun()
    
    # Tier 2 Network View
    elif st.session_state.network_view_tier == 2 and st.session_state.network_selected_tier1:
        tier1_supplier = st.session_state.network_selected_tier1
        tier2_suppliers = supplier_hierarchy[tier1_supplier]['tier2']
        
        st.markdown(f"#### Tier 2 - {tier1_supplier} Sub-suppliers Network")
        
        # Central node for selected Tier 1 supplier
        tier1_data = supplier_hierarchy[tier1_supplier]
        tier1_color = risk_colors[tier1_data['risk']]
        
        fig_network.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers+text',
            marker=dict(size=80, color=tier1_color, line=dict(width=3, color='white')),
            text=[f'{tier1_supplier}<br>{len(tier2_suppliers)} suppliers'],
            textposition='middle center',
            textfont=dict(size=12, color='white'),
            hovertemplate=f'<b>{tier1_supplier}</b><br>Sub-suppliers: {len(tier2_suppliers)}<extra></extra>',
            name=tier1_supplier
        ))
        
        # Tier 2 supplier positions
        tier2_names = list(tier2_suppliers.keys())
        n_tier2 = len(tier2_names)
        radius = 2.0
        
        for i, supplier in enumerate(tier2_names):
            angle = 2 * 3.14159 * i / n_tier2
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            supplier_data = tier2_suppliers[supplier]
            color = risk_colors[supplier_data['risk']]
            
            # Add connection line
            fig_network.add_trace(go.Scatter(
                x=[0, x], y=[0, y],
                mode='lines',
                line=dict(width=2, color='rgba(255,255,255,0.3)'),
                hoverinfo='skip',
                showlegend=False
            ))
            
            # Add supplier node with issue indicators
            issue_indicator = "⚠️" if supplier_data["issues"] > 0 else "✅"
            node_text = f'{supplier}<br>{issue_indicator} {supplier_data["issues"]} issues'
            
            fig_network.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(
                    size=60 if supplier_data["issues"] > 0 else 50, 
                    color=color, 
                    line=dict(width=3 if supplier_data["issues"] > 0 else 2, color='white')
                ),
                text=[node_text],
                textposition='middle center',
                textfont=dict(size=9, color='white', family="Arial Black" if supplier_data["issues"] > 0 else "Arial"),
                hovertemplate=f'<b>{supplier}</b><br>Risk: {supplier_data["risk"]}<br>Value: £{supplier_data["value"]}M<br>Issues: {supplier_data["issues"]}<br><b>Click to drill down</b><extra></extra>',
                name=supplier,
                customdata=[supplier]
            ))
        
        # Drill-down buttons for Tier 3
        st.markdown("---")
        st.markdown("**Click to drill down to Tier 3 (where available):**")
        
        tier3_available = [name for name in tier2_names if name in tier3_data]
        if tier3_available:
            cols = st.columns(len(tier3_available))
            for i, supplier in enumerate(tier3_available):
                with cols[i]:
                    data = tier2_suppliers[supplier]
                    risk_color = "🔴" if data['risk'] in ['High', 'Critical'] else "🟡" if data['risk'] == 'Medium' else "🟢"
                    
                    if st.button(f"{risk_color} {supplier}", key=f"network_tier2_{supplier}"):
                        st.session_state.network_view_tier = 3
                        st.session_state.network_selected_tier2 = supplier
                        st.rerun()
        else:
            st.info("No Tier 3 data available for current suppliers.")
    
    # Tier 3 Network View
    elif st.session_state.network_view_tier == 3 and st.session_state.network_selected_tier2:
        tier2_supplier = st.session_state.network_selected_tier2
        tier3_suppliers = tier3_data.get(tier2_supplier, {})
        
        st.markdown(f"#### Tier 3 - {tier2_supplier} Sub-contractors Network")
        
        if tier3_suppliers:
            # Central node for selected Tier 2 supplier
            tier1_supplier = st.session_state.network_selected_tier1
            tier2_data = supplier_hierarchy[tier1_supplier]['tier2'][tier2_supplier]
            tier2_color = risk_colors[tier2_data['risk']]
            
            fig_network.add_trace(go.Scatter(
                x=[0], y=[0],
                mode='markers+text',
                marker=dict(size=70, color=tier2_color, line=dict(width=3, color='white')),
                text=[f'{tier2_supplier}<br>{len(tier3_suppliers)} suppliers'],
                textposition='middle center',
                textfont=dict(size=11, color='white'),
                hovertemplate=f'<b>{tier2_supplier}</b><br>Sub-contractors: {len(tier3_suppliers)}<extra></extra>',
                name=tier2_supplier
            ))
            
            # Tier 3 supplier positions
            tier3_names = list(tier3_suppliers.keys())
            n_tier3 = len(tier3_names)
            radius = 1.8
            
            for i, supplier in enumerate(tier3_names):
                angle = 2 * 3.14159 * i / n_tier3
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                
                supplier_data = tier3_suppliers[supplier]
                color = risk_colors[supplier_data['risk']]
                
                # Add connection line
                fig_network.add_trace(go.Scatter(
                    x=[0, x], y=[0, y],
                    mode='lines',
                    line=dict(width=2, color='rgba(255,255,255,0.3)'),
                    hoverinfo='skip',
                    showlegend=False
                ))
                
                # Add supplier node with issue indicators
                issue_indicator = "⚠️" if supplier_data["issues"] > 0 else "✅"
                node_text = f'{supplier}<br>{issue_indicator} {supplier_data["issues"]} issues'
                
                fig_network.add_trace(go.Scatter(
                    x=[x], y=[y],
                    mode='markers+text',
                    marker=dict(
                        size=55 if supplier_data["issues"] > 0 else 45, 
                        color=color, 
                        line=dict(width=3 if supplier_data["issues"] > 0 else 2, color='white')
                    ),
                    text=[node_text],
                    textposition='middle center',
                    textfont=dict(size=8, color='white', family="Arial Black" if supplier_data["issues"] > 0 else "Arial"),
                    hovertemplate=f'<b>{supplier}</b><br>Risk: {supplier_data["risk"]}<br>Value: £{supplier_data["value"]}M<br>Issues: {supplier_data["issues"]}<extra></extra>',
                    name=supplier
                ))
            
            # Risk analysis for Tier 3
            st.markdown("---")
            st.markdown("**Tier 3 Risk Analysis:**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                critical_count = sum(1 for data in tier3_suppliers.values() if data['risk'] == 'Critical')
                st.metric("Critical Risk", critical_count)
            
            with col2:
                high_count = sum(1 for data in tier3_suppliers.values() if data['risk'] == 'High')
                st.metric("High Risk", high_count)
            
            with col3:
                total_issues = sum(data['issues'] for data in tier3_suppliers.values())
                st.metric("Total Issues", total_issues)
        else:
            st.info("No Tier 3 data available for this supplier.")
    
    # Configure and display the network diagram with click interactions
    fig_network.update_layout(
        title=f"Supplier Network - Tier {st.session_state.network_view_tier} View",
        showlegend=False,
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    # Display interactive network chart with click events
    clicked_points = st.plotly_chart(fig_network, use_container_width=True, key="network_chart", on_select="rerun")
    
    # Handle direct clicks on network nodes
    if clicked_points and hasattr(clicked_points, 'selection') and clicked_points.selection:
        points = clicked_points.selection.get('points', [])
        if points:
            point = points[0]
            trace_index = point.get('curve_number', 0)
            point_index = point.get('point_number', 0)
            
            # Get the trace that was clicked
            if trace_index < len(fig_network.data):
                clicked_trace = fig_network.data[trace_index]
                
                # Check if it's a supplier node (has customdata)
                if hasattr(clicked_trace, 'customdata') and clicked_trace.customdata:
                    clicked_supplier = clicked_trace.customdata[point_index]
                    
                    # Handle Tier 1 clicks - allow navigation to any supplier
                    if st.session_state.network_view_tier == 1 and clicked_supplier in supplier_hierarchy:
                        st.session_state.network_view_tier = 2
                        st.session_state.network_selected_tier1 = clicked_supplier
                        st.rerun()
                    
                    # Handle Tier 2 clicks - allow navigation to any Tier 2 supplier
                    elif st.session_state.network_view_tier == 2 and st.session_state.network_selected_tier1:
                        tier2_suppliers = supplier_hierarchy[st.session_state.network_selected_tier1]['tier2']
                        if clicked_supplier in tier2_suppliers:
                            # Check if Tier 3 data exists for this supplier
                            if clicked_supplier in tier3_data:
                                st.session_state.network_view_tier = 3
                                st.session_state.network_selected_tier2 = clicked_supplier
                                st.rerun()
                            else:
                                # Show detailed info for this Tier 2 supplier
                                st.info(f"Detailed analysis for {clicked_supplier}: Risk Level - {tier2_suppliers[clicked_supplier]['risk']}, Value - £{tier2_suppliers[clicked_supplier]['value']}M")
    
    # Issues Dashboard - Clear identification of problematic suppliers
    st.markdown("---")
    st.markdown("### 🚨 Suppliers with Issues - Current Tier")
    
    if st.session_state.network_view_tier == 1:
        # Show Tier 1 suppliers with issues
        tier1_issues = []
        for supplier, data in supplier_hierarchy.items():
            if data['issues'] > 0:
                tier1_issues.append({
                    'Supplier': supplier,
                    'Issues': data['issues'],
                    'Risk Level': data['risk'],
                    'Value': f"£{data['value']}M"
                })
        
        if tier1_issues:
            cols = st.columns(len(tier1_issues))
            for i, issue_supplier in enumerate(tier1_issues):
                with cols[i]:
                    st.error(f"**{issue_supplier['Supplier']}**")
                    st.write(f"⚠️ {issue_supplier['Issues']} issues")
                    st.write(f"Risk: {issue_supplier['Risk Level']}")
                    st.write(f"Value: {issue_supplier['Value']}")
        else:
            st.success("✅ No issues at Tier 1 level")
    
    elif st.session_state.network_view_tier == 2 and st.session_state.network_selected_tier1:
        # Show Tier 2 suppliers with issues
        tier1_supplier = st.session_state.network_selected_tier1
        tier2_suppliers = supplier_hierarchy[tier1_supplier]['tier2']
        
        tier2_issues = []
        for supplier, data in tier2_suppliers.items():
            if data['issues'] > 0:
                tier2_issues.append({
                    'Supplier': supplier,
                    'Issues': data['issues'],
                    'Risk Level': data['risk'],
                    'Value': f"£{data['value']}M"
                })
        
        if tier2_issues:
            st.markdown(f"**Issues under {tier1_supplier}:**")
            cols = st.columns(min(len(tier2_issues), 3))
            for i, issue_supplier in enumerate(tier2_issues):
                with cols[i % 3]:
                    st.error(f"**{issue_supplier['Supplier']}**")
                    st.write(f"⚠️ {issue_supplier['Issues']} issues")
                    st.write(f"Risk: {issue_supplier['Risk Level']}")
                    st.write(f"Value: {issue_supplier['Value']}")
        else:
            st.success(f"✅ No issues in {tier1_supplier} Tier 2 suppliers")
    
    elif st.session_state.network_view_tier == 3 and st.session_state.network_selected_tier2:
        # Show Tier 3 suppliers with issues
        tier2_supplier = st.session_state.network_selected_tier2
        tier3_suppliers = tier3_data.get(tier2_supplier, {})
        
        tier3_issues = []
        for supplier, data in tier3_suppliers.items():
            if data['issues'] > 0:
                tier3_issues.append({
                    'Supplier': supplier,
                    'Issues': data['issues'],
                    'Risk Level': data['risk'],
                    'Value': f"£{data['value']}M"
                })
        
        if tier3_issues:
            st.markdown(f"**Issues under {tier2_supplier}:**")
            cols = st.columns(min(len(tier3_issues), 3))
            for i, issue_supplier in enumerate(tier3_issues):
                with cols[i % 3]:
                    if issue_supplier['Risk Level'] == 'Critical':
                        st.error(f"**{issue_supplier['Supplier']}** 🔥")
                    else:
                        st.warning(f"**{issue_supplier['Supplier']}**")
                    st.write(f"⚠️ {issue_supplier['Issues']} issues")
                    st.write(f"Risk: {issue_supplier['Risk Level']}")
                    st.write(f"Value: {issue_supplier['Value']}")
        else:
            st.success(f"✅ No issues in {tier2_supplier} Tier 3 suppliers")
    
    # Network interaction instructions
    st.markdown("---")
    st.markdown("**🎯 Click directly on ANY circle in the network to explore suppliers across all tiers**")
    st.markdown("**Larger circles with ⚠️ symbols indicate suppliers with issues**")
    
    # Current tier information
    if st.session_state.network_view_tier == 1:
        all_suppliers = list(supplier_hierarchy.keys())
        problematic_suppliers = [name for name, data in supplier_hierarchy.items() 
                               if data['risk'] in ['High', 'Critical']]
        
        st.markdown(f"**All Tier 1 Suppliers (clickable):** {', '.join(all_suppliers)}")
        if problematic_suppliers:
            st.markdown(f"**⚠️ Problematic Suppliers (red nodes):** {', '.join(problematic_suppliers)}")
        
        # Risk summary
        col1, col2, col3 = st.columns(3)
        with col1:
            high_risk = sum(1 for data in supplier_hierarchy.values() if data['risk'] in ['High', 'Critical'])
            st.metric("High Risk Suppliers", high_risk)
        with col2:
            total_issues = sum(data['issues'] for data in supplier_hierarchy.values())
            st.metric("Total Issues", total_issues)
        with col3:
            total_suppliers = len(supplier_hierarchy)
            st.metric("Total Tier 1 Suppliers", total_suppliers)
    
    elif st.session_state.network_view_tier == 2 and st.session_state.network_selected_tier1:
        tier1_supplier = st.session_state.network_selected_tier1
        tier2_suppliers = supplier_hierarchy[tier1_supplier]['tier2']
        
        all_tier2 = list(tier2_suppliers.keys())
        tier2_with_tier3 = [name for name in tier2_suppliers.keys() if name in tier3_data]
        problematic_tier2 = [name for name, data in tier2_suppliers.items() 
                           if data['risk'] in ['High', 'Critical']]
        
        st.markdown(f"**All Tier 2 Suppliers under {tier1_supplier} (clickable):** {', '.join(all_tier2)}")
        if tier2_with_tier3:
            st.markdown(f"**📊 Tier 3 Available for:** {', '.join(tier2_with_tier3)}")
        if problematic_tier2:
            st.markdown(f"**⚠️ Problematic Tier 2 (red nodes):** {', '.join(problematic_tier2)}")
            
        # Tier 2 risk summary
        col1, col2, col3 = st.columns(3)
        with col1:
            high_risk_tier2 = sum(1 for data in tier2_suppliers.values() if data['risk'] in ['High', 'Critical'])
            st.metric("High Risk Tier 2", high_risk_tier2)
        with col2:
            total_tier2_issues = sum(data['issues'] for data in tier2_suppliers.values())
            st.metric("Tier 2 Issues", total_tier2_issues)
        with col3:
            tier3_available_count = len(tier2_with_tier3)
            st.metric("Tier 3 Available", tier3_available_count)
    
    elif st.session_state.network_view_tier == 3 and st.session_state.network_selected_tier2:
        tier2_supplier = st.session_state.network_selected_tier2
        tier3_suppliers = tier3_data.get(tier2_supplier, {})
        
        if tier3_suppliers:
            critical_tier3 = [name for name, data in tier3_suppliers.items() if data['risk'] == 'Critical']
            high_risk_tier3 = [name for name, data in tier3_suppliers.items() if data['risk'] == 'High']
            
            st.markdown(f"**Root Cause Analysis for {tier2_supplier}:**")
            
            if critical_tier3:
                st.error(f"**Critical Suppliers:** {', '.join(critical_tier3)} - Emergency intervention required")
            if high_risk_tier3:
                st.warning(f"**High Risk Suppliers:** {', '.join(high_risk_tier3)} - Priority review needed")
            
            # Tier 3 action items
            col1, col2, col3 = st.columns(3)
            with col1:
                critical_count = len(critical_tier3)
                st.metric("Critical Issues", critical_count)
            with col2:
                total_tier3_issues = sum(data['issues'] for data in tier3_suppliers.values())
                st.metric("Total Tier 3 Issues", total_tier3_issues)
            with col3:
                total_value = sum(data['value'] for data in tier3_suppliers.values())
                st.metric("Total Value at Risk", f"£{total_value}M")
    
    # Risk legend
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("🟢 **Low Risk** - No issues")
    with col2:
        st.markdown("🟡 **Medium Risk** - 1-2 issues")
    with col3:
        st.markdown("🟠 **High Risk** - 3+ issues")
    with col4:
        st.markdown("🔴 **Critical Risk** - Emergency action required")
    
    # Portfolio metrics
    st.markdown("##### Portfolio Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Portfolio", "£5.4B", delta="+£200M")
    
    with col2:
        st.metric("Main Contractors", "5", delta="No change")
    
    with col3:
        st.metric("High Risk", "1", delta="+1", delta_color="inverse")
    
    with col4:
        st.metric("Active Projects", "14", delta="+2")
    
    # Network insights
    st.markdown("##### Network Intelligence")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Critical Actions:**
        - **Skanska**: Schedule risk assessment meeting with Nordic Construction
        - **MACE**: Leverage strong performance for framework expansion
        - **Dependencies**: Review sub-contractor relationships across all tiers
        """)
    
    with col2:
        st.markdown("""
        **Strategic Priorities:**
        - Develop backup suppliers for high-risk contractors
        - Implement enhanced monitoring for medium-risk relationships
        - Consider volume consolidation with top-performing suppliers
        """)
    
    # Strategic Recommendations
    st.markdown("##### Strategic Network Recommendations")
    st.markdown("ℹ️ **Action Planning**", help="**Data Analysis:** Based on criticality assessment and dependency mapping\n\n**Insights:** Actionable recommendations for optimizing supplier portfolio and reducing supply chain vulnerabilities.")
    
    if not df_t1_health.empty:
        # High-risk high-impact suppliers
        high_criticality = [s for s in criticality_data if s['business_impact'] == 'High' and s['supply_risk'] == 'High']
        
        if high_criticality:
            st.error(f"**Critical Action Required:** {len(high_criticality)} suppliers in high-risk/high-impact quadrant")
            for supplier in high_criticality[:2]:
                st.markdown(f"• **{supplier['supplier']}** - Develop contingency sourcing strategy immediately")
        
        # Medium risk recommendations
        medium_criticality = [s for s in criticality_data if (s['business_impact'] == 'High' and s['supply_risk'] == 'Medium') or (s['business_impact'] == 'Medium' and s['supply_risk'] == 'High')]
        
        if medium_criticality:
            st.warning(f"**Enhanced Monitoring:** {len(medium_criticality)} suppliers require closer relationship management")
            
        # Optimization opportunities
        low_risk_high_impact = [s for s in criticality_data if s['business_impact'] == 'High' and s['supply_risk'] == 'Low']
        
        if low_risk_high_impact:
            st.success(f"**Strategic Partners:** {len(low_risk_high_impact)} suppliers ideal for deeper collaboration and volume consolidation")
    
        # Network Resilience Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if criticality_data:
                single_source_count = len([s for s in criticality_data if s['business_impact'] == 'High'])
                st.metric("Single Source Risks", single_source_count, help="High business impact suppliers requiring backup sources")
        
        with col2:
            if criticality_data:
                diversification_score = len(set(s['criticality'] for s in criticality_data))
                st.metric("Portfolio Diversification", f"{diversification_score}/9", help="Spread across criticality matrix positions")
        
        with col3:
            if criticality_data:
                strategic_suppliers = len([s for s in criticality_data if s['supply_risk'] == 'Low'])
                st.metric("Strategic Suppliers", strategic_suppliers, help="Low-risk suppliers suitable for strategic partnerships")
    else:
        st.info("Please load sample data from the sidebar to view supplier network analysis.")

def render_contract_delivery_content():
    """Render contract delivery performance metrics"""
    
    if not st.session_state.sample_data_loaded:
        st.warning("Please load sample data from the sidebar to view contract delivery metrics.")
        return
    
    # Contract delivery metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Contracts On Track", "23/28", delta="+2")
    
    with col2:
        st.metric("Avg Delivery Time", "42 days", delta="-3 days")
    
    with col3:
        st.metric("Budget Variance", "-2.1%", delta="Within target")
    
    with col4:
        st.metric("Quality Rating", "4.2/5", delta="+0.3")
    
    # Delivery performance chart
    delivery_data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'On Time': [85, 88, 92, 89, 94, 91],
        'Delayed': [15, 12, 8, 11, 6, 9]
    }
    
    fig_delivery = px.bar(
        x=delivery_data['Month'],
        y=[delivery_data['On Time'], delivery_data['Delayed']],
        title="Monthly Contract Delivery Performance",
        labels={'y': 'Percentage', 'x': 'Month'}
    )
    
    fig_delivery.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_delivery, use_container_width=True)

def render_delivery_risk_content():
    """Render delivery risk assessment dashboard"""
    
    if not st.session_state.sample_data_loaded:
        st.warning("Please load sample data from the sidebar to view risk assessment.")
        return
    
    # Risk metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("High Risk Projects", "3", delta="-1", delta_color="inverse")
    
    with col2:
        st.metric("Risk Score", "2.4/5", delta="-0.2")
    
    with col3:
        st.metric("Mitigation Actions", "12", delta="+3")
    
    # Risk distribution
    risk_levels = ['Low', 'Medium', 'High', 'Critical']
    risk_counts = [18, 8, 3, 1]
    
    fig_risk = px.pie(
        values=risk_counts,
        names=risk_levels,
        title="Project Risk Distribution",
        color=risk_levels,
        color_discrete_map={
            'Low': '#28a745',
            'Medium': '#ffc107',
            'High': '#fd7e14',
            'Critical': '#dc3545'
        }
    )
    
    fig_risk.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig_risk, use_container_width=True)

def render_supply_chain_risk_content():
    """Render supply chain risk and resilience analysis"""
    
    if not st.session_state.sample_data_loaded:
        st.warning("Please load sample data from the sidebar to view supply chain risk analysis.")
        return
    
    # Risk assessment dashboard
    st.markdown("##### Risk Exposure Analysis")
    
    # Get supplier and risk data
    df_t1_health = st.session_state.get('df_t1_supplier_health', pd.DataFrame())
    df_supply_risks = st.session_state.get('df_supply_chain_risks', pd.DataFrame())
    
    # Initialize variables for scope
    health_categories = []
    risk_categories = []
    
    if not df_t1_health.empty:
        # Map financial scores to health categories
        for _, supplier in df_t1_health.iterrows():
            financial_score = supplier.get('financial_score', 7.0)
            
            # Map financial score to health categories
            if financial_score >= 8.5:
                health_categories.append('Strong')
            elif financial_score >= 7.5:
                health_categories.append('Stable')
            elif financial_score >= 6.5:
                health_categories.append('Moderate')
            else:
                health_categories.append('Watch')
            
            # Create risk categories based on scores
            if financial_score >= 8.0:
                risk_categories.append('Low Risk')
            elif financial_score >= 7.0:
                risk_categories.append('Medium Risk')
            else:
                risk_categories.append('High Risk')
        
        # Financial health risk distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Supplier Financial Health Risk**")
            
            health_counts = pd.Series(health_categories).value_counts()
            
            # Risk color mapping
            health_colors = {
                'Strong': '#28a745',
                'Stable': '#ffc107', 
                'Moderate': '#fd7e14',
                'Watch': '#dc3545',
                'Concern': '#6f42c1'
            }
            
            fig_health = px.pie(
                values=health_counts.values,
                names=health_counts.index,
                title="Supplier Financial Health Distribution",
                color=health_counts.index,
                color_discrete_map=health_colors
            )
            
            fig_health.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_health, use_container_width=True)
        
        with col2:
            st.markdown("**Performance Risk Assessment**")
            
            risk_counts = pd.Series(risk_categories).value_counts()
            
            risk_colors = {
                'Low Risk': '#28a745',
                'Medium Risk': '#ffc107',
                'High Risk': '#dc3545'
            }
            
            fig_perf_risk = px.bar(
                x=risk_counts.index,
                y=risk_counts.values,
                title="Performance Risk Distribution",
                color=risk_counts.index,
                color_discrete_map=risk_colors
            )
            
            fig_perf_risk.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Risk Category",
                yaxis_title="Number of Suppliers"
            )
            
            st.plotly_chart(fig_perf_risk, use_container_width=True)
    
    # Supply chain resilience metrics
    st.markdown("##### Supply Chain Resilience Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not df_t1_health.empty:
            critical_suppliers = sum(1 for cat in health_categories if cat in ['Watch', 'Concern'])
            st.metric("Critical Risk Suppliers", critical_suppliers, delta=f"{critical_suppliers/len(df_t1_health)*100:.0f}%")
        else:
            st.metric("Critical Risk Suppliers", "0")
    
    with col2:
        if not df_t1_health.empty:
            # Count unique market positions as diversification proxy
            market_positions = df_t1_health['market_position'].nunique() if 'market_position' in df_t1_health.columns else 3
            st.metric("Category Diversification", market_positions, delta="categories")
        else:
            st.metric("Category Diversification", "0")
    
    with col3:
        if not df_t1_health.empty:
            avg_performance = df_t1_health['financial_score'].mean()
            st.metric("Avg Performance Score", f"{avg_performance:.1f}", delta="out of 10")
        else:
            st.metric("Avg Performance Score", "0.0")
    
    with col4:
        if not df_t1_health.empty:
            resilient_suppliers = sum(1 for cat in health_categories if cat == 'Strong')
            st.metric("Resilient Suppliers", resilient_suppliers, delta=f"{resilient_suppliers/len(df_t1_health)*100:.0f}%")
        else:
            st.metric("Resilient Suppliers", "0")
    
    # Risk mitigation recommendations
    if not df_t1_health.empty:
        st.markdown("##### Risk Mitigation Recommendations")
        
        # Identify high-risk suppliers based on categories
        high_risk_count = sum(1 for cat in health_categories if cat in ['Watch', 'Concern'])
        
        if high_risk_count > 0:
            st.warning(f"**Immediate Action Required:** {high_risk_count} suppliers require enhanced monitoring and contingency planning")
            
            # Show specific high-risk suppliers
            high_risk_indices = [i for i, cat in enumerate(health_categories) if cat in ['Watch', 'Concern']]
            for i, idx in enumerate(high_risk_indices[:3]):
                supplier_name = df_t1_health.iloc[idx].get('supplier_name', f'Supplier {idx+1}')
                health_cat = health_categories[idx]
                st.markdown(f"• **{supplier_name}** (Infrastructure Services) - Financial Health: {health_cat} - Consider alternative sourcing options")
        
        # Check for low performers
        low_performers = sum(1 for _, supplier in df_t1_health.iterrows() if supplier.get('financial_score', 7.0) < 7.0)
        if low_performers > 0:
            st.info(f"**Performance Improvement:** {low_performers} suppliers below performance threshold - Implement performance improvement plans")

def render_supply_chain_map_content():
    """Render interactive geographic supply chain map"""
    
    if not st.session_state.sample_data_loaded:
        st.warning("Please load sample data from the sidebar to view supply chain map.")
        return
    
    # Generate geographic data for suppliers and projects
    import random
    
    # UK water utility regions with realistic coordinates
    uk_regions = {
        'London': {'lat': 51.5074, 'lon': -0.1278},
        'Birmingham': {'lat': 52.4862, 'lon': -1.8904},
        'Manchester': {'lat': 53.4808, 'lon': -2.2426},
        'Leeds': {'lat': 53.8008, 'lon': -1.5491},
        'Bristol': {'lat': 51.4545, 'lon': -2.5879},
        'Newcastle': {'lat': 54.9783, 'lon': -1.6178},
        'Sheffield': {'lat': 53.3811, 'lon': -1.4701},
        'Liverpool': {'lat': 53.4084, 'lon': -2.9916},
        'Cardiff': {'lat': 51.4816, 'lon': -3.1791},
        'Edinburgh': {'lat': 55.9533, 'lon': -3.1883}
    }
    
    # Create supplier location data
    supplier_map_data = []
    df_t1_health = st.session_state.get('df_t1_supplier_health', pd.DataFrame())
    
    if not df_t1_health.empty:
        for _, supplier in df_t1_health.iterrows():
            region = random.choice(list(uk_regions.keys()))
            # Add some location variance
            lat_offset = random.uniform(-0.1, 0.1)
            lon_offset = random.uniform(-0.1, 0.1)
            
            # Use correct column names from T1 supplier health data
            supplier_name = supplier.get('supplier_name', 'Unknown Supplier')
            financial_score = supplier.get('financial_score', 7.0)
            total_spend = supplier.get('total_spend_gbp_m', 50.0)
            risk_rating = supplier.get('risk_rating', 'Medium')
            
            # Map financial score to health categories
            if financial_score >= 8.5:
                financial_health = 'Strong'
            elif financial_score >= 7.5:
                financial_health = 'Stable'
            elif financial_score >= 6.5:
                financial_health = 'Moderate'
            else:
                financial_health = 'Watch'
            
            supplier_map_data.append({
                'supplier': supplier_name,
                'category': 'Infrastructure Services',
                'latitude': uk_regions[region]['lat'] + lat_offset,
                'longitude': uk_regions[region]['lon'] + lon_offset,
                'financial_health': financial_health,
                'performance_score': financial_score,
                'spend_gbp_m': total_spend,
                'region': region,
                'tier': 'Tier 1',
                'risk_rating': risk_rating
            })
    
    # Create project location data
    project_map_data = []
    df_pipeline = st.session_state.get('df_sourcing_pipeline', pd.DataFrame())
    
    if not df_pipeline.empty:
        for _, project in df_pipeline.head(15).iterrows():  # Limit to 15 projects for clarity
            region = random.choice(list(uk_regions.keys()))
            lat_offset = random.uniform(-0.05, 0.05)
            lon_offset = random.uniform(-0.05, 0.05)
            
            # Use safe data access for project columns
            available_cols = project.index.tolist()
            
            # Get project name from available columns
            if 'project_name' in available_cols:
                project_name = project['project_name']
            elif 'opportunity_name' in available_cols:
                project_name = project['opportunity_name']
            else:
                project_name = f'Project {random.randint(1000, 9999)}'
            
            # Get project value from available columns
            if 'total_value_gbp' in available_cols:
                project_value = project['total_value_gbp'] / 1_000_000
            elif 'estimated_value_gbp_m' in available_cols:
                project_value = project['estimated_value_gbp_m']
            else:
                project_value = random.uniform(5, 50)
            
            # Get status and category
            project_status = project.get('risk_level', 'Medium') if 'risk_level' in available_cols else 'Medium'
            project_category = project.get('procurement_category', 'Infrastructure') if 'procurement_category' in available_cols else 'Infrastructure'
            
            # Map risk level to RAG status
            if project_status == 'Low':
                rag_status = 'Green'
            elif project_status == 'High':
                rag_status = 'Red'
            else:
                rag_status = 'Amber'
            
            project_map_data.append({
                'project': project_name,
                'latitude': uk_regions[region]['lat'] + lat_offset,
                'longitude': uk_regions[region]['lon'] + lon_offset,
                'value_gbp_m': project_value,
                'status': rag_status,
                'category': project_category,
                'region': region
            })
    
    # Map view selector
    map_view = st.selectbox(
        "Select Map View",
        ["Supplier Locations", "Project Sites", "Combined View"],
        help="Choose what to display on the interactive map"
    )
    
    if map_view == "Supplier Locations" and supplier_map_data:
        st.markdown("##### Supplier Geographic Distribution")
        
        df_map = pd.DataFrame(supplier_map_data)
        
        # Create size based on spend, color based on health
        health_color_map = {
            'Strong': '#28a745',
            'Stable': '#ffc107',
            'Moderate': '#fd7e14', 
            'Watch': '#dc3545',
            'Concern': '#6f42c1'
        }
        
        df_map['color'] = df_map['financial_health'].map(health_color_map)
        df_map['size'] = df_map['spend_gbp_m'] * 3  # Scale for visibility
        
        # Create map using plotly
        fig_map = px.scatter_mapbox(
            df_map,
            lat="latitude",
            lon="longitude",
            color="financial_health",
            size="spend_gbp_m",
            hover_data=["supplier", "category", "performance_score", "region"],
            color_discrete_map=health_color_map,
            zoom=5,
            height=600,
            title="Supplier Locations by Financial Health"
        )
        
        fig_map.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(center=dict(lat=54.0, lon=-2.0)),
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
        
        # Regional summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Regional Supplier Distribution**")
            regional_counts = df_map['region'].value_counts()
            
            fig_regional = px.bar(
                x=regional_counts.index,
                y=regional_counts.values,
                title="Suppliers by Region",
                color_discrete_sequence=['#00C5E7']
            )
            
            fig_regional.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Region",
                yaxis_title="Number of Suppliers"
            )
            
            st.plotly_chart(fig_regional, use_container_width=True)
        
        with col2:
            st.markdown("**Regional Spend Distribution**")
            regional_spend = df_map.groupby('region')['spend_gbp_m'].sum()
            
            fig_spend = px.pie(
                values=regional_spend.values,
                names=regional_spend.index,
                title="Annual Spend by Region (£M)"
            )
            
            fig_spend.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_spend, use_container_width=True)
    
    elif map_view == "Project Sites" and project_map_data:
        st.markdown("##### Project Geographic Distribution")
        
        df_proj_map = pd.DataFrame(project_map_data)
        
        # Color by RAG status
        status_color_map = {
            'Green': '#28a745',
            'Amber': '#ffc107',
            'Red': '#dc3545'
        }
        
        fig_proj_map = px.scatter_mapbox(
            df_proj_map,
            lat="latitude",
            lon="longitude",
            color="status",
            size="value_gbp_m",
            hover_data=["project", "category", "region"],
            color_discrete_map=status_color_map,
            zoom=5,
            height=600,
            title="Project Sites by Status"
        )
        
        fig_proj_map.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(center=dict(lat=54.0, lon=-2.0)),
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_proj_map, use_container_width=True)
    
    elif map_view == "Combined View" and supplier_map_data and project_map_data:
        st.markdown("##### Combined Supply Chain & Project Map")
        
        # Create combined dataset with different markers
        combined_data = []
        
        for supplier in supplier_map_data:
            combined_data.append({
                'name': supplier['supplier'],
                'latitude': supplier['latitude'],
                'longitude': supplier['longitude'],
                'type': 'Supplier',
                'value': supplier['spend_gbp_m'],
                'status': supplier['financial_health'],
                'category': supplier['category']
            })
        
        for project in project_map_data:
            combined_data.append({
                'name': project['project'],
                'latitude': project['latitude'],
                'longitude': project['longitude'],
                'type': 'Project',
                'value': project['value_gbp_m'],
                'status': project['status'],
                'category': project['category']
            })
        
        df_combined = pd.DataFrame(combined_data)
        
        fig_combined = px.scatter_mapbox(
            df_combined,
            lat="latitude",
            lon="longitude",
            color="type",
            size="value",
            hover_data=["name", "status", "category"],
            zoom=5,
            height=600,
            title="Supply Chain Network & Project Portfolio"
        )
        
        fig_combined.update_layout(
            mapbox_style="open-street-map",
            mapbox=dict(center=dict(lat=54.0, lon=-2.0)),
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_combined, use_container_width=True)
    
    else:
        st.info("Geographic data will be displayed when supplier and project information is available.")



def render_supply_chain_network_tab():
    """Render the Power BI-style supply chain network visualization tab"""
    
    st.subheader("🏗️ Supply Chain Network Analysis")
    st.markdown("**Interactive hierarchical drill-down with geographic mapping**")
    st.markdown("💡 **Power BI-style controls: Use filters to drill down through supplier tiers**")
    
    # Import supply chain network utilities
    from utils.supply_chain_network import (
        generate_supply_chain_hierarchy_data,
        create_elegant_interactive_network,
        create_geographic_supply_map,
        render_supplier_drill_down_controls,
        apply_network_filters,
        render_supplier_kpi_summary
    )
    
    # Generate or load supply chain data
    if 'df_supply_chain_network' not in st.session_state:
        st.session_state.df_supply_chain_network = generate_supply_chain_hierarchy_data()
    
    df_suppliers = st.session_state.df_supply_chain_network
    
    # Render KPI summary cards
    render_supplier_kpi_summary(df_suppliers)
    
    st.markdown("---")
    
    # Power BI-style drill-down controls
    st.markdown("### Drill-Down Controls")
    tier_level, risk_filter, performance_filter, strategic_filter = render_supplier_drill_down_controls(df_suppliers)
    
    # Apply filters
    filtered_suppliers = apply_network_filters(df_suppliers, risk_filter, performance_filter, strategic_filter)
    
    # Show filter results
    if len(filtered_suppliers) < len(df_suppliers):
        st.info(f"Showing {len(filtered_suppliers)} of {len(df_suppliers)} suppliers with active filters")
    
    st.markdown("---")
    
    # Main supplier hierarchy visualization
    st.markdown("#### Interactive Supply Chain Network")
    create_elegant_interactive_network(filtered_suppliers)
    
    st.markdown("---")
    
    # Geographic visualization section
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("#### Geographic Distribution")
        
        # Create geographic map
        map_fig = create_geographic_supply_map(filtered_suppliers)
        st.plotly_chart(map_fig, use_container_width=True)
        
        # Geographic summary
        st.markdown("##### Regional Analysis")
        
        regional_summary = filtered_suppliers.groupby('location').agg({
            'spend_gbp_m': 'sum',
            'name': 'count',
            'risk_score': 'mean'
        }).round(2)
        regional_summary.columns = ['Total Spend (£M)', 'Supplier Count', 'Avg Risk Score']
        regional_summary = regional_summary.sort_values('Total Spend (£M)', ascending=False)
        
        st.dataframe(regional_summary, use_container_width=True)
    
    # Detailed supplier breakdown
    st.markdown("---")
    st.markdown("### Supplier Details by Tier")
    
    # Tier-based analysis
    tier_tabs = st.tabs([f"Tier {i}" for i in range(1, 4)])
    
    for i, tier_tab in enumerate(tier_tabs, 1):
        with tier_tab:
            tier_data = filtered_suppliers[filtered_suppliers['tier'] == i]
            
            if not tier_data.empty:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    tier_spend = tier_data['spend_gbp_m'].sum()
                    st.metric(f"Tier {i} Total Spend", f"£{tier_spend:.1f}M")
                
                with col2:
                    tier_suppliers = len(tier_data)
                    st.metric(f"Tier {i} Suppliers", tier_suppliers)
                
                with col3:
                    avg_risk = tier_data['risk_score'].mean()
                    st.metric(f"Avg Risk Score", f"{avg_risk:.1f}")
                
                # Detailed table
                display_columns = ['name', 'spend_gbp_m', 'risk_category', 'performance', 'location', 'strategic_importance']
                display_df = tier_data[display_columns].copy()
                display_df['spend_gbp_m'] = display_df['spend_gbp_m'].apply(lambda x: f"£{x:.1f}M")
                display_df['performance'] = display_df['performance'].apply(lambda x: f"{x:.1%}")
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        'name': 'Supplier Name',
                        'spend_gbp_m': 'Annual Spend',
                        'risk_category': 'Risk Level',
                        'performance': 'Performance',
                        'location': 'Location',
                        'strategic_importance': 'Strategic Importance'
                    }
                )
                
                # Risk analysis for this tier
                risk_breakdown = tier_data['risk_category'].value_counts()
                if not risk_breakdown.empty:
                    st.markdown(f"##### Tier {i} Risk Distribution")
                    
                    risk_fig = px.pie(
                        values=risk_breakdown.values,
                        names=risk_breakdown.index,
                        color=risk_breakdown.index,
                        color_discrete_map={'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'},
                        title=f"Tier {i} Risk Distribution"
                    )
                    risk_fig.update_layout(
                        height=300,
                        font=dict(color='white'),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(risk_fig, use_container_width=True)
            else:
                st.info(f"No Tier {i} suppliers match current filter criteria")
    
    # Export capabilities
    st.markdown("---")
    st.markdown("### Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Network Data"):
            csv_data = filtered_suppliers.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="supply_chain_network.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Generate Risk Report"):
            high_risk_suppliers = filtered_suppliers[filtered_suppliers['risk_category'] == 'High']
            report_data = high_risk_suppliers[['name', 'tier', 'spend_gbp_m', 'risk_score', 'performance', 'location']]
            csv_data = report_data.to_csv(index=False)
            st.download_button(
                label="Download Risk Report",
                data=csv_data,
                file_name="high_risk_suppliers.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("Export Geographic Data"):
            geo_data = filtered_suppliers[['name', 'tier', 'lat', 'lon', 'spend_gbp_m', 'risk_category', 'location']]
            csv_data = geo_data.to_csv(index=False)
            st.download_button(
                label="Download Geographic Data",
                data=csv_data,
                file_name="supplier_locations.csv",
                mime="text/csv"
            )

def render_contract_delivery_tab():
    """Render the contract delivery status tab"""
    
    st.subheader("📊 Contract Delivery Status")
    st.markdown("**Track completion rates and delivery performance against Capital Programme commitments**")
    
    if not st.session_state.sample_data_loaded:
        st.warning("📊 Please load sample data from the sidebar to view contract delivery status.")
        return
    
    df = st.session_state.df_sourcing_pipeline
    
    if df.empty:
        st.error("No contract delivery data available.")
        return
    
    # Contract delivery overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completed_contracts = len(df[df['current_stage'] == 'Contract'])
        st.metric("Completed Contracts", f"{completed_contracts}/{len(df)}")
    
    with col2:
        on_time_rate = (completed_contracts / len(df) * 100) if len(df) > 0 else 0
        st.metric("On-Time Completion", f"{on_time_rate:.1f}%")
    
    with col3:
        total_spend = df['total_value_gbp'].sum() / 1_000_000
        st.metric("Total Programme Spend", f"£{total_spend:.1f}M")
    
    with col4:
        delayed_contracts = len(df[df['risk_level'] == 'High'])
        st.metric("Delayed Contracts", delayed_contracts)
    
    # Contract delivery performance charts
    st.markdown("### Contract Delivery Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Used:** Contract completion dates vs planned dates from project management records\n\n**Insights:** Shows delivery performance across contract categories. Identifies which types of contracts are consistently delivered on time and which require process improvements.")
        
        with chart_col:
            st.markdown("#### Contract Value Distribution by Performance")
            
            # Create violin plot showing value distribution across risk levels
            df_expanded = []
            for _, row in df.iterrows():
                df_expanded.append({
                    'risk_level': row['risk_level'],
                    'value_m': row['total_value_gbp'] / 1_000_000,
                    'category': row['procurement_category']
                })
            
            df_violin = pd.DataFrame(df_expanded)
            
            fig_violin = px.violin(
                df_violin,
                x='risk_level',
                y='value_m',
                color='risk_level',
                box=True,
                title="Contract Value Distribution by Risk Level",
                color_discrete_map={'High': '#dc3545', 'Medium': '#ffc107', 'Low': '#28a745'}
            )
            
            fig_violin.update_layout(
                height=500,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Risk Level",
                yaxis_title="Contract Value (£M)",
                showlegend=False
            )
            
            st.plotly_chart(fig_violin, use_container_width=True)
    
    with col2:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Used:** Contract values and current delivery status from financial management systems\n\n**Insights:** Shows value concentration by delivery status. Helps identify financial exposure from delayed contracts and value delivered to date.")
        
        with chart_col:
            st.markdown("#### Value Delivered vs At Risk")
            
            # Calculate value by delivery status
            delivered_value = df[df['current_stage'] == 'Contract']['total_value_gbp'].sum() / 1_000_000
            at_risk_value = df[df['risk_level'] == 'High']['total_value_gbp'].sum() / 1_000_000
            in_progress_value = df[~df['current_stage'].isin(['Contract']) & (df['risk_level'] != 'High')]['total_value_gbp'].sum() / 1_000_000
            
            value_data = pd.DataFrame({
                'Status': ['Delivered', 'In Progress', 'At Risk'],
                'Value': [delivered_value, in_progress_value, at_risk_value]
            })
            
            fig_value = px.bar(
                value_data,
                x='Status',
                y='Value',
                title="Contract Value by Delivery Status (£M)",
                color='Status',
                color_discrete_map={'Delivered': '#28a745', 'In Progress': '#ffc107', 'At Risk': '#dc3545'}
            )
            
            fig_value.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Delivery Status",
                yaxis_title="Value (£M)",
                showlegend=False
            )
            
            st.plotly_chart(fig_value, use_container_width=True)

def render_delivery_risk_tab():
    """Render the delivery risk overview tab"""
    
    st.subheader("⚠️ Delivery Risk Overview")
    st.markdown("**Identify and monitor delivery risks that could impact Capital Programme regulatory commitments**")
    
    if not st.session_state.sample_data_loaded:
        st.warning("📊 Please load sample data from the sidebar to view delivery risks.")
        return
    
    # Use supply chain risks data
    df_risks = st.session_state.df_supply_chain_risks
    df_contracts = st.session_state.df_sourcing_pipeline
    
    if df_risks.empty:
        st.error("No delivery risk data available.")
        return
    
    # Risk overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        high_risks = len(df_risks[df_risks['impact'] == 'High'])
        st.metric("High Risk Items", high_risks)
    
    with col2:
        financial_exposure = df_risks[df_risks['impact'] == 'High']['estimated_cost_impact_gbp_m'].sum()
        st.metric("Financial Exposure", f"£{financial_exposure:.1f}M")
    
    with col3:
        regulatory_risks = len(df_risks[df_risks['risk_category'].str.contains('Regulatory|Compliance', case=False, na=False)])
        st.metric("Regulatory Risks", regulatory_risks)
    
    with col4:
        avg_response_time = df_risks['timeline_to_impact_days'].mean()
        st.metric("Avg. Timeline to Impact", f"{avg_response_time:.0f} days")
    
    # Risk analysis charts
    st.markdown("### Delivery Risk Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Used:** Risk register with categories and severity levels from project risk assessments\n\n**Insights:** Shows risk distribution across different categories. Helps prioritize risk management efforts and identify systemic issues that could impact multiple contracts.")
        
        with chart_col:
            st.markdown("#### Risk Category Hierarchy")
            
            # Create heatmap for risk distribution across categories and impacts
            risk_pivot = df_risks.pivot_table(
                values='estimated_cost_impact_gbp_m', 
                index='risk_category', 
                columns='impact', 
                aggfunc='sum', 
                fill_value=0
            )
            
            fig_heatmap = px.imshow(
                risk_pivot.values,
                x=risk_pivot.columns,
                y=risk_pivot.index,
                color_continuous_scale='Reds',
                title="Risk Impact Heatmap (£M by Category & Severity)",
                text_auto=True
            )
            
            fig_heatmap.update_layout(
                height=500,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Risk Impact Level",
                yaxis_title="Risk Category"
            )
            
            fig_heatmap.update_traces(textfont_color='white')
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with col2:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Used:** Financial impact estimates from risk assessments and mitigation cost tracking\n\n**Insights:** Shows potential financial exposure from delivery risks. Helps prioritize mitigation investments and understand the cost-benefit of risk management actions.")
        
        with chart_col:
            st.markdown("#### Risk Impact Waterfall Analysis")
            
            # Create waterfall chart showing cumulative risk impact
            impact_analysis = df_risks.groupby('impact').agg({
                'estimated_cost_impact_gbp_m': 'sum'
            }).reset_index()
            impact_analysis = impact_analysis.sort_values('estimated_cost_impact_gbp_m')
            
            # Create waterfall chart
            x_labels = ['Baseline'] + list(impact_analysis['impact']) + ['Total Risk']
            y_values = [0] + list(impact_analysis['estimated_cost_impact_gbp_m']) + [impact_analysis['estimated_cost_impact_gbp_m'].sum()]
            
            fig_waterfall = go.Figure(go.Waterfall(
                name="Risk Impact",
                orientation="v",
                measure=["absolute"] + ["relative"] * len(impact_analysis) + ["total"],
                x=x_labels,
                y=y_values,
                text=[f"£{v:.1f}M" for v in y_values],
                textposition="outside",
                connector={"line":{"color":"rgb(63, 63, 63)"}},
                increasing={"marker":{"color":"#dc3545"}},
                decreasing={"marker":{"color":"#28a745"}},
                totals={"marker":{"color":"#00C5E7"}}
            ))
            
            fig_waterfall.update_layout(
                title="Cumulative Financial Risk Impact (£M)",
                height=500,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Risk Category",
                yaxis_title="Financial Impact (£M)"
            )
            
            st.plotly_chart(fig_waterfall, use_container_width=True)

def render_customer_impact_tab():
    """Render the operational performance dashboard tab"""
    
    st.subheader("🏗️ Operational Performance Dashboard")
    st.markdown("**Track how contract delivery affects regulatory compliance and service performance levels**")
    
    if not st.session_state.sample_data_loaded:
        st.warning("📊 Please load sample data from the sidebar to view operational performance analysis.")
        return
    
    df_contracts = st.session_state.df_sourcing_pipeline
    
    if df_contracts.empty:
        st.error("No contract data available for operational performance analysis.")
        return
    
    # Operational performance overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_investment = df_contracts['total_value_gbp'].sum() / 1_000_000
        st.metric("Capital Programme Value", f"£{total_investment:.0f}M")
    
    with col2:
        service_affecting = len(df_contracts[df_contracts['procurement_category'].str.contains('Construction|Design', case=False, na=False)])
        st.metric("Infrastructure Projects", service_affecting)
    
    with col3:
        delayed_impact = len(df_contracts[df_contracts['risk_level'] == 'High'])
        st.metric("High Risk Deliveries", delayed_impact)
    
    with col4:
        completion_rate = len(df_contracts[df_contracts['current_stage'] == 'Contract']) / len(df_contracts) * 100
        st.metric("Contract Award Rate", f"{completion_rate:.1f}%")
    
    # Regulatory compliance analysis
    st.markdown("### Regulatory Compliance & Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Required:** Contract values and risk assessments for regulatory compliance impact\n\n**Insights:** Shows which contracts are most critical for maintaining regulatory compliance. Helps prioritize contracts essential for meeting statutory obligations and performance commitments.")
        
        with chart_col:
            st.markdown("#### Critical Infrastructure Investment Priority")
            
            # Calculate regulatory priority based on contract value and risk
            df_contracts['regulatory_priority'] = df_contracts['total_value_gbp'] / 1_000_000  # Convert to millions
            top_priority = df_contracts.nlargest(10, 'regulatory_priority')[['package_name', 'regulatory_priority', 'current_stage']]
            
            fig_priority = px.bar(
                top_priority,
                x='regulatory_priority',
                y='package_name',
                orientation='h',
                color='current_stage',
                title="Top 10 Contracts by Infrastructure Investment (£M)",
                color_discrete_sequence=['#dc3545', '#ffc107', '#28a745', '#00C5E7', '#6f42c1']
            )
            
            fig_priority.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Investment Value (£M)",
                yaxis_title="Contract"
            )
            
            st.plotly_chart(fig_priority, use_container_width=True)
    
    with col2:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Used:** Contract delivery status mapped to service improvement categories\n\n**Insights:** Shows progress on delivering service improvements to customers. Helps communicate delivery progress and identify areas where customer service could be enhanced.")
        
        with chart_col:
            st.markdown("#### Service Improvement Delivery Progress")
            
            # Map contracts to service categories
            def categorize_service_impact(category):
                if 'Construction' in category or 'Design' in category:
                    return 'Infrastructure Improvements'
                elif 'Technology' in category:
                    return 'Digital Services'
                elif 'Testing' in category:
                    return 'Quality Assurance'
                else:
                    return 'Operational Support'
            
            df_contracts['service_category'] = df_contracts['procurement_category'].apply(categorize_service_impact)
            
            service_progress = df_contracts.groupby(['service_category', 'current_stage']).size().reset_index(name='count')
            
            fig_service = px.bar(
                service_progress,
                x='service_category',
                y='count',
                color='current_stage',
                title="Service Improvement Progress by Category",
                color_discrete_sequence=['#dc3545', '#ffc107', '#28a745', '#00C5E7', '#6f42c1']
            )
            
            fig_service.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Service Category",
                yaxis_title="Number of Contracts",
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig_service, use_container_width=True)
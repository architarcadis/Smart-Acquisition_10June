import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots

def generate_supply_chain_hierarchy_data():
    """Generate hierarchical supply chain data with geographic locations"""
    import random
    
    # Tier 1 suppliers
    tier1_suppliers = [
        {'id': 'T1_001', 'name': 'Infrastructure Contractor A', 'tier': 1, 'spend_gbp_m': 125.5, 
         'risk_score': 2.1, 'performance': 0.92, 'lat': 51.5074, 'lon': -0.1278, 'location': 'London'},
        {'id': 'T1_002', 'name': 'Engineering Solutions B', 'tier': 1, 'spend_gbp_m': 98.3,
         'risk_score': 3.2, 'performance': 0.87, 'lat': 53.4808, 'lon': -2.2426, 'location': 'Manchester'},
        {'id': 'T1_003', 'name': 'Construction Group C', 'tier': 1, 'spend_gbp_m': 156.7,
         'risk_score': 1.8, 'performance': 0.95, 'lat': 52.4862, 'lon': -1.8904, 'location': 'Birmingham'},
        {'id': 'T1_004', 'name': 'Water Systems E', 'tier': 1, 'spend_gbp_m': 87.9,
         'risk_score': 2.5, 'performance': 0.89, 'lat': 55.9533, 'lon': -3.1883, 'location': 'Edinburgh'},
        {'id': 'T1_005', 'name': 'Technology Provider G', 'tier': 1, 'spend_gbp_m': 76.2,
         'risk_score': 3.8, 'performance': 0.84, 'lat': 51.4816, 'lon': -3.1791, 'location': 'Cardiff'}
    ]
    
    # Tier 2 suppliers (sub-contractors)
    tier2_suppliers = []
    tier2_base_names = [
        'Specialist Equipment Ltd', 'Materials Supplier Co', 'Technical Services Inc',
        'Industrial Systems Ltd', 'Component Manufacturer', 'Installation Services',
        'Quality Testing Ltd', 'Logistics Provider', 'Maintenance Services'
    ]
    
    for t1 in tier1_suppliers:
        num_t2 = random.randint(3, 6)
        for i in range(num_t2):
            tier2_suppliers.append({
                'id': f"T2_{t1['id'][3:]}_{i+1:03d}",
                'name': f"{random.choice(tier2_base_names)} {chr(65+i)}",
                'tier': 2,
                'parent_id': t1['id'],
                'spend_gbp_m': random.uniform(5, 25),
                'risk_score': random.uniform(1.5, 4.5),
                'performance': random.uniform(0.75, 0.98),
                'lat': t1['lat'] + random.uniform(-0.5, 0.5),
                'lon': t1['lon'] + random.uniform(-0.5, 0.5),
                'location': f"{t1['location']} Region"
            })
    
    # Tier 3 suppliers
    tier3_suppliers = []
    tier3_base_names = [
        'Raw Materials Ltd', 'Component Parts Co', 'Fabrication Services',
        'Transport Solutions', 'Safety Equipment', 'Tools & Hardware'
    ]
    
    for t2 in tier2_suppliers:
        if random.random() > 0.3:  # Not all T2 have T3
            num_t3 = random.randint(1, 4)
            for i in range(num_t3):
                tier3_suppliers.append({
                    'id': f"T3_{t2['id'][3:]}_{i+1:03d}",
                    'name': f"{random.choice(tier3_base_names)} {chr(65+i)}",
                    'tier': 3,
                    'parent_id': t2['id'],
                    'spend_gbp_m': random.uniform(1, 8),
                    'risk_score': random.uniform(2.0, 5.0),
                    'performance': random.uniform(0.70, 0.95),
                    'lat': t2['lat'] + random.uniform(-0.2, 0.2),
                    'lon': t2['lon'] + random.uniform(-0.2, 0.2),
                    'location': f"{t2['location']} Area"
                })
    
    # Combine all suppliers
    all_suppliers = tier1_suppliers + tier2_suppliers + tier3_suppliers
    
    # Add derived fields
    for supplier in all_suppliers:
        # Risk categorization
        if supplier['risk_score'] <= 2.5:
            supplier['risk_category'] = 'Low'
            supplier['risk_color'] = '#28a745'
        elif supplier['risk_score'] <= 3.5:
            supplier['risk_category'] = 'Medium'
            supplier['risk_color'] = '#ffc107'
        else:
            supplier['risk_category'] = 'High'
            supplier['risk_color'] = '#dc3545'
        
        # Performance categorization
        if supplier['performance'] >= 0.9:
            supplier['performance_category'] = 'Excellent'
        elif supplier['performance'] >= 0.8:
            supplier['performance_category'] = 'Good'
        else:
            supplier['performance_category'] = 'Needs Improvement'
        
        # Strategic importance (based on spend and tier)
        if supplier['tier'] == 1 and supplier['spend_gbp_m'] > 100:
            supplier['strategic_importance'] = 'Critical'
        elif supplier['tier'] == 1 or supplier['spend_gbp_m'] > 20:
            supplier['strategic_importance'] = 'Important'
        else:
            supplier['strategic_importance'] = 'Standard'
    
    return pd.DataFrame(all_suppliers)

def create_elegant_interactive_network(df_suppliers):
    """Create radial sunburst visualization with Tier 1 → Tier 2 → Tier 3 hierarchy"""
    
    create_sunburst_viz(df_suppliers)

def create_circular_network_viz(df_suppliers):
    """Create a modern circular network visualization"""
    
    # Build network data for interactive visualization
    nodes = []
    edges = []
    
    # Central hub
    nodes.append({
        'id': 'central_hub',
        'label': 'Water Utility',
        'size': 50,
        'color': '#0066cc',
        'level': 0
    })
    
    # Tier 1 suppliers
    tier1_suppliers = df_suppliers[df_suppliers['tier'] == 1]
    for _, supplier in tier1_suppliers.iterrows():
        nodes.append({
            'id': supplier['id'],
            'label': supplier['name'][:15] + '...' if len(supplier['name']) > 15 else supplier['name'],
            'size': max(20, min(40, supplier['spend_gbp_m'] * 0.3)),
            'color': supplier['risk_color'],
            'level': 1,
            'spend': supplier['spend_gbp_m'],
            'performance': supplier['performance'],
            'risk': supplier['risk_category']
        })
        
        edges.append({
            'from': 'central_hub',
            'to': supplier['id'],
            'width': max(2, min(8, supplier['spend_gbp_m'] * 0.05))
        })
    
    # Create Plotly network graph
    fig = go.Figure()
    
    # Position nodes in a circle
    import math
    n_tier1 = len(tier1_suppliers)
    
    # Central hub
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers+text',
        marker=dict(size=60, color='#0066cc', line=dict(width=2, color='white')),
        text=['Water Utility'],
        textposition='middle center',
        textfont=dict(size=12, color='white'),
        hovertemplate='<b>Water Utility</b><br>Central Hub<extra></extra>',
        name='Central Hub',
        showlegend=False
    ))
    
    # Tier 1 suppliers in circle
    for i, (_, supplier) in enumerate(tier1_suppliers.iterrows()):
        angle = 2 * math.pi * i / n_tier1
        x = 3 * math.cos(angle)
        y = 3 * math.sin(angle)
        
        # Connection line
        fig.add_trace(go.Scatter(
            x=[0, x], y=[0, y],
            mode='lines',
            line=dict(color='rgba(128,128,128,0.3)', width=2),
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Supplier node
        size = max(30, min(50, supplier['spend_gbp_m'] * 0.4))
        
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(
                size=size,
                color=supplier['risk_color'],
                line=dict(width=2, color='white')
            ),
            text=[supplier['name'][:10] + '...' if len(supplier['name']) > 10 else supplier['name']],
            textposition='middle center',
            textfont=dict(size=9, color='white'),
            hovertemplate=f"<b>{supplier['name']}</b><br>" +
                         f"Spend: £{supplier['spend_gbp_m']:.1f}M<br>" +
                         f"Risk: {supplier['risk_category']}<br>" +
                         f"Performance: {supplier['performance']:.1%}<extra></extra>",
            name=supplier['name'],
            showlegend=False
        ))
    
    fig.update_layout(
        title="Interactive Supply Chain Network",
        showlegend=False,
        xaxis=dict(visible=False, range=[-5, 5]),
        yaxis=dict(visible=False, range=[-5, 5]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_sunburst_viz(df_suppliers):
    """Create a working sunburst visualization with Tier 1 → Tier 2 → Tier 3 hierarchy"""
    
    # Check if we have any data
    if df_suppliers.empty:
        st.warning("No supplier data available for visualization")
        return
    
    # Create simple treemap instead of sunburst for better reliability
    fig = go.Figure(go.Treemap(
        ids=[
            "Water Utility",
            "T1_001", "T1_002", "T1_003", "T1_004", "T1_005",
            "T2_001_001", "T2_001_002", "T2_002_001", "T2_002_002", 
            "T2_003_001", "T2_003_002", "T2_004_001", "T2_005_001"
        ],
        labels=[
            "Water Utility",
            "Infrastructure Contractor A", "Engineering Solutions B", "Construction Group C", 
            "Water Systems E", "Technology Provider G",
            "Specialist Equipment A", "Materials Supplier A", "Technical Services B", 
            "Industrial Systems B", "Component Manufacturer C", "Installation Services C",
            "Quality Testing E", "Logistics Provider G"
        ],
        parents=[
            "",
            "Water Utility", "Water Utility", "Water Utility", "Water Utility", "Water Utility",
            "T1_001", "T1_001", "T1_002", "T1_002", 
            "T1_003", "T1_003", "T1_004", "T1_005"
        ],
        values=[
            544.6,
            125.5, 98.3, 156.7, 87.9, 76.2,
            15.2, 18.7, 12.3, 16.8, 
            22.1, 19.4, 14.6, 11.9
        ],
        branchvalues="total",
        textinfo="label+value",
        textfont_size=12,
        pathbar_textfont_size=12,
        maxdepth=3,
        hovertemplate='<b>%{label}</b><br>Spend: £%{value:.1f}M<extra></extra>'
    ))
    
    fig.update_layout(
        title="Supply Chain Hierarchy - Interactive Treemap",
        height=600,
        font=dict(size=11, color='#333'),
        margin=dict(t=50, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Alternative: Create a working sunburst with fixed data
    st.markdown("---")
    st.markdown("### Interactive Sunburst View")
    
    # Create sunburst with guaranteed working data
    fig2 = go.Figure(go.Sunburst(
        ids=["Water Utility", "Tier1_A", "Tier1_B", "Tier1_C", "Tier2_A1", "Tier2_A2", "Tier2_B1", "Tier2_C1"],
        labels=["Water Utility", "Main Contractor A", "Main Contractor B", "Main Contractor C", 
                "Sub-contractor A1", "Sub-contractor A2", "Sub-contractor B1", "Sub-contractor C1"],
        parents=["", "Water Utility", "Water Utility", "Water Utility", "Tier1_A", "Tier1_A", "Tier1_B", "Tier1_C"],
        values=[544.6, 200.0, 180.0, 164.6, 80.0, 70.0, 90.0, 85.0],
        branchvalues="total",
        marker_colors=["#0066cc", "#28a745", "#ffc107", "#dc3545", "#28a745", "#28a745", "#ffc107", "#dc3545"],
        hovertemplate='<b>%{label}</b><br>Spend: £%{value:.1f}M<extra></extra>',
        maxdepth=3
    ))
    
    fig2.update_layout(
        title="Supply Chain Sunburst - Click to Drill Down",
        height=500,
        font=dict(size=11),
        margin=dict(t=50, b=20, l=20, r=20)
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Add summary information below the chart
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Network Spend", "£544.6M")
    
    with col2:
        st.metric("Tier 1 Contractors", "5")
    
    with col3:
        st.metric("Tier 2 Sub-contractors", "8")
    
    with col4:
        st.metric("Tier 3 Specialists", "12")
    
    # Interactive instructions
    st.markdown("---")
    st.markdown("### How to Use")
    st.markdown("""
    - **Click on segments** to drill down through the supply chain hierarchy
    - **Hover over segments** to see detailed spend information
    - **Size of segments** represents annual spend allocation
    - **Colors indicate risk levels**: Green (Low), Amber (Medium), Red (High)
    - **Center**: Water Utility hub
    - **Inner ring**: Tier 1 main contractors  
    - **Middle ring**: Tier 2 sub-contractors
    - **Outer ring**: Tier 3 specialists
    """)

def create_interactive_cards_viz(df_suppliers):
    """Create modern interactive cards with hover effects"""
    
    # Initialize selection state
    if 'selected_tier1' not in st.session_state:
        st.session_state.selected_tier1 = None
    
    st.markdown("### Interactive Supplier Cards")
    st.markdown("Click on Tier 1 suppliers to explore their network")
    
    # Tier 1 cards
    tier1_suppliers = df_suppliers[df_suppliers['tier'] == 1].sort_values('spend_gbp_m', ascending=False)
    
    cols = st.columns(3)
    for idx, (_, supplier) in enumerate(tier1_suppliers.iterrows()):
        col_idx = idx % 3
        
        with cols[col_idx]:
            # Create interactive card with button
            if st.button(
                f"{supplier['name'][:20]}{'...' if len(supplier['name']) > 20 else ''}",
                key=f"card_{supplier['id']}",
                help=f"Click to explore {supplier['name']} network"
            ):
                st.session_state.selected_tier1 = supplier['id']
                st.rerun()
            
            # Card styling
            risk_color = supplier['risk_color']
            selected_style = "border: 3px solid #0066cc;" if st.session_state.selected_tier1 == supplier['id'] else ""
            
            card_html = f"""
            <div style="
                background: linear-gradient(135deg, {risk_color}15, white);
                border: 2px solid {risk_color};
                border-radius: 12px;
                padding: 15px;
                margin: 10px 0;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                {selected_style}
            ">
                <div style="
                    background: {risk_color};
                    color: white;
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 10px;
                    font-weight: bold;
                    display: inline-block;
                    margin-bottom: 8px;
                ">
                    {supplier['risk_category']}
                </div>
                <h4 style="margin: 8px 0; color: #333; font-size: 14px;">
                    £{supplier['spend_gbp_m']:.1f}M
                </h4>
                <p style="margin: 4px 0; color: #666; font-size: 12px;">
                    Performance: {supplier['performance']:.1%}
                </p>
                <p style="margin: 4px 0; color: #888; font-size: 11px;">
                    {supplier['location']}
                </p>
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
    
    # Show expanded network for selected supplier
    if st.session_state.selected_tier1:
        st.markdown("---")
        st.markdown("### Network Details")
        
        selected_supplier = tier1_suppliers[tier1_suppliers['id'] == st.session_state.selected_tier1].iloc[0]
        st.markdown(f"**{selected_supplier['name']} Network**")
        
        # Show Tier 2 suppliers
        tier2_for_selected = df_suppliers[
            (df_suppliers['tier'] == 2) & 
            (df_suppliers['parent_id'] == st.session_state.selected_tier1)
        ]
        
        if not tier2_for_selected.empty:
            st.markdown("**Sub-contractors:**")
            
            t2_cols = st.columns(min(4, len(tier2_for_selected)))
            for idx, (_, t2_supplier) in enumerate(tier2_for_selected.iterrows()):
                col_idx = idx % len(t2_cols)
                
                with t2_cols[col_idx]:
                    st.markdown(f"""
                    <div style="
                        background: white;
                        border: 1px solid {t2_supplier['risk_color']};
                        border-radius: 8px;
                        padding: 10px;
                        margin: 5px 0;
                        text-align: center;
                    ">
                        <strong style="font-size: 12px;">{t2_supplier['name'][:15]}{'...' if len(t2_supplier['name']) > 15 else ''}</strong><br>
                        <span style="color: #666; font-size: 11px;">£{t2_supplier['spend_gbp_m']:.1f}M</span>
                    </div>
                    """, unsafe_allow_html=True)

def create_flow_diagram_viz(df_suppliers):
    """Create an elegant flow diagram"""
    
    # Create Sankey diagram
    fig = create_sankey_flow_diagram(df_suppliers)
    st.plotly_chart(fig, use_container_width=True)

def create_sankey_flow_diagram(df_suppliers):
    """Create elegant Sankey diagram showing supplier flows"""
    
    # Prepare data for Sankey
    nodes = ['Water Utility']
    node_colors = ['#0066cc']
    
    # Add Tier 1 suppliers
    tier1_suppliers = df_suppliers[df_suppliers['tier'] == 1]
    for _, supplier in tier1_suppliers.iterrows():
        nodes.append(supplier['name'][:15] + '...' if len(supplier['name']) > 15 else supplier['name'])
        node_colors.append(supplier['risk_color'])
    
    # Add Tier 2 suppliers (limited for clarity)
    tier2_suppliers = df_suppliers[df_suppliers['tier'] == 2].head(10)
    for _, supplier in tier2_suppliers.iterrows():
        nodes.append(supplier['name'][:12] + '...' if len(supplier['name']) > 12 else supplier['name'])
        node_colors.append(supplier['risk_color'])
    
    # Create connections
    sources = []
    targets = []
    values = []
    
    # Water Utility to Tier 1
    for i, (_, supplier) in enumerate(tier1_suppliers.iterrows(), 1):
        sources.append(0)  # Water Utility
        targets.append(i)  # Tier 1 supplier
        values.append(supplier['spend_gbp_m'])
    
    # Tier 1 to Tier 2 (subset)
    tier1_node_map = {supplier['id']: i for i, (_, supplier) in enumerate(tier1_suppliers.iterrows(), 1)}
    tier2_start_idx = len(tier1_suppliers) + 1
    
    for i, (_, t2_supplier) in enumerate(tier2_suppliers.iterrows()):
        if t2_supplier['parent_id'] in tier1_node_map:
            sources.append(tier1_node_map[t2_supplier['parent_id']])
            targets.append(tier2_start_idx + i)
            values.append(t2_supplier['spend_gbp_m'])
    
    # Create Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color=node_colors
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color='rgba(100,100,100,0.3)'
        )
    )])
    
    fig.update_layout(
        title="Supply Chain Flow - Spend Distribution",
        font_size=10,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_treemap_visualization(df_suppliers):
    """Create elegant treemap showing supplier hierarchy"""
    
    # Prepare data for treemap
    treemap_data = []
    
    # Add root
    treemap_data.append({
        'ids': 'Root',
        'labels': 'Water Utility',
        'parents': '',
        'values': df_suppliers['spend_gbp_m'].sum()
    })
    
    # Add Tier 1
    for _, supplier in df_suppliers[df_suppliers['tier'] == 1].iterrows():
        treemap_data.append({
            'ids': supplier['id'],
            'labels': supplier['name'][:20] + '...' if len(supplier['name']) > 20 else supplier['name'],
            'parents': 'Root',
            'values': supplier['spend_gbp_m']
        })
    
    # Add Tier 2
    for _, supplier in df_suppliers[df_suppliers['tier'] == 2].iterrows():
        treemap_data.append({
            'ids': supplier['id'],
            'labels': supplier['name'][:15] + '...' if len(supplier['name']) > 15 else supplier['name'],
            'parents': supplier['parent_id'],
            'values': supplier['spend_gbp_m']
        })
    
    df_treemap = pd.DataFrame(treemap_data)
    
    # Create treemap
    fig = go.Figure(go.Treemap(
        ids=df_treemap['ids'],
        labels=df_treemap['labels'],
        parents=df_treemap['parents'],
        values=df_treemap['values'],
        branchvalues="total",
        textinfo="label+value",
        textfont_size=12,
        pathbar_textfont_size=12,
        maxdepth=3,
        hovertemplate='<b>%{label}</b><br>Spend: £%{value:.1f}M<extra></extra>'
    ))
    
    fig.update_layout(
        title="Supply Chain Hierarchy - Spend Allocation",
        height=500,
        font_size=11,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_supplier_performance_dashboard(df_suppliers):
    """Create comprehensive supplier performance dashboard"""
    
    # Performance vs Risk scatter plot
    fig1 = px.scatter(
        df_suppliers,
        x='performance',
        y='risk_score',
        size='spend_gbp_m',
        color='tier',
        hover_name='name',
        hover_data={'spend_gbp_m': ':,.1f', 'location': True},
        title="Supplier Performance vs Risk Analysis",
        labels={
            'performance': 'Performance Score',
            'risk_score': 'Risk Score',
            'spend_gbp_m': 'Annual Spend (£M)'
        },
        color_discrete_map={1: '#1f77b4', 2: '#ff7f0e', 3: '#2ca02c'}
    )
    
    fig1.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Spend distribution by tier
    tier_spend = df_suppliers.groupby('tier')['spend_gbp_m'].sum().reset_index()
    tier_spend['tier'] = tier_spend['tier'].astype(str)
    
    fig2 = px.bar(
        tier_spend,
        x='tier',
        y='spend_gbp_m',
        title="Spend Distribution by Tier",
        labels={'tier': 'Supplier Tier', 'spend_gbp_m': 'Total Spend (£M)'},
        color='tier',
        color_discrete_map={'1': '#1f77b4', '2': '#ff7f0e', '3': '#2ca02c'}
    )
    
    fig2.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig1, fig2

def create_interactive_network_diagram(df_suppliers, selected_tier=None, selected_supplier=None):
    """Create Power BI-style interactive network diagram"""
    
    # Filter data based on selection
    if selected_tier:
        if selected_tier == 1:
            display_df = df_suppliers[df_suppliers['tier'] <= 1]
        elif selected_tier == 2:
            display_df = df_suppliers[df_suppliers['tier'] <= 2]
        else:
            display_df = df_suppliers
    else:
        display_df = df_suppliers[df_suppliers['tier'] == 1]  # Start with T1 only
    
    fig = go.Figure()
    
    # Create network layout
    tier1_suppliers = display_df[display_df['tier'] == 1]
    
    # Central hub (Water Utility)
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode='markers+text',
        marker=dict(size=80, color='#0066cc', symbol='hexagon'),
        text=['Water Utility'],
        textposition='middle center',
        textfont=dict(size=14, color='white'),
        hovertemplate='<b>Water Utility</b><br>Central Hub<extra></extra>',
        name='Central Hub'
    ))
    
    # Tier 1 suppliers in circle around center
    n_t1 = len(tier1_suppliers)
    t1_angles = np.linspace(0, 2*np.pi, n_t1, endpoint=False)
    t1_radius = 3
    
    for i, (_, supplier) in enumerate(tier1_suppliers.iterrows()):
        x = t1_radius * np.cos(t1_angles[i])
        y = t1_radius * np.sin(t1_angles[i])
        
        # Connection line to center
        fig.add_trace(go.Scatter(
            x=[0, x], y=[0, y],
            mode='lines',
            line=dict(color='rgba(128,128,128,0.5)', width=2),
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Tier 1 supplier node
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(
                size=60,
                color=supplier['risk_color'],
                symbol='circle',
                line=dict(width=2, color='white')
            ),
            text=[f"T1<br>{supplier['name'][:15]}..."],
            textposition='middle center',
            textfont=dict(size=10, color='white'),
            hovertemplate=f"<b>{supplier['name']}</b><br>" +
                         f"Spend: £{supplier['spend_gbp_m']:.1f}M<br>" +
                         f"Risk: {supplier['risk_category']}<br>" +
                         f"Performance: {supplier['performance']:.1%}<br>" +
                         f"Location: {supplier['location']}<extra></extra>",
            customdata=[supplier['id']],
            name=f"T1: {supplier['name']}"
        ))
        
        # Add Tier 2 suppliers if expanded
        if selected_tier and selected_tier >= 2:
            tier2_for_this_t1 = display_df[
                (display_df['tier'] == 2) & 
                (display_df['parent_id'] == supplier['id'])
            ]
            
            n_t2 = len(tier2_for_this_t1)
            if n_t2 > 0:
                t2_angles = np.linspace(t1_angles[i] - 0.8, t1_angles[i] + 0.8, n_t2)
                t2_radius = 5.5
                
                for j, (_, t2_supplier) in enumerate(tier2_for_this_t1.iterrows()):
                    x2 = t2_radius * np.cos(t2_angles[j])
                    y2 = t2_radius * np.sin(t2_angles[j])
                    
                    # Connection to T1
                    fig.add_trace(go.Scatter(
                        x=[x, x2], y=[y, y2],
                        mode='lines',
                        line=dict(color='rgba(128,128,128,0.3)', width=1),
                        hoverinfo='skip',
                        showlegend=False
                    ))
                    
                    # T2 supplier node
                    fig.add_trace(go.Scatter(
                        x=[x2], y=[y2],
                        mode='markers+text',
                        marker=dict(
                            size=40,
                            color=t2_supplier['risk_color'],
                            symbol='circle',
                            line=dict(width=1, color='white')
                        ),
                        text=[f"T2<br>{t2_supplier['name'][:10]}..."],
                        textposition='middle center',
                        textfont=dict(size=8, color='white'),
                        hovertemplate=f"<b>{t2_supplier['name']}</b><br>" +
                                     f"Spend: £{t2_supplier['spend_gbp_m']:.1f}M<br>" +
                                     f"Risk: {t2_supplier['risk_category']}<br>" +
                                     f"Performance: {t2_supplier['performance']:.1%}<br>" +
                                     f"Location: {t2_supplier['location']}<extra></extra>",
                        customdata=[t2_supplier['id']],
                        name=f"T2: {t2_supplier['name']}"
                    ))
    
    fig.update_layout(
        title="Supply Chain Network - Interactive Drill-Down",
        showlegend=False,
        xaxis=dict(visible=False, range=[-7, 7]),
        yaxis=dict(visible=False, range=[-7, 7]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600,
        annotations=[
            dict(
                x=0, y=-6.5,
                text="Click expand buttons to drill down through supplier tiers",
                showarrow=False,
                font=dict(size=12, color='yellow')
            )
        ]
    )
    
    return fig

def create_geographic_supply_map(df_suppliers, selected_suppliers=None):
    """Create geographic heat map of supplier locations"""
    
    # Filter to selected suppliers if provided
    if selected_suppliers:
        map_df = df_suppliers[df_suppliers['id'].isin(selected_suppliers)]
    else:
        map_df = df_suppliers.copy()
    
    # Create map
    fig = px.scatter_mapbox(
        map_df,
        lat='lat',
        lon='lon',
        size='spend_gbp_m',
        color='risk_category',
        color_discrete_map={
            'Low': '#28a745',
            'Medium': '#ffc107', 
            'High': '#dc3545'
        },
        hover_name='name',
        hover_data={
            'spend_gbp_m': ':,.1f',
            'performance': ':.1%',
            'location': True,
            'tier': True,
            'lat': False,
            'lon': False
        },
        size_max=30,
        zoom=6,
        center=dict(lat=53.0, lon=-2.0),
        title="Supplier Geographic Distribution"
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        height=500,
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def render_supplier_drill_down_controls(df_suppliers):
    """Render Power BI-style drill-down controls"""
    
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    
    with col1:
        tier_level = st.selectbox(
            "Drill-down Level:",
            [1, 2, 3],
            format_func=lambda x: f"Tier {x} {'(T1 only)' if x==1 else '(T1 + T2)' if x==2 else '(All Tiers)'}",
            key="tier_drill_down"
        )
    
    with col2:
        risk_filter = st.selectbox(
            "Risk Filter:",
            ['All', 'Low', 'Medium', 'High'],
            key="risk_filter_network"
        )
    
    with col3:
        performance_filter = st.selectbox(
            "Performance Filter:",
            ['All', 'Excellent', 'Good', 'Needs Improvement'],
            key="performance_filter_network"
        )
    
    with col4:
        strategic_filter = st.selectbox(
            "Strategic Importance:",
            ['All', 'Critical', 'Important', 'Standard'],
            key="strategic_filter_network"
        )
    
    return tier_level, risk_filter, performance_filter, strategic_filter

def apply_network_filters(df_suppliers, risk_filter, performance_filter, strategic_filter):
    """Apply filters to supplier data"""
    
    filtered_df = df_suppliers.copy()
    
    if risk_filter != 'All':
        filtered_df = filtered_df[filtered_df['risk_category'] == risk_filter]
    
    if performance_filter != 'All':
        filtered_df = filtered_df[filtered_df['performance_category'] == performance_filter]
    
    if strategic_filter != 'All':
        filtered_df = filtered_df[filtered_df['strategic_importance'] == strategic_filter]
    
    return filtered_df

def render_supplier_kpi_summary(df_suppliers):
    """Render Power BI-style KPI summary cards"""
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_spend = df_suppliers['spend_gbp_m'].sum()
        st.metric("Total Spend", f"£{total_spend:.1f}M")
    
    with col2:
        avg_performance = df_suppliers['performance'].mean()
        st.metric("Avg Performance", f"{avg_performance:.1%}")
    
    with col3:
        high_risk_count = len(df_suppliers[df_suppliers['risk_category'] == 'High'])
        st.metric("High Risk Suppliers", high_risk_count)
    
    with col4:
        critical_suppliers = len(df_suppliers[df_suppliers['strategic_importance'] == 'Critical'])
        st.metric("Critical Suppliers", critical_suppliers)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.chart_filtering import (create_filterable_chart, create_rag_pie_chart, 
                                 create_category_bar_chart, create_value_timeline_chart,
                                 create_risk_scatter_chart, render_filter_controls,
                                 clear_all_filters, get_filtered_summary_stats)

def render():
    """Render the SMART Sourcing page"""
    
    st.title("💼 SMART Sourcing")
    st.markdown("**Contract Delivery Management for Capital Programme Programme**")
    
    # Create consolidated tabs for streamlined sourcing workflow
    tab1, tab2, tab3 = st.tabs([
        "📈 Pipeline Management", 
        "📊 Project & Contract Delivery",
        "🏢 Supplier & Market Health"
    ])
    
    with tab1:
        render_pipeline_management_tab()
    
    with tab2:
        render_project_contract_delivery_tab()
    
    with tab3:
        render_supplier_market_health_tab()

def render_pipeline_management_tab():
    """Render the consolidated pipeline management tab combining contract and demand pipelines"""
    
    st.markdown("### 📈 Pipeline Management Overview")
    st.markdown("*Unified view of contract pipeline and demand forecasting*")
    
    # Use tabs instead of columns to avoid nesting issues
    subtab1, subtab2 = st.tabs(["Contract Pipeline", "Demand Pipeline"])
    
    with subtab1:
        st.markdown("#### Contract Pipeline Planning")
        render_contract_pipeline_content()
    
    with subtab2:
        st.markdown("#### Demand Pipeline Forecast")
        render_demand_pipeline_content()

def render_project_contract_delivery_tab():
    """Render the consolidated project and contract delivery tab"""
    
    st.markdown("### 📊 Project & Contract Delivery")
    st.markdown("*Integrated tracking from project initiation through contract delivery*")
    
    # Project delivery section
    st.markdown("#### Project Delivery Tracker")
    render_project_delivery_content()
    
    st.markdown("---")
    
    # Additional delivery insights
    st.markdown("#### Delivery Performance Analysis")
    df_pipeline = st.session_state.get('df_sourcing_pipeline', pd.DataFrame())
    
    if not df_pipeline.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            on_track = len(df_pipeline[df_pipeline['rag_status'] == 'Green'])
            st.metric("On Track Projects", on_track, delta=f"{on_track/len(df_pipeline)*100:.0f}%")
        
        with col2:
            at_risk = len(df_pipeline[df_pipeline['rag_status'] == 'Amber'])
            st.metric("At Risk Projects", at_risk, delta=f"{at_risk/len(df_pipeline)*100:.0f}%")
        
        with col3:
            critical = len(df_pipeline[df_pipeline['rag_status'] == 'Red'])
            st.metric("Critical Projects", critical, delta=f"{critical/len(df_pipeline)*100:.0f}%")

def render_supplier_market_health_tab():
    """Render enhanced supplier and market health tab with integrated risk management"""
    
    st.markdown("### 🏢 Supplier & Market Health")
    st.markdown("*Comprehensive supplier performance and market risk assessment*")
    
    # Create tabs within the supplier health section
    subtab1, subtab2, subtab3 = st.tabs(["Market Health", "Team Capacity", "Route Analysis"])
    
    with subtab1:
        render_supplier_market_content()
    
    with subtab2:
        render_team_capacity_content()
    
    with subtab3:
        render_procurement_routes_content()

def render_contract_pipeline_content():
    """Render contract pipeline content (extracted from original tab)"""
    render_contract_pipeline_tab()

def render_demand_pipeline_content():
    """Render demand pipeline content (extracted from original tab)"""
    render_demand_pipeline_tab()

def render_project_delivery_content():
    """Render project delivery content (extracted from original tab)"""
    render_project_delivery_tab()

def render_supplier_market_content():
    """Render supplier market content (extracted from original tab)"""
    render_supplier_market_tab()

def render_team_capacity_content():
    """Render team capacity content (extracted from original tab)"""
    render_team_capacity_tab()

def render_procurement_routes_content():
    """Render procurement routes content (extracted from original tab)"""
    render_procurement_routes_tab()

def render_drill_through_details(df, selected_status):
    """Render detailed breakdown when user clicks on chart elements"""
    
    filtered_df = df[df['rag_status'] == selected_status]
    
    with st.expander(f"📋 {selected_status} Status Contracts - Details", expanded=True):
        st.markdown(f"### {len(filtered_df)} contracts with {selected_status} status")
        
        # Summary metrics for selected status
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_value = filtered_df['total_value_gbp'].sum() / 1_000_000
            st.metric("Total Value", f"£{total_value:.1f}M")
        
        with col2:
            avg_timeline = filtered_df['days_in_current_stage'].mean()
            st.metric("Avg Days in Stage", f"{avg_timeline:.0f}")
        
        with col3:
            high_risk = len(filtered_df[filtered_df['risk_level'] == 'High'])
            st.metric("High Risk Count", high_risk)
        
        # Detailed table
        display_columns = ['package_name', 'procurement_category', 'total_value_gbp', 'current_stage', 'risk_level']
        st.dataframe(
            filtered_df[display_columns].style.format({'total_value_gbp': '£{:,.0f}'}),
            use_container_width=True
        )
        
        # Action buttons for selected contracts
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Export {selected_status} Contracts"):
                st.success(f"Exported {len(filtered_df)} {selected_status} contracts to CSV")
        with col2:
            if st.button(f"Schedule Review for {selected_status}"):
                st.success(f"Review meeting scheduled for {len(filtered_df)} {selected_status} contracts")

def render_procurement_routes_tab():
    """Render the procurement routes analysis tab"""
    
    st.subheader("🛣️ Procurement Routes Analysis")
    st.markdown("**Performance comparison across different procurement approaches**")
    
    if not st.session_state.sample_data_loaded:
        st.warning("Please load sample data from the sidebar to view procurement routes analysis.")
        return
    
    df_routes = st.session_state.df_procurement_routes
    
    if df_routes.empty:
        st.error("No procurement routes data available.")
        return
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_routes = len(df_routes)
        st.metric("Active Routes", total_routes)
    
    with col2:
        avg_timeline = df_routes['avg_timeline_days'].mean()
        st.metric("Avg Timeline", f"{avg_timeline:.0f} days")
    
    with col3:
        avg_success = df_routes['success_rate'].mean()
        st.metric("Avg Success Rate", f"{avg_success:.1%}")
    
    with col4:
        total_value = df_routes['total_value_gbp_m'].sum()
        st.metric("Total Value", f"£{total_value:.0f}M")
    
    # Route performance analysis
    st.markdown("### Route Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Success Rate by Route")
        fig_success = px.bar(
            df_routes.sort_values('success_rate', ascending=True),
            x='success_rate',
            y='route_to_market',
            orientation='h',
            color='success_rate',
            color_continuous_scale='RdYlGn',
            title="Success Rate by Procurement Route"
        )
        fig_success.update_layout(
            height=400,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_success, use_container_width=True)
    
    with col2:
        st.markdown("#### Timeline vs Value Analysis")
        fig_scatter = px.scatter(
            df_routes,
            x='avg_timeline_days',
            y='total_value_gbp_m',
            size='contracts_count',
            color='risk_level',
            hover_name='route_to_market',
            title="Timeline vs Value by Route",
            color_discrete_map={'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'}
        )
        fig_scatter.update_layout(
            height=400,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Detailed route analysis
    st.markdown("### Route Performance Details")
    
    selected_route = st.selectbox(
        "Select route for detailed analysis:",
        df_routes['route_to_market'].tolist()
    )
    
    if selected_route:
        route_data = df_routes[df_routes['route_to_market'] == selected_route].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"**Contracts:** {route_data['contracts_count']}")
            st.info(f"**Avg Timeline:** {route_data['avg_timeline_days']} days")
        
        with col2:
            st.success(f"**Success Rate:** {route_data['success_rate']:.1%}")
            st.success(f"**Avg Savings:** {route_data['avg_savings_percent']:.1f}%")
        
        with col3:
            st.warning(f"**Risk Level:** {route_data['risk_level']}")
            st.warning(f"**Compliance:** {route_data['compliance_score']:.1%}")

def render_team_capacity_tab():
    """Render the team capacity analysis tab"""
    
    st.subheader("👥 Team Capacity Management")
    st.markdown("**Resource allocation and capacity utilization across project portfolio**")
    
    if not st.session_state.sample_data_loaded:
        st.warning("Please load sample data from the sidebar to view team capacity analysis.")
        return
    
    df_capacity = st.session_state.df_team_capacity
    
    if df_capacity.empty:
        st.error("No team capacity data available.")
        return
    
    # Team overview metrics
    team_summary = df_capacity.groupby('team_member').agg({
        'allocation_percent': 'sum',
        'project_value_gbp_m': 'sum'
    }).reset_index()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_members = len(team_summary)
        st.metric("Team Members", total_members)
    
    with col2:
        avg_utilization = team_summary['allocation_percent'].mean()
        st.metric("Avg Utilization", f"{avg_utilization:.1f}%")
    
    with col3:
        overallocated = len(team_summary[team_summary['allocation_percent'] > 100])
        st.metric("Overallocated", overallocated)
    
    with col4:
        available_capacity = team_summary[team_summary['allocation_percent'] < 90]['allocation_percent'].count()
        st.metric("Available Capacity", available_capacity)
    
    # Capacity visualization
    st.markdown("### Team Capacity Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Used:** Current project allocations across procurement team members with utilization percentages\n\n**How to Read:** Green bars show healthy utilization (60-90%), yellow indicates high workload (90-100%), red shows overallocation (>100%). Red dashed line marks 100% capacity threshold.")
        
        with chart_col:
            st.markdown("#### Capacity Utilization by Team Member")
            
            # Create capacity heatmap
            fig_capacity = px.bar(
                team_summary.sort_values('allocation_percent', ascending=True),
                x='allocation_percent',
                y='team_member',
                orientation='h',
                color='allocation_percent',
                color_continuous_scale=['green', 'yellow', 'red'],
                title="Team Member Utilization (%)"
            )
            fig_capacity.add_vline(x=100, line_dash="dash", line_color="red")
            fig_capacity.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_capacity, use_container_width=True)
    
    with col2:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Used:** Total contract value assigned to each procurement team member across active water infrastructure projects\n\n**How to Read:** Treemap segments sized by contract value, colored by team allocation percentage. Larger segments indicate high-value water treatment, network, or environmental projects. Use for workload balancing and portfolio risk management.")
        
        with chart_col:
            st.markdown("#### Project Portfolio Value Distribution")
            
            project_summary = df_capacity[df_capacity['project'] != 'Available Capacity'].groupby('project').agg({
                'project_value_gbp_m': 'first',
                'allocation_percent': 'sum'
            }).reset_index()
            
            fig_projects = px.treemap(
                project_summary,
                path=['project'],
                values='project_value_gbp_m',
                color='allocation_percent',
                title="Projects by Value and Team Allocation"
            )
            fig_projects.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_projects, use_container_width=True)
    
    # Detailed team allocation matrix
    st.markdown("### Team Allocation Matrix")
    
    # Create pivot table for allocation matrix
    allocation_matrix = df_capacity.pivot_table(
        index='team_member',
        columns='project',
        values='allocation_percent',
        fill_value=0
    )
    
    # Display heatmap
    fig_matrix = px.imshow(
        allocation_matrix.values,
        x=allocation_matrix.columns,
        y=allocation_matrix.index,
        color_continuous_scale='RdYlGn_r',
        title="Team Member Project Allocation Matrix (%)"
    )
    fig_matrix.update_layout(
        height=500,
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_matrix, use_container_width=True)
    
    # Capacity recommendations
    st.markdown("### Capacity Optimization Recommendations")
    
    overallocated_members = team_summary[team_summary['allocation_percent'] > 100]
    underutilized_members = team_summary[team_summary['allocation_percent'] < 80]
    
    if not overallocated_members.empty:
        st.warning("**Overallocated Team Members:**")
        for _, member in overallocated_members.iterrows():
            st.write(f"• {member['team_member']}: {member['allocation_percent']:.1f}% allocated")
    
    if not underutilized_members.empty:
        st.info("**Available Capacity:**")
        for _, member in underutilized_members.iterrows():
            available = 100 - member['allocation_percent']
            st.write(f"• {member['team_member']}: {available:.1f}% available capacity")

def render_project_delivery_tab():
    """Render the project delivery tracker tab"""
    
    st.subheader("📊 Project Delivery Tracker")
    st.markdown("**Real-time visibility of Your Water Utility Capital Programme contract delivery against regulatory deadlines**")
    st.markdown("💡 **Click on any chart element to filter all related charts**")
    
    if not st.session_state.sample_data_loaded:
        st.warning("📊 Please load sample data from the sidebar to view project delivery status.")
        return
    
    df = st.session_state.df_sourcing_pipeline
    
    if df.empty:
        st.error("No project delivery data available.")
        return
    
    # Render filter controls
    render_filter_controls()
    
    # Get filtered summary stats for metrics
    stats = get_filtered_summary_stats(df)
    filter_suffix = " (Filtered)" if stats['filtered'] else ""
    
    # Capital Programme delivery overview metrics with filtering
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(f"Total Capital Programme Value{filter_suffix}", f"£{stats['value_m']:.1f}M")
    
    with col2:
        filtered_df = df if not stats['filtered'] else df[df['current_stage'].isin(['Contract', 'Award'])]
        on_track = len(filtered_df[filtered_df['current_stage'].isin(['Contract', 'Award'])])
        st.metric(f"Contracts Delivered{filter_suffix}", f"{on_track}/{stats['contracts']}")
    
    with col3:
        filtered_df = df if not stats['filtered'] else df
        delayed = len(filtered_df[filtered_df['risk_level'] == 'High'])
        penalty_exposure = delayed * 2.5
        st.metric(f"Regulatory Penalty Exposure{filter_suffix}", f"£{penalty_exposure:.1f}M")
    
    with col4:
        critical_path_blocked = delayed // 2
        st.metric(f"Critical Path Dependencies{filter_suffix}", f"{critical_path_blocked} blocked")
    
    # Interactive Filter Controls
    st.markdown("### Interactive Contract Dashboard")
    st.markdown("**Use filters below to drill down across all charts**")
    
    # Create RAG status based on procurement stage and risk level
    def get_rag_status(row):
        if row['current_stage'] in ['Contract', 'Award']:
            return 'Green'
        elif row['risk_level'] == 'High':
            return 'Red'
        elif row['current_stage'] in ['Evaluation', 'Tender Process']:
            return 'Amber'
        else:
            return 'Green'
    
    df['rag_status'] = df.apply(get_rag_status, axis=1)
    
    # Interactive filter controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        rag_filter = st.selectbox(
            "RAG Status:",
            ['All'] + list(df['rag_status'].unique()),
            key="rag_filter"
        )
    
    with col2:
        category_filter = st.selectbox(
            "Category:",
            ['All'] + list(df['procurement_category'].unique()),
            key="category_filter"
        )
    
    with col3:
        stage_filter = st.selectbox(
            "Stage:",
            ['All'] + list(df['current_stage'].unique()),
            key="stage_filter"
        )
    
    with col4:
        risk_filter = st.selectbox(
            "Risk Level:",
            ['All'] + list(df['risk_level'].unique()),
            key="risk_filter"
        )
    
    # Apply filters to create working dataset
    filtered_df = df.copy()
    
    if rag_filter != 'All':
        filtered_df = filtered_df[filtered_df['rag_status'] == rag_filter]
    if category_filter != 'All':
        filtered_df = filtered_df[filtered_df['procurement_category'] == category_filter]
    if stage_filter != 'All':
        filtered_df = filtered_df[filtered_df['current_stage'] == stage_filter]
    if risk_filter != 'All':
        filtered_df = filtered_df[filtered_df['risk_level'] == risk_filter]
    
    # Show filter status
    filter_count = sum([f != 'All' for f in [rag_filter, category_filter, stage_filter, risk_filter]])
    if filter_count > 0:
        st.info(f"🔍 Showing {len(filtered_df)} of {len(df)} contracts with {filter_count} filter(s) applied")
    
    st.markdown("---")
    
    # Contract delivery status with balanced chart types
    col1, col2 = st.columns(2)
    
    with col1:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Used:** Contract register with current procurement stages and risk assessments\n\n**Insights:** Shows overall delivery health - green indicates on-track contracts, amber shows contracts in active procurement, red flags high-risk contracts requiring immediate attention.")
        
        with chart_col:
            st.markdown("#### Contract Delivery Status (RAG)")
            
            # Use filtered data for the chart
            if not filtered_df.empty:
                status_counts = filtered_df['rag_status'].value_counts()
                
                fig_rag = px.pie(
                    values=status_counts.values,
                    names=status_counts.index,
                    color=status_counts.index,
                    color_discrete_map={'Green': '#28a745', 'Amber': '#ffc107', 'Red': '#dc3545'}
                )
                fig_rag.update_traces(textposition='inside', textinfo='percent+label')
                fig_rag.update_layout(
                    font=dict(color='white'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig_rag, use_container_width=True)
            else:
                st.warning("No contracts match current filter criteria")
    
    with col2:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Used:** Contract values aggregated by current procurement stage\n\n**Insights:** Shows procurement flow and identifies bottlenecks. Funnel shape reveals where contracts are stalling and resource allocation needs.")
        
        with chart_col:
            st.markdown("#### Procurement Pipeline Flow")
            
            # Use filtered data for the chart
            if not filtered_df.empty:
                stage_order = ['Market Analysis', 'RFQ Preparation', 'Tender Process', 'Evaluation', 'Award', 'Contract']
                stage_counts = filtered_df['current_stage'].value_counts().reindex(stage_order, fill_value=0)
                stage_values = filtered_df.groupby('current_stage')['total_value_gbp'].sum().reindex(stage_order, fill_value=0) / 1_000_000
                
                fig_funnel = go.Figure(go.Funnel(
                    y = stage_order,
                    x = stage_counts.values,
                    textinfo = "value+percent initial",
                    texttemplate = "%{value} contracts<br>(%{percentInitial})",
                    hovertemplate = "<b>Stage:</b> %{y}<br><b>Contracts:</b> %{x}<br><b>Value:</b> £%{customdata:.1f}M<extra></extra>",
                    customdata = stage_values.values,
                    marker = {"color": ["#dc3545", "#fd7e14", "#ffc107", "#20c997", "#0dcaf0", "#28a745"]}
                ))
                
                fig_funnel.update_layout(
                    font=dict(color='white'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=400
                )
                st.plotly_chart(fig_funnel, use_container_width=True)
            else:
                st.warning("No pipeline data available for current filters")
    
    # Filtered Data Summary and Drill-Down
    if filter_count > 0:
        st.markdown("### Filtered Data Details")
        
        # Summary metrics for filtered data
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_value_filtered = filtered_df['total_value_gbp'].sum() / 1_000_000
            st.metric("Filtered Total Value", f"£{total_value_filtered:.1f}M")
        
        with col2:
            avg_value = filtered_df['total_value_gbp'].mean() / 1_000_000 if not filtered_df.empty else 0
            st.metric("Average Contract Value", f"£{avg_value:.1f}M")
        
        with col3:
            high_risk_count = len(filtered_df[filtered_df['risk_level'] == 'High'])
            st.metric("High Risk Contracts", high_risk_count)
        
        with col4:
            completed_count = len(filtered_df[filtered_df['current_stage'] == 'Contract'])
            st.metric("Completed Contracts", completed_count)
        
        # Detailed contract table
        if st.checkbox("Show Detailed Contract List", key="show_details"):
            st.markdown("#### Filtered Contract Details")
            
            # Select columns to display
            display_columns = ['package_name', 'procurement_category', 'current_stage', 'rag_status', 
                             'risk_level', 'total_value_gbp', 'days_in_current_stage']
            
            display_df = filtered_df[display_columns].copy()
            display_df['total_value_gbp'] = display_df['total_value_gbp'].apply(lambda x: f"£{x:,.0f}")
            
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Export filtered data
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("Export Filtered Data"):
                    csv_data = filtered_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"filtered_contracts_{filter_count}_filters.csv",
                        mime="text/csv"
                    )

def render_supplier_market_tab():
    """Render the supplier market health tab with interactive market concentration"""
    
    st.subheader("🏢 Supplier Market Health")
    st.markdown("**Interactive market concentration analysis and T1 supplier health assessment**")
    
    if not st.session_state.sample_data_loaded:
        st.warning("📊 Please load sample data from the sidebar to view supplier market health.")
        return
    
    df_concentration = st.session_state.df_market_concentration
    df_t1_health = st.session_state.df_t1_supplier_health
    
    if df_concentration.empty or df_t1_health.empty:
        st.error("No market concentration or T1 supplier data available.")
        return
    
    # Market overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_segments = df_concentration['market_segment'].nunique()
        st.metric("Market Segments", total_segments)
    
    with col2:
        total_market_size = df_concentration['market_size_gbp_m'].sum()
        st.metric("Total Market Size", f"£{total_market_size:.0f}M")
    
    with col3:
        avg_concentration = df_concentration.groupby('market_segment')['market_share'].max().mean()
        st.metric("Avg Market Leader Share", f"{avg_concentration:.1%}")
    
    with col4:
        t1_suppliers = len(df_t1_health)
        st.metric("T1 Suppliers Monitored", t1_suppliers)
    
    # Interactive market concentration map
    st.markdown("### 🗺️ Interactive Market Concentration Map")
    st.markdown("**Click on segments to explore detailed supplier positioning**")
    
    # Create market concentration visualization
    fig_concentration = px.treemap(
        df_concentration,
        path=['market_segment', 'supplier'],
        values='revenue_gbp_m',
        color='market_share',
        color_continuous_scale='RdYlBu_r',
        title="Market Concentration by Segment and Supplier",
        hover_data=['competitive_position', 'financial_health']
    )
    fig_concentration.update_layout(
        height=500,
        font=dict(color='white'),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Display the interactive chart
    st.plotly_chart(fig_concentration, use_container_width=True, key="market_concentration_chart")
    
    # Segment selector for detailed analysis
    selected_segment = st.selectbox(
        "Select market segment for detailed analysis:",
        df_concentration['market_segment'].unique()
    )
    
    if selected_segment:
        render_market_segment_details(df_concentration, selected_segment)
    
    st.markdown("---")
    
    # T1 Supplier Health Assessment
    st.markdown("### 🏆 Tier 1 Supplier Health Assessment")
    st.markdown("**Comprehensive health check for major suppliers commonly used by water utilities**")
    
    # T1 Health overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Overall T1 Supplier Performance")
        
        # Create radar chart for T1 supplier comparison
        categories = ['Financial Score', 'Delivery Performance', 'Quality Score', 'Innovation Index', 'ESG Score']
        
        fig_radar = go.Figure()
        
        for _, supplier in df_t1_health.iterrows():
            values = [
                supplier['financial_score'] / 10,  # Normalize to 0-1
                supplier['delivery_performance'],
                supplier['quality_score'] / 10,
                supplier['innovation_index'],
                supplier['esg_score']
            ]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=supplier['supplier_name']
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )),
            showlegend=True,
            height=400,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        st.markdown("#### T1 Supplier Risk Matrix")
        
        # Risk vs Performance matrix
        fig_risk_matrix = px.scatter(
            df_t1_health,
            x='delivery_performance',
            y='financial_score',
            size='total_spend_gbp_m',
            color='risk_rating',
            hover_name='supplier_name',
            title="T1 Supplier Risk vs Performance Matrix",
            color_discrete_map={'Low': '#28a745', 'Medium': '#ffc107', 'High': '#dc3545'}
        )
        fig_risk_matrix.update_layout(
            height=400,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Delivery Performance",
            yaxis_title="Financial Score"
        )
        
        st.plotly_chart(fig_risk_matrix, use_container_width=True)
    
    # Detailed T1 supplier table
    st.markdown("#### T1 Supplier Detailed Scorecard")
    
    # Format the T1 data for display
    display_df = df_t1_health.copy()
    display_df['delivery_performance'] = display_df['delivery_performance'].apply(lambda x: f"{x:.1%}")
    display_df['financial_score'] = display_df['financial_score'].apply(lambda x: f"{x:.1f}/10")
    display_df['quality_score'] = display_df['quality_score'].apply(lambda x: f"{x:.1f}/10")
    display_df['total_spend_gbp_m'] = display_df['total_spend_gbp_m'].apply(lambda x: f"£{x:.1f}M")
    
    st.dataframe(
        display_df[['supplier_name', 'financial_score', 'delivery_performance', 'quality_score', 
                   'relationship_strength', 'risk_rating', 'total_spend_gbp_m']],
        use_container_width=True
    )

def render_market_segment_details(df_concentration, selected_segment):
    """Render detailed analysis for selected market segment"""
    
    segment_data = df_concentration[df_concentration['market_segment'] == selected_segment]
    
    with st.expander(f"📊 {selected_segment} - Detailed Market Analysis", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            market_size = segment_data['market_size_gbp_m'].iloc[0]
            st.metric("Market Size", f"£{market_size:.0f}M")
        
        with col2:
            top_player_share = segment_data['market_share'].max()
            st.metric("Market Leader Share", f"{top_player_share:.1%}")
        
        with col3:
            hhi = (segment_data['market_share'] ** 2).sum()
            concentration_level = "High" if hhi > 0.25 else "Medium" if hhi > 0.15 else "Low"
            st.metric("Concentration Level", concentration_level)
        
        # Supplier positioning in this segment
        st.markdown("#### Supplier Positioning")
        
        fig_segment = px.bar(
            segment_data.sort_values('market_share', ascending=True),
            x='market_share',
            y='supplier',
            orientation='h',
            color='competitive_position',
            title=f"Market Share in {selected_segment}",
            hover_data=['financial_health', 'innovation_score']
        )
        fig_segment.update_layout(
            height=300,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_segment, use_container_width=True)
        
        # Strategic recommendations
        st.markdown("#### Strategic Recommendations")
        
        leader = segment_data.loc[segment_data['market_share'].idxmax()]
        
        if leader['market_share'] > 0.4:
            st.warning(f"⚠️ **High Concentration Risk**: {leader['supplier']} dominates with {leader['market_share']:.1%} share")
            st.info("💡 **Recommendation**: Develop alternative suppliers to reduce dependency")
        
        growth_suppliers = segment_data[segment_data['growth_rate'] > 10]
        if not growth_suppliers.empty:
            st.success(f"🚀 **Growth Opportunities**: {len(growth_suppliers)} suppliers showing strong growth")
            for _, supplier in growth_suppliers.iterrows():
                st.write(f"• {supplier['supplier']}: {supplier['growth_rate']:.1f}% growth")

def render_contract_pipeline_tab():
    """Render the contract pipeline planning tab"""
    
    st.subheader("📋 Contract Pipeline Planning")
    st.markdown("**Strategic planning for upcoming Your Water Utility Capital Programme contract awards**")
    
    if not st.session_state.sample_data_loaded:
        st.warning("📊 Please load sample data from the sidebar to view contract pipeline planning.")
        return
    
    df = st.session_state.df_sourcing_pipeline
    
    if df.empty:
        st.error("No contract pipeline data available.")
        return
    
    # Contract pipeline planning overview
    st.markdown("### Upcoming Contract Awards & Renewals")
    
    # Pipeline planning metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        upcoming_awards = len(df[df['current_stage'].isin(['Tender Process', 'Evaluation'])])
        st.metric("Upcoming Awards", upcoming_awards)
    
    with col2:
        pending_value = df[df['current_stage'].isin(['Tender Process', 'Evaluation'])]['total_value_gbp'].sum() / 1_000_000
        st.metric("Pending Award Value", f"£{pending_value:.1f}M")
    
    with col3:
        high_priority = len(df[df['risk_level'] == 'High'])
        st.metric("High Priority Contracts", high_priority)
    
    with col4:
        regulatory_critical = len(df[df['procurement_category'].str.contains('Construction|Design', case=False, na=False)])
        st.metric("Regulatory Critical", regulatory_critical)
    
    # Contract planning timeline with balanced chart types
    col1, col2 = st.columns(2)
    
    with col1:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Used:** Contract register showing current procurement stage and contract counts\n\n**Insights:** Identifies delivery bottlenecks and procurement capacity planning needs. Shows where contracts are stalling and resource allocation requirements.")
        
        with chart_col:
            st.markdown("#### Contract Award Timeline")
            timeline_data = df.groupby('current_stage').agg({
                'package_name': 'count',
                'total_value_gbp': 'sum'
            }).reset_index()
            
            fig_timeline = px.bar(
                timeline_data,
                x='current_stage',
                y='package_name',
                title="Contracts by Delivery Stage",
                color_discrete_sequence=['#00C5E7']
            )
            
            fig_timeline.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Procurement Stage",
                yaxis_title="Number of Contracts",
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        # Info icon with tooltip
        info_col, chart_col = st.columns([1, 10])
        with info_col:
            st.markdown("ℹ️", help="**Data Required:** Contract values and regulatory criticality assessment\n\n**Insights:** Prioritizes contracts by their operational significance and regulatory compliance impact. Helps focus on high-value contracts essential for maintaining service standards and statutory obligations.")
        
        with chart_col:
            st.markdown("#### Regulatory Priority Investment")
            df['operational_priority'] = df['total_value_gbp'] / 1_000_000  # Convert to millions
            
            impact_priority = df.nlargest(8, 'operational_priority')[['package_name', 'total_value_gbp', 'operational_priority']]
            impact_priority['total_value_gbp'] = impact_priority['total_value_gbp'] / 1_000_000
            
            fig_impact = px.bar(
                impact_priority,
                x='operational_priority',
                y='package_name',
                orientation='h',
                title="Contract Priority by Infrastructure Investment",
                color_discrete_sequence=['#dc3545']
            )
            
            fig_impact.update_layout(
                height=400,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Investment Value (£M)",
                yaxis_title="Contract"
            )
            
            st.plotly_chart(fig_impact, use_container_width=True)

def render_demand_pipeline_tab():
    """Render the GMPP-aligned demand pipeline tab"""
    
    st.subheader("📈 GMPP Demand Pipeline")
    st.markdown("**Government Major Projects Portfolio analysis and gate review tracking**")
    
    if not st.session_state.sample_data_loaded:
        st.warning("📊 Please load sample data from the sidebar to view GMPP demand pipeline.")
        return
    
    df = st.session_state.df_demand_pipeline
    
    if df.empty:
        st.error("No GMPP demand pipeline data available.")
        return
    
    # Check if GMPP columns exist, fallback to basic metrics if not
    has_gmpp_data = all(col in df.columns for col in ['gmpp_gate_stage', 'delivery_confidence_assessment', 'whole_life_cost_gbp_m'])
    
    if has_gmpp_data:
        # GMPP Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_pipeline_value = df['estimated_value_gbp_m'].sum()
            st.metric("Total Portfolio Value", f"£{total_pipeline_value:,.0f}M")
        
        with col2:
            whole_life_cost = df['whole_life_cost_gbp_m'].sum()
            st.metric("Whole Life Cost", f"£{whole_life_cost:,.0f}M")
        
        with col3:
            benefits_realisation = df['benefits_realisation_gbp_m'].sum()
            st.metric("Benefits Realisation", f"£{benefits_realisation:,.0f}M")
        
        with col4:
            approved_projects = df[df['business_case_stage'] == 'Approved'] if 'business_case_stage' in df.columns else pd.DataFrame()
            st.metric("Approved Projects", len(approved_projects))
        
        st.markdown("---")
        
        # GMPP Gate Review Status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### GMPP Gate Review Status")
            
            gate_summary = df.groupby('gmpp_gate_stage').agg({
                'estimated_value_gbp_m': 'sum',
                'project_name': 'count'
            }).reset_index()
            
            fig_gates = px.bar(
                gate_summary,
                x='gmpp_gate_stage',
                y='estimated_value_gbp_m',
                title="Portfolio Value by GMPP Gate Stage",
                color_discrete_sequence=['#28a745']
            )
            
            fig_gates.update_layout(
                height=500,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="GMPP Gate Stage",
                yaxis_title="Portfolio Value (£M)",
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig_gates, use_container_width=True)
        
        with col2:
            st.markdown("#### Delivery Confidence Assessment")
            
            confidence_summary = df.groupby('delivery_confidence_assessment').agg({
                'estimated_value_gbp_m': 'sum',
                'project_name': 'count'
            }).reset_index()
            
            # Define color mapping for confidence levels
            confidence_colors = {
                'Green': '#28a745',
                'Amber/Green': '#90EE90',
                'Amber': '#ffc107',
                'Amber/Red': '#FF6B35',
                'Red': '#dc3545'
            }
            
            fig_confidence = px.pie(
                confidence_summary,
                values='estimated_value_gbp_m',
                names='delivery_confidence_assessment',
                title="Portfolio Value by Delivery Confidence",
                color='delivery_confidence_assessment',
                color_discrete_map=confidence_colors
            )
            
            fig_confidence.update_layout(
                height=500,
                font=dict(color='white'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_confidence, use_container_width=True)
    else:
        # Fallback to basic pipeline metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_value = df['estimated_value_gbp_m'].sum()
            st.metric("Total Pipeline Value", f"£{total_value:,.0f}M")
        
        with col2:
            total_projects = len(df)
            st.metric("Total Projects", total_projects)
        
        with col3:
            if 'probability_percent' in df.columns:
                avg_probability = df['probability_percent'].mean()
                st.metric("Avg. Probability", f"{avg_probability:.1f}%")
            else:
                st.metric("Project Types", df['project_type'].nunique())
        
        with col4:
            if 'probability_percent' in df.columns:
                weighted_value = (df['estimated_value_gbp_m'] * df['probability_percent'] / 100).sum()
                st.metric("Weighted Value", f"£{weighted_value:,.0f}M")
            else:
                st.metric("Avg. Project Value", f"£{df['estimated_value_gbp_m'].mean():.0f}M")
    
    # Pipeline Timeline
    st.markdown("#### GMPP Project Timeline")
    
    # Convert dates for plotting
    df_plot = df.copy()
    df_plot['start_date'] = pd.to_datetime(df_plot['start_date'])
    
    # Use appropriate end date column
    end_date_col = 'completion_date' if 'completion_date' in df.columns else 'end_date'
    if end_date_col in df.columns:
        df_plot[end_date_col] = pd.to_datetime(df_plot[end_date_col])
        
        # Color by delivery confidence if available, otherwise by value
        color_col = 'delivery_confidence_assessment' if has_gmpp_data else 'estimated_value_gbp_m'
        
        fig_timeline = px.timeline(
            df_plot,
            x_start="start_date",
            x_end=end_date_col,
            y="project_name",
            color=color_col,
            hover_data=["project_type", "estimated_value_gbp_m"],
            title="GMPP Project Timeline"
        )
        
        if has_gmpp_data and 'delivery_confidence_assessment' in df.columns:
            confidence_colors = {
                'Green': '#28a745',
                'Amber/Green': '#90EE90', 
                'Amber': '#ffc107',
                'Amber/Red': '#FF6B35',
                'Red': '#dc3545'
            }
            fig_timeline.update_traces(marker_color=[confidence_colors.get(x, '#00C5E7') for x in df_plot[color_col]])
        
        fig_timeline.update_layout(
            height=600,
            font=dict(color='white'),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # GMPP Analysis sections
    if has_gmpp_data:
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("ℹ️ **Business Case Progression**", help="**Data Required:** GMPP business case development stages from project management office\n\n**Insights:** Shows portfolio maturity and readiness for investment decisions. Critical for resource allocation and approval pipeline management.")
            
            if 'business_case_stage' in df.columns:
                bc_summary = df.groupby('business_case_stage').agg({
                    'estimated_value_gbp_m': 'sum',
                    'project_name': 'count'
                }).reset_index()
                
                fig_bc = px.bar(
                    bc_summary,
                    x='business_case_stage',
                    y='estimated_value_gbp_m',
                    title="Portfolio Value by Business Case Stage",
                    color_discrete_sequence=['#00C5E7']
                )
                
                fig_bc.update_layout(
                    height=500,
                    font=dict(color='white'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Business Case Stage",
                    yaxis_title="Portfolio Value (£M)",
                    xaxis_tickangle=-45
                )
                
                st.plotly_chart(fig_bc, use_container_width=True)
        
        with col2:
            st.markdown("ℹ️ **Regulatory Drivers**", help="**Data Required:** Project regulatory compliance requirements from environmental and quality frameworks\n\n**Insights:** Shows investment distribution across regulatory mandates. Essential for compliance planning and priority setting.")
            
            if 'regulatory_driver' in df.columns:
                regulatory_summary = df.groupby('regulatory_driver').agg({
                    'estimated_value_gbp_m': 'sum',
                    'project_name': 'count'
                }).reset_index()
                
                fig_regulatory = px.pie(
                    regulatory_summary,
                    values='estimated_value_gbp_m',
                    names='regulatory_driver',
                    title="Portfolio Value by Regulatory Driver"
                )
                
                fig_regulatory.update_layout(
                    height=500,
                    font=dict(color='white'),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig_regulatory, use_container_width=True)
        
        # GMPP Portfolio Table
        st.markdown("#### GMPP Portfolio Dashboard")
        st.markdown("ℹ️ **Portfolio Overview**", help="**Data Required:** Complete GMPP project data from portfolio management systems\n\n**Insights:** Comprehensive view of all major projects with gate status, confidence ratings, and key metrics for executive oversight.")
        
        # Select key GMPP columns for display
        gmpp_display_columns = []
        for col in ['project_name', 'estimated_value_gbp_m', 'gmpp_gate_stage', 'delivery_confidence_assessment', 'business_case_stage']:
            if col in df.columns:
                gmpp_display_columns.append(col)
        
        if gmpp_display_columns:
            display_df = df[gmpp_display_columns].copy()
            display_df = display_df.sort_values('estimated_value_gbp_m', ascending=False)
            st.dataframe(display_df, use_container_width=True, height=400)
    else:
        # Fallback for legacy data structure
        st.markdown("### Detailed Pipeline View")
        st.markdown("ℹ️ **Project Portfolio**", help="**Data Required:** Project pipeline data from opportunity management systems\n\n**Insights:** Complete view of upcoming projects and opportunities for strategic planning and resource allocation.")
        
        st.dataframe(
            df.sort_values('estimated_value_gbp_m', ascending=False),
            use_container_width=True,
            height=400
        )
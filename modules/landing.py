import streamlit as st
import pandas as pd

def render():
    """Render the SMART Acquisition Platform landing page"""
    
    # Hero section
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="font-size: 3.5rem; margin-bottom: 1rem; color: #00C5E7;">
                🏗️ SMART Acquisition Platform
            </h1>
            <h2 style="font-size: 1.8rem; margin-bottom: 2rem; color: #FAFAFA; font-weight: 300;">
                Thames Water AMP8 Procurement Intelligence
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Platform overview and navigation guidance
    st.markdown("""
        ### Platform Overview
        
        Navigate through the comprehensive procurement intelligence modules:
        
        **📊 SMART Performance** - Supplier performance monitoring and risk assessment
        - Supply chain overview with KPI dashboards
        - Interactive supplier network mapping
        - Contract delivery and risk management
        
        **🔍 SMART Markets** - Market intelligence and supplier insights
        - Real-time market scanning and analysis
        - Supplier intelligence monitoring
        - Competitive landscape assessment
        
        **📋 SMART Sourcing** - Procurement pipeline and contract management
        - Project delivery tracking
        - Supplier market health analysis
        - Contract pipeline planning
        
        **⚖️ AMP8 Regulatory** - Regulatory compliance and performance commitments
        - ODI financial impact tracking
        - Performance commitments monitoring
        - Business plan variance analysis
        
        ---
        
        **Getting Started:** Load Thames Water AMP8 data from the sidebar to explore authentic procurement scenarios.
    """)
    
    st.markdown("---")

def render_executive_kpi_overview():
    """Render executive KPI overview with key metrics from all modules"""
    
    st.markdown("### 📊 Executive Dashboard Overview")
    st.markdown("*Key performance indicators across all acquisition activities*")
    
    # Get data from session state
    df_pipeline = st.session_state.get('df_sourcing_pipeline', pd.DataFrame())
    df_concentration = st.session_state.get('df_market_concentration', pd.DataFrame())
    df_t1_health = st.session_state.get('df_t1_supplier_health', pd.DataFrame())
    
    # Executive metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if not df_pipeline.empty and 'rag_status' in df_pipeline.columns:
            total_projects = len(df_pipeline)
            on_track = len(df_pipeline[df_pipeline['rag_status'] == 'Green'])
            st.metric("Total Projects", total_projects, delta=f"{on_track} on track")
        else:
            st.metric("Total Projects", "0")
    
    with col2:
        if not df_pipeline.empty and 'contract_value_gbp_m' in df_pipeline.columns:
            total_value = df_pipeline['contract_value_gbp_m'].sum()
            st.metric("Total Programme Value", f"£{total_value:.0f}M")
        else:
            st.metric("Total Programme Value", "£0M")
    
    with col3:
        if not df_concentration.empty and 'market_segment' in df_concentration.columns:
            market_segments = df_concentration['market_segment'].nunique()
            st.metric("Market Segments", market_segments)
        else:
            st.metric("Market Segments", "0")
    
    with col4:
        if not df_t1_health.empty and 'financial_health' in df_t1_health.columns:
            healthy_suppliers = len(df_t1_health[df_t1_health['financial_health'] == 'Strong'])
            total_suppliers = len(df_t1_health)
            st.metric("Healthy T1 Suppliers", f"{healthy_suppliers}/{total_suppliers}")
        else:
            st.metric("Healthy T1 Suppliers", "0/0")
    
    # Health status indicators
    st.markdown("#### Programme Health Status")
    
    if not df_pipeline.empty and 'rag_status' in df_pipeline.columns:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            green_count = len(df_pipeline[df_pipeline['rag_status'] == 'Green'])
            green_pct = (green_count / len(df_pipeline)) * 100
            st.metric("On Track", f"{green_count} projects", delta=f"{green_pct:.0f}%")
        
        with col2:
            amber_count = len(df_pipeline[df_pipeline['rag_status'] == 'Amber'])
            amber_pct = (amber_count / len(df_pipeline)) * 100
            st.metric("At Risk", f"{amber_count} projects", delta=f"{amber_pct:.0f}%")
        
        with col3:
            red_count = len(df_pipeline[df_pipeline['rag_status'] == 'Red'])
            red_pct = (red_count / len(df_pipeline)) * 100
            st.metric("Critical", f"{red_count} projects", delta=f"{red_pct:.0f}%")

    st.markdown("---")
    
    # Three pillars
    st.markdown("### 🔺 The Smart Acquisition Framework")
    
    # Create three columns for the pillars
    pillar_col1, pillar_col2, pillar_col3 = st.columns(3)
    
    with pillar_col1:
        st.markdown("""
        #### 💼 SMART Sourcing
        **Contract Delivery Management**
        
        - Project delivery tracking
        - Supplier market health
        - Contract pipeline planning
        - Compliance deadline monitoring
        - Budget variance tracking
        """)
    
    with pillar_col2:
        st.markdown("""
        #### 🚀 SMART Performance
        **Operational Excellence**
        
        - Contract delivery status
        - Delivery risk oversight
        - Customer impact tracking
        - Supplier performance monitoring
        - Service improvement delivery
        """)
    
    with pillar_col3:
        st.markdown("""
        #### 📈 SMART Markets
        **Strategic Market Intelligence**
        
        - Water industry market scanning
        - Regulatory change monitoring
        - Competitive intelligence
        - Innovation trend analysis
        - Market capacity assessment
        """)
    
    st.markdown("---")
    
    # Key features
    st.markdown("### ✨ Key Features")
    
    feature_col1, feature_col2 = st.columns(2)
    
    with feature_col1:
        st.markdown("""
        **🔗 Integrated Intelligence**
        - Pin insights from market scanning
        - Reference external data in procurement decisions
        - Cross-module data sharing
        - Contextual analysis triggers
        
        **🤖 AI-Powered Analytics**
        - OpenAI GPT integration for content analysis
        - Automated market intelligence gathering
        - Sentiment analysis and trend detection
        - Entity extraction and summarization
        """)
    
    with feature_col2:
        st.markdown("""
        **📊 Interactive Dashboards**
        - Real-time data visualization
        - Elegant Plotly charts and graphs
        - Responsive design and layout
        - Professional built-assets styling
        
        **🔧 Configurable Scanning**
        - Industry sub-sector targeting
        - Geographic focus settings
        - Category-specific searches
        - Custom keyword integration
        """)
    
    st.markdown("---")
    
    # Getting started
    st.markdown("### 🚀 Getting Started")
    
    # Status checks
    api_configured = all([
        st.session_state.api_openai_key,
        st.session_state.api_google_key,
        st.session_state.api_google_cx
    ])
    
    data_loaded = st.session_state.sample_data_loaded
    
    setup_col1, setup_col2 = st.columns(2)
    
    with setup_col1:
        st.markdown("#### 1️⃣ API Configuration")
        
        if api_configured:
            st.success("✅ APIs configured via Streamlit Cloud")
            st.markdown("""
            **Ready for Market Intelligence:**
            - OpenAI GPT analysis
            - Google Custom Search
            - Real-time data processing
            """)
        else:
            st.warning("⚠️ API keys required")
            st.markdown("""
            **For Streamlit Cloud deployment:**
            
            Configure API keys in your app settings under "Secrets":
            - `OPENAI_API_KEY`: For content analysis
            - `GOOGLE_API_KEY`: For market search
            - `GOOGLE_CX_ID`: Custom search engine
            
            See sidebar for detailed setup instructions.
            """)
    
    with setup_col2:
        st.markdown("#### 2️⃣ Load Sample Data")
        if data_loaded:
            st.success("✅ Sample data is loaded")
            st.markdown("Explore SMART Sourcing and SMART Performance modules with built assets data.")
        else:
            st.info("📊 Sample data available")
            st.markdown("Load built assets sample data from the sidebar to explore all analytics features.")
    
    st.markdown("---")
    
    # Navigation prompt
    st.markdown("""
    ### 🧭 Ready to Explore?
    
    Use the **SMART Acquisition Navigator** in the sidebar to access the three main modules:
    
    - **📈 SMART Markets**: Start with market intelligence and AI-powered scanning
    - **📊 SMART Sourcing**: Analyze procurement pipelines and team performance  
    - **🚀 SMART Performance**: Monitor supplier KPIs and supply chain risks
    
    Each module is designed to work independently while sharing intelligence 
    through the integrated pinned insights system.
    """)
    
    # Call to action
    if not api_configured or not data_loaded:
        st.markdown("---")
        st.info("💡 **Pro Tip**: Complete the setup steps above to unlock the full potential of the SMART Acquisition platform.")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #888;">
        <small>
            Generic SMART Acquisition for Built Assets v1.0<br>
            Empowering capital programme success through integrated intelligence
        </small>
    </div>
    """, unsafe_allow_html=True)

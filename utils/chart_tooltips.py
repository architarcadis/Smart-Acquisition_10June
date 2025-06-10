"""
Chart tooltip definitions for water infrastructure dashboard
"""

def get_chart_tooltip(chart_type: str, context: str = "") -> str:
    """Get standardized tooltip text for different chart types"""
    
    tooltips = {
        # SMART Sourcing Charts
        "rag_status_pie": {
            "help": "**Data Used:** Current contract delivery status from procurement register with risk assessments\n\n**How to Read:** Green indicates contracts on-track with no delivery concerns, Amber shows contracts with minor risks requiring monitoring, Red flags high-risk contracts needing immediate intervention. Percentages show distribution across portfolio."
        },
        
        "procurement_routes": {
            "help": "**Data Used:** Procurement method selection by contract category from tender management system\n\n**How to Read:** Shows procurement strategy effectiveness across different approaches. Framework agreements provide speed and efficiency, Open tenders maximize competition, Negotiated procedures used for specialized requirements. Helps optimize procurement route selection."
        },
        
        "team_capacity": {
            "help": "**Data Used:** Current project allocations across procurement team members with utilization percentages\n\n**How to Read:** Green bars show healthy utilization (60-90%), yellow indicates high workload (90-100%), red shows overallocation (>100%). Red dashed line marks 100% capacity threshold. Essential for resource planning and workload management."
        },
        
        "supplier_responses": {
            "help": "**Data Used:** Number of supplier responses received per tender by procurement category\n\n**How to Read:** Higher response rates indicate competitive markets with adequate supplier capacity. Low response rates may signal market constraints, barriers to entry, or need for procurement strategy adjustment. Benchmark: 4+ responses for competitive tenders."
        },
        
        "market_concentration": {
            "help": "**Data Used:** Supplier market share and positioning analysis by infrastructure segment\n\n**How to Read:** Larger segments indicate dominant suppliers, colors show market position strength. High concentration (few large suppliers) may indicate supply risk. Use for supplier relationship strategy and market development planning."
        },
        
        "contract_pipeline": {
            "help": "**Data Used:** Forward contract schedule from business planning with estimated values and timelines\n\n**How to Read:** Timeline view of upcoming procurement activity enabling resource planning and market engagement. Peak periods require early planning, gaps may indicate missed opportunities. Critical for procurement capacity management."
        },
        
        # SMART Performance Charts
        "delivery_status": {
            "help": "**Data Used:** Contract milestone tracking and delivery performance from project management systems\n\n**How to Read:** Shows delivery confidence across active contracts. Green indicates on-schedule delivery, Amber shows potential delays, Red flags critical delivery risks. Essential for customer service impact assessment."
        },
        
        "supplier_performance": {
            "help": "**Data Used:** Supplier scorecards covering quality, delivery, cost, and innovation metrics\n\n**How to Read:** Multi-dimensional performance assessment showing supplier strengths and improvement areas. High performers (green) are strategic partners, poor performers (red) require performance improvement plans or contract termination."
        },
        
        "supply_chain_kpi": {
            "help": "**Data Used:** Key performance indicators from supplier management system including delivery, quality, and financial metrics\n\n**How to Read:** Dashboard view of critical supply chain health indicators. Red metrics require immediate attention, amber indicates monitoring needed, green shows good performance. Use for supplier relationship management."
        },
        
        "supply_chain_network": {
            "help": "**Data Used:** Supplier tier structure with spend allocation and risk assessment from vendor management system\n\n**How to Read:** Hierarchical view showing Water Utility at center, Tier 1 main contractors, Tier 2 sub-contractors, and Tier 3 specialists. Size represents spend, colors indicate risk levels. Click segments to drill down through supply chain layers."
        },
        
        "customer_impact": {
            "help": "**Data Used:** Contract delivery status mapped to customer service impact categories\n\n**How to Read:** Shows how procurement and supplier performance translates to customer experience. Infrastructure improvements affect service reliability, digital projects enhance customer experience, quality assurance ensures service standards."
        },
        
        # SMART Markets Charts
        "market_intelligence": {
            "help": "**Data Used:** Market research, supplier intelligence, and competitive analysis from external sources and industry monitoring\n\n**How to Read:** Strategic insights into market trends, supplier capabilities, and competitive landscape. Use for procurement strategy development, supplier selection, and market positioning. High-impact insights require strategic response."
        },
        
        "supplier_intelligence": {
            "help": "**Data Used:** Supplier financial health, capability assessment, and market positioning analysis\n\n**How to Read:** Comprehensive supplier intelligence covering financial stability, technical capabilities, market position, and innovation potential. Critical for supplier selection, relationship management, and supply chain risk assessment."
        },
        
        # AMP8 Regulatory Charts
        "performance_commitments": {
            "help": "**Data Used:** Performance commitment register with actual vs target performance from regulatory team quarterly submissions\n\n**How to Read:** Shows RAG status across all regulatory commitments. Green indicates target achievement, Amber shows performance requiring attention, Red flags penalty risk. Essential for regulatory compliance and financial protection."
        },
        
        "odi_financial": {
            "help": "**Data Used:** Outcome Delivery Incentive calculations based on performance against regulatory targets\n\n**How to Read:** Financial impact of performance delivery showing potential penalties and rewards. Red indicates penalty exposure, green shows reward opportunities. Critical for business plan delivery and financial performance."
        },
        
        "business_plan_variance": {
            "help": "**Data Used:** Actual performance compared to AMP8 business plan commitments and investment levels\n\n**How to Read:** Variance analysis showing delivery against regulatory commitments. Positive variance indicates outperformance, negative shows underdelivery risk. Essential for regulatory relationship management and future price review preparation."
        }
    }
    
    # Return specific tooltip or generic fallback
    key = f"{chart_type}_{context}" if context else chart_type
    return tooltips.get(key, tooltips.get(chart_type, {
        "help": "**Data Used:** Operational data from business systems providing performance insights\n\n**How to Read:** Chart visualization showing key metrics and trends. Use for performance monitoring, trend analysis, and decision support. Contact system administrator for specific data source details."
    }))["help"]

def add_chart_tooltip(chart_title: str, chart_type: str, context: str = ""):
    """Add consistent tooltip to chart with title"""
    import streamlit as st
    
    # Create info icon with tooltip
    info_col, chart_col = st.columns([1, 10])
    with info_col:
        tooltip_text = get_chart_tooltip(chart_type, context)
        st.markdown("ℹ️", help=tooltip_text)
    
    with chart_col:
        st.markdown(f"#### {chart_title}")
        return chart_col

def get_water_infrastructure_context():
    """Get contextual information for water infrastructure charts"""
    return {
        "regulatory_framework": "Ofwat AMP8 regulatory period (2025-2030)",
        "performance_commitments": "15+ regulatory performance commitments",
        "penalty_regime": "Outcome Delivery Incentives with financial penalties/rewards",
        "business_areas": [
            "Water Treatment", "Distribution Network", "Wastewater Treatment", 
            "Customer Services", "Asset Management", "Environmental Compliance"
        ],
        "supplier_ecosystem": "Tier 1 main contractors, Tier 2 sub-contractors, Tier 3 specialists",
        "procurement_value": "£500M+ annual procurement spend across infrastructure and services"
    }
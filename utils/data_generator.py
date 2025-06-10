import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta
import random
from utils.intelligent_data_generator import (
    generate_realistic_procurement_data,
    generate_realistic_supplier_network,
    generate_realistic_performance_commitments,
    generate_realistic_market_intelligence
)

def generate_market_segments_data():
    """Generate sample market segmentation data"""
    segments = [
        'Infrastructure', 'Residential', 'Commercial', 'Industrial', 
        'Healthcare', 'Education', 'Transport', 'Energy', 'Water', 'Digital'
    ]
    
    data = []
    for segment in segments:
        data.append({
            'segment': segment,
            'market_size_gbp_m': random.randint(5000, 50000),
            'growth_rate_percent': round(random.uniform(-2.5, 8.5), 1),
            'competitive_intensity': random.choice(['Low', 'Medium', 'High']),
            'regulatory_impact': random.choice(['Low', 'Medium', 'High']),
            'technology_disruption': random.choice(['Low', 'Medium', 'High']),
            'arcadis_market_share_percent': round(random.uniform(2.0, 15.0), 1)
        })
    
    return pd.DataFrame(data)

def generate_competencies_data():
    """Generate sample core competencies data"""
    competencies = [
        'Project Management', 'Design & Engineering', 'Cost Management',
        'Digital Solutions', 'Sustainability', 'Risk Management',
        'Asset Management', 'Programme Delivery', 'Technical Advisory',
        'Infrastructure Planning'
    ]
    
    data = []
    for comp in competencies:
        data.append({
            'competency': comp,
            'demand_score': random.randint(60, 95),
            'supply_capability': random.randint(55, 90),
            'market_position': random.choice(['Leading', 'Strong', 'Developing']),
            'investment_priority': random.choice(['High', 'Medium', 'Low']),
            'revenue_contribution_percent': round(random.uniform(5.0, 20.0), 1)
        })
    
    return pd.DataFrame(data)

def generate_demand_pipeline_data():
    """Generate GMPP-aligned demand pipeline data with government project methodology"""
    
    # Water infrastructure projects aligned with GMPP categories
    gmpp_project_types = [
        'Water Treatment Works Upgrade', 'Reservoir Construction', 'Network Reinforcement',
        'Flood Defence Scheme', 'Smart Water Grid', 'Leakage Reduction Programme',
        'Water Quality Enhancement', 'Supply Resilience Infrastructure', 'Digital Control Systems',
        'Environmental Compliance Programme'
    ]
    
    # GMPP Gate Review stages (0-5)
    gmpp_gates = [
        'Gate 0 - Strategic Assessment', 'Gate 1 - Business Justification', 
        'Gate 2 - Delivery Strategy', 'Gate 3 - Investment Decision',
        'Gate 4 - Readiness for Service', 'Gate 5 - Operations Review'
    ]
    
    # GMPP Delivery Confidence Assessment ratings
    delivery_confidence = ['Green', 'Amber/Green', 'Amber', 'Amber/Red', 'Red']
    
    # Business case stages per GMPP
    business_case_stages = [
        'Strategic Outline Case', 'Outline Business Case', 'Full Business Case', 'Approved'
    ]
    
    data = []
    start_date = datetime.now()
    
    for i, project_type in enumerate(gmpp_project_types):
        # GMPP projects typically have longer timelines
        project_start = start_date + timedelta(days=random.randint(90, 730))
        project_duration = random.randint(730, 1825)  # 2-5 years typical for major projects
        project_end = project_start + timedelta(days=project_duration)
        
        # GMPP value thresholds (projects >£10M enter GMPP)
        project_value = random.randint(15, 250)  # £15M-£250M for water infrastructure
        
        # Assurance review schedule based on value
        if project_value > 100:
            assurance_reviews = 'Full GMPP Assurance'
        elif project_value > 50:
            assurance_reviews = 'Enhanced Assurance'
        else:
            assurance_reviews = 'Standard Assurance'
        
        data.append({
            'project_name': f"{project_type} - AMP8 Programme",
            'project_type': project_type,
            'gmpp_gate_stage': random.choice(gmpp_gates),
            'business_case_stage': random.choice(business_case_stages),
            'delivery_confidence_assessment': random.choice(delivery_confidence),
            'estimated_value_gbp_m': project_value,
            'whole_life_cost_gbp_m': round(project_value * random.uniform(1.2, 1.8), 1),
            'benefits_realisation_gbp_m': round(project_value * random.uniform(0.8, 2.5), 1),
            'start_date': project_start.strftime('%Y-%m-%d'),
            'completion_date': project_end.strftime('%Y-%m-%d'),
            'sro_department': 'Water Infrastructure Delivery',
            'assurance_review_type': assurance_reviews,
            'next_gate_review_date': (project_start + timedelta(days=random.randint(30, 180))).strftime('%Y-%m-%d'),
            'regulatory_driver': random.choice(['AMP8 Commitment', 'Environmental Regulation', 'Quality Enhancement', 'Resilience Improvement']),
            'spend_to_date_gbp_m': round(project_value * random.uniform(0.0, 0.3), 1),
            'forecast_completion_confidence': random.choice(['High', 'Medium-High', 'Medium', 'Medium-Low', 'Low']),
            'key_risks': random.choice(['Planning Consent', 'Technical Complexity', 'Stakeholder Engagement', 'Regulatory Approval', 'Resource Availability'])
        })
    
    return pd.DataFrame(data)

def generate_sourcing_pipeline_data():
    """Generate realistic water infrastructure procurement pipeline data"""
    return generate_realistic_procurement_data()

def generate_team_performance_data():
    """Generate sample team performance data"""
    teams = ['North Region', 'South Region', 'London', 'Scotland', 'Digital', 'Infrastructure']
    
    data = []
    for team in teams:
        data.append({
            'team': team,
            'procurement_cycle_days_avg': random.randint(45, 120),
            'cost_savings_percent': round(random.uniform(3.5, 12.0), 1),
            'supplier_satisfaction_score': round(random.uniform(7.2, 9.5), 1),
            'compliance_score_percent': random.randint(85, 98),
            'active_suppliers': random.randint(25, 85),
            'contracts_awarded_qtd': random.randint(15, 55),
            'spend_under_management_gbp_m': random.randint(20, 150)
        })
    
    return pd.DataFrame(data)

def generate_supplier_kpis_data():
    """Generate sample supplier KPIs data"""
    suppliers = [
        'Infrastructure Contractor A', 'Engineering Solutions B', 'Construction Group C', 'Design Build Co D',
        'Water Systems E', 'Civil Engineering F', 'Technology Provider G', 'Equipment Supplier H',
        'Consulting Services I', 'Facilities Management J', 'Project Delivery K', 'Innovation Systems L'
    ]
    
    data = []
    for supplier in suppliers:
        data.append({
            'supplier_name': supplier,
            'overall_score': round(random.uniform(6.5, 9.2), 1),
            'quality_score': round(random.uniform(7.0, 9.5), 1),
            'delivery_score': round(random.uniform(6.8, 9.3), 1),
            'cost_performance_score': round(random.uniform(6.2, 8.8), 1),
            'sustainability_score': round(random.uniform(5.5, 9.0), 1),
            'innovation_score': round(random.uniform(5.8, 8.5), 1),
            'contracts_active': random.randint(2, 15),
            'total_spend_gbp_m': round(random.uniform(5.0, 75.0), 1),
            'risk_level': random.choice(['Low', 'Medium', 'High'])
        })
    
    return pd.DataFrame(data)

def generate_sub_tier_map_data():
    """Generate sample sub-tier mapping data"""
    main_contractors = ['Infrastructure Contractor A', 'Engineering Solutions B', 'Construction Group C', 'Design Build Co D']
    sub_contractors = [
        'ABC Electrical', 'XYZ Plumbing', 'Steel Solutions Ltd', 'Concrete Experts',
        'Green Energy Co', 'Safety First Ltd', 'Tech Install Pro', 'Foundation Specialists'
    ]
    
    data = []
    for main in main_contractors:
        # Each main contractor has 3-6 sub-contractors
        num_subs = random.randint(3, 6)
        selected_subs = random.sample(sub_contractors, num_subs)
        
        for sub in selected_subs:
            data.append({
                'main_contractor': main,
                'sub_contractor': sub,
                'relationship_strength': random.choice(['Strong', 'Medium', 'Weak']),
                'contract_value_gbp': random.randint(50000, 2000000),
                'performance_rating': round(random.uniform(6.0, 9.0), 1),
                'risk_exposure': random.choice(['Low', 'Medium', 'High'])
            })
    
    return pd.DataFrame(data)

def generate_supply_chain_risks_data():
    """Generate sample supply chain risks data"""
    risk_categories = [
        'Material Shortages', 'Price Volatility', 'Supplier Financial Health',
        'Geopolitical Disruption', 'Regulatory Changes', 'Cyber Security',
        'Climate Impact', 'Skills Shortage', 'Transport Disruption', 'Quality Issues'
    ]
    
    data = []
    for risk in risk_categories:
        data.append({
            'risk_category': risk,
            'probability': random.choice(['Very Low', 'Low', 'Medium', 'High', 'Very High']),
            'impact': random.choice(['Very Low', 'Low', 'Medium', 'High', 'Very High']),
            'current_mitigation': random.choice(['None', 'Basic', 'Adequate', 'Strong', 'Comprehensive']),
            'affected_suppliers': random.randint(5, 45),
            'estimated_cost_impact_gbp_m': round(random.uniform(0.5, 25.0), 1),
            'timeline_to_impact_days': random.randint(30, 365),
            'mitigation_owner': random.choice(['Procurement', 'Risk', 'Operations', 'Finance'])
        })
    
    return pd.DataFrame(data)

def generate_procurement_routes_data():
    """Generate procurement route to market data"""
    import random
    
    routes = [
        'Framework Agreement', 'Open Competition', 'Direct Award', 
        'Dynamic Purchasing System', 'Innovation Partnership', 'Design & Build',
        'Traditional Tender', 'Competitive Dialogue'
    ]
    
    data = []
    for route in routes:
        contracts_count = random.randint(3, 15)
        avg_timeline = random.randint(45, 180)
        success_rate = random.uniform(0.7, 0.95)
        avg_savings = random.uniform(5, 25)
        
        data.append({
            'route_to_market': route,
            'contracts_count': contracts_count,
            'avg_timeline_days': avg_timeline,
            'success_rate': success_rate,
            'avg_savings_percent': avg_savings,
            'total_value_gbp_m': random.uniform(10, 150),
            'compliance_score': random.uniform(0.8, 1.0),
            'risk_level': random.choice(['Low', 'Medium', 'High'])
        })
    
    return pd.DataFrame(data)

def generate_team_capacity_data():
    """Generate team capacity and project allocation data"""
    import random
    
    team_members = [
        'Senior Procurement Manager A', 'Category Manager B', 'Procurement Specialist C',
        'Contract Manager D', 'Strategic Sourcing Lead E', 'Supplier Relationship Manager F',
        'Commercial Manager G', 'Project Procurement Lead H', 'Risk & Compliance Manager I'
    ]
    
    projects = [
        'Water Treatment Upgrade', 'Network Infrastructure', 'Digital Transformation',
        'Environmental Compliance', 'Asset Modernization', 'Customer Service Enhancement',
        'Operational Efficiency', 'Innovation Program', 'Sustainability Initiative'
    ]
    
    data = []
    for member in team_members:
        allocated_projects = random.sample(projects, random.randint(2, 5))
        total_allocation = 0
        
        for project in allocated_projects:
            allocation = random.uniform(10, 40)
            total_allocation += allocation
            
            data.append({
                'team_member': member,
                'project': project,
                'allocation_percent': allocation,
                'project_value_gbp_m': random.uniform(5, 50),
                'project_stage': random.choice(['Planning', 'Execution', 'Monitoring', 'Closure']),
                'priority': random.choice(['High', 'Medium', 'Low']),
                'skills_match': random.uniform(0.6, 1.0)
            })
        
        # Add unallocated capacity
        if total_allocation < 100:
            data.append({
                'team_member': member,
                'project': 'Available Capacity',
                'allocation_percent': 100 - total_allocation,
                'project_value_gbp_m': 0,
                'project_stage': 'Available',
                'priority': 'Available',
                'skills_match': 1.0
            })
    
    return pd.DataFrame(data)

def generate_market_concentration_data():
    """Generate realistic water infrastructure market concentration data"""
    # Create treemap-compatible format from market intelligence
    market_data = generate_realistic_market_intelligence()
    
    concentration_data = []
    for _, segment in market_data.iterrows():
        # Generate realistic suppliers for each segment
        num_suppliers = random.randint(3, 6)
        supplier_names = [
            'Aqua Solutions Ltd', 'Water Engineering Group', 'Infrastructure Systems Co',
            'Environmental Technologies', 'Network Solutions Ltd', 'Treatment Systems Group',
            'Digital Water Solutions', 'Asset Management Partners'
        ]
        
        selected_suppliers = random.sample(supplier_names, num_suppliers)
        market_size = segment['market_size_gbp_m']
        
        for i, supplier in enumerate(selected_suppliers):
            # Market leader gets higher share
            if i == 0:
                share = random.uniform(25, 40)
            elif i == 1:
                share = random.uniform(15, 25)
            else:
                share = random.uniform(5, 15)
            
            revenue = market_size * (share / 100)
            
            concentration_data.append({
                'market_segment': segment['market_segment'],
                'supplier': supplier,
                'revenue_gbp_m': round(revenue, 1),
                'market_share': round(share / 100, 3),  # Convert to decimal for percentage calculations
                'market_size_gbp_m': market_size,  # Add expected column
                'growth_rate': segment['annual_growth_rate_percent'],  # Add growth rate from market intelligence
                'competitive_position': 'Leader' if i == 0 else 'Challenger' if i == 1 else 'Follower',
                'financial_health': random.choice(['Strong', 'Stable', 'Moderate']),
                'innovation_score': random.uniform(3.0, 5.0)
            })
    
    return pd.DataFrame(concentration_data)

def generate_t1_supplier_health_data():
    """Generate realistic water utility Tier 1 supplier health assessment data"""
    
    # Realistic water utility suppliers matching the story
    suppliers_data = [
        {
            'supplier_name': 'Thames Water Engineering',
            'financial_score': 8.9,
            'delivery_performance': 0.96,
            'quality_score': 9.2,
            'innovation_index': 0.85,
            'relationship_strength': 'Strategic',
            'risk_rating': 'Low',
            'market_position': 'Market Leader',
            'contracts_active': 18,
            'total_spend_gbp_m': 285.0,
            'esg_score': 0.92,
            'cyber_security_rating': 'A',
            'capacity_utilization': 0.88
        },
        {
            'supplier_name': 'Severn Trent Construction',
            'financial_score': 6.2,
            'delivery_performance': 0.73,
            'quality_score': 6.8,
            'innovation_index': 0.45,
            'relationship_strength': 'Conditional',
            'risk_rating': 'High',
            'market_position': 'Challenger',
            'contracts_active': 12,
            'total_spend_gbp_m': 220.0,
            'esg_score': 0.58,
            'cyber_security_rating': 'C',
            'capacity_utilization': 0.95
        },
        {
            'supplier_name': 'Anglian Water Projects',
            'financial_score': 7.6,
            'delivery_performance': 0.84,
            'quality_score': 7.9,
            'innovation_index': 0.68,
            'relationship_strength': 'Preferred',
            'risk_rating': 'Medium',
            'market_position': 'Strong Player',
            'contracts_active': 15,
            'total_spend_gbp_m': 195.0,
            'esg_score': 0.78,
            'cyber_security_rating': 'B',
            'capacity_utilization': 0.82
        },
        {
            'supplier_name': 'Yorkshire Water Services',
            'financial_score': 6.8,
            'delivery_performance': 0.79,
            'quality_score': 7.1,
            'innovation_index': 0.52,
            'relationship_strength': 'Approved',
            'risk_rating': 'High',
            'market_position': 'Strong Player',
            'contracts_active': 14,
            'total_spend_gbp_m': 180.0,
            'esg_score': 0.65,
            'cyber_security_rating': 'B',
            'capacity_utilization': 0.91
        },
        {
            'supplier_name': 'United Utilities Alliance',
            'financial_score': 8.4,
            'delivery_performance': 0.91,
            'quality_score': 8.6,
            'innovation_index': 0.89,
            'relationship_strength': 'Strategic',
            'risk_rating': 'Low',
            'market_position': 'Market Leader',
            'contracts_active': 16,
            'total_spend_gbp_m': 160.0,
            'esg_score': 0.87,
            'cyber_security_rating': 'A',
            'capacity_utilization': 0.75
        }
    ]
    
    return pd.DataFrame(suppliers_data)

def generate_supply_chain_kpi_data():
    """Generate supply chain KPI performance data"""
    import random
    
    suppliers = [
        'Infrastructure Contractor A', 'Engineering Solutions B', 'Construction Group C', 'Design Build Co D',
        'Water Systems E', 'Civil Engineering F', 'Technology Provider G', 'Equipment Supplier H'
    ]
    
    kpis = [
        'On-Time Delivery', 'Quality Performance', 'Cost Performance', 'Innovation Delivery',
        'Sustainability Score', 'Safety Performance', 'Relationship Health', 'Capacity Availability'
    ]
    
    data = []
    for supplier in suppliers:
        for kpi in kpis:
            # Generate realistic KPI scores
            if 'Safety' in kpi:
                target = random.uniform(95, 99.5)
                actual = target + random.uniform(-5, 2)
            elif 'Cost' in kpi:
                target = random.uniform(90, 95)
                actual = target + random.uniform(-10, 5)
            else:
                target = random.uniform(85, 95)
                actual = target + random.uniform(-15, 10)
            
            actual = max(0, min(100, actual))
            
            data.append({
                'supplier': supplier,
                'kpi': kpi,
                'target_score': target,
                'actual_score': actual,
                'variance': actual - target,
                'trend': random.choice(['Improving', 'Stable', 'Declining']),
                'priority': random.choice(['High', 'Medium', 'Low']),
                'support_needed': random.choice(['Yes', 'No']),
                'investment_potential': random.uniform(0, 100000)
            })
    
    return pd.DataFrame(data)

def load_all_sample_data():
    """Load all sample data into session state"""
    try:
        st.session_state.df_market_segments = generate_market_segments_data()
        st.session_state.df_competencies = generate_competencies_data()
        st.session_state.df_demand_pipeline = generate_demand_pipeline_data()
        st.session_state.df_sourcing_pipeline = generate_sourcing_pipeline_data()
        st.session_state.df_team_performance = generate_team_performance_data()
        st.session_state.df_supplier_kpis = generate_supplier_kpis_data()
        st.session_state.df_sub_tier_map = generate_sub_tier_map_data()
        st.session_state.df_supply_chain_risks = generate_supply_chain_risks_data()
        
        # Enhanced data for new features
        st.session_state.df_procurement_routes = generate_procurement_routes_data()
        st.session_state.df_team_capacity = generate_team_capacity_data()
        st.session_state.df_market_concentration = generate_market_concentration_data()
        st.session_state.df_t1_supplier_health = generate_t1_supplier_health_data()
        st.session_state.df_supply_chain_kpis = generate_supply_chain_kpi_data()
        
        return True
    except Exception as e:
        st.error(f"Error loading sample data: {str(e)}")
        return False

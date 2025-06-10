"""
Intelligent data generator for water infrastructure context using LLM-style reasoning
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any

def generate_water_infrastructure_context():
    """Generate realistic water infrastructure business context"""
    
    # Water utility business areas and their typical procurement categories
    infrastructure_categories = {
        "Water Treatment": ["Chemical Supply", "Membrane Systems", "Filtration Equipment", "Dosing Systems"],
        "Distribution Network": ["Pipeline Installation", "Valve Replacement", "Pump Stations", "Network Monitoring"],
        "Wastewater Treatment": ["Biological Treatment", "Sludge Management", "Effluent Systems", "Aeration Equipment"],
        "Smart Infrastructure": ["SCADA Systems", "IoT Sensors", "Data Analytics", "Control Systems"],
        "Asset Management": ["Condition Assessment", "Predictive Maintenance", "Asset Replacement", "Inspection Services"],
        "Environmental Compliance": ["Sampling & Testing", "Environmental Monitoring", "Regulatory Reporting", "Emissions Control"],
        "Customer Services": ["Meter Reading", "Billing Systems", "Customer Contact", "Digital Services"],
        "Energy & Carbon": ["Renewable Energy", "Energy Efficiency", "Carbon Reduction", "Green Technology"]
    }
    
    # Realistic supplier ecosystem for water utilities
    tier1_suppliers = [
        {"name": "Infrastructure Solutions Group", "specialties": ["Water Treatment", "Distribution Network"], "risk": "Low"},
        {"name": "Aqua Engineering Partners", "specialties": ["Wastewater Treatment", "Environmental Compliance"], "risk": "Medium"},
        {"name": "Digital Water Technologies", "specialties": ["Smart Infrastructure", "Customer Services"], "risk": "Low"},
        {"name": "Sustainable Infrastructure Ltd", "specialties": ["Energy & Carbon", "Asset Management"], "risk": "Medium"},
        {"name": "Advanced Treatment Systems", "specialties": ["Water Treatment", "Wastewater Treatment"], "risk": "High"},
    ]
    
    # Performance commitments aligned with regulatory framework
    performance_commitments = [
        {"name": "Water Quality Compliance", "target": 99.96, "unit": "%", "penalty_rate": 2.5},
        {"name": "Supply Interruptions", "target": 15, "unit": "minutes/property", "penalty_rate": 1.8},
        {"name": "Mains Repairs", "target": 150, "unit": "repairs/1000km", "penalty_rate": 1.2},
        {"name": "Customer Satisfaction", "target": 4.2, "unit": "score/5", "penalty_rate": 3.0},
        {"name": "Leakage Reduction", "target": 180, "unit": "Ml/day", "penalty_rate": 4.5},
        {"name": "Pollution Incidents", "target": 25, "unit": "incidents/year", "penalty_rate": 5.0},
        {"name": "Energy Efficiency", "target": 0.85, "unit": "kWh/Ml", "penalty_rate": 2.0},
        {"name": "Biodiversity Enhancement", "target": 15, "unit": "sites", "penalty_rate": 1.5},
    ]
    
    return infrastructure_categories, tier1_suppliers, performance_commitments

def generate_realistic_procurement_data():
    """Generate realistic Thames Water AMP8 procurement pipeline data"""
    
    # Thames Water AMP8 procurement packages aligned with regulatory commitments
    procurement_packages = [
        {
            'package_name': 'Thames Valley Sewer Flooding Reduction Programme',
            'procurement_stage': 'Contract Management',
            'estimated_value_gbp_m': 89.5,
            'category': 'Internal Sewer Flooding',
            'supplier': 'Severn Trent Construction',
            'risk_level': 'Critical',
            'start_date': datetime(2024, 4, 1),
            'end_date': datetime(2025, 3, 31),
            'procurement_route': 'AMP8 Framework',
            'team_lead': 'Sarah Mitchell',
            'region': 'Thames Valley',
            'status': 'Critical - ODI at Risk (£4.2M penalty exposure)',
            'amp8_commitment': 'Internal Sewer Flooding - Target: <2,500 incidents/year'
        },
        {
            'package_name': 'Leakage Reduction Programme - London Ring Main',
            'procurement_stage': 'Contract Management',
            'estimated_value_gbp_m': 156.2,
            'category': 'Leakage',
            'supplier': 'Thames Water Engineering',
            'risk_level': 'Low',
            'start_date': datetime(2024, 1, 1),
            'end_date': datetime(2029, 12, 31),
            'procurement_route': 'AMP8 Alliance',
            'team_lead': 'Emma Richardson',
            'region': 'London',
            'status': 'On Track - Leading Industry Performance',
            'amp8_commitment': 'Leakage Reduction - Target: 240 Ml/d by 2030'
        },
        {
            'package_name': 'Customer Service Excellence Programme',
            'procurement_stage': 'Contract Management',
            'estimated_value_gbp_m': 42.8,
            'category': 'C-MeX Performance',
            'supplier': 'United Utilities Alliance',
            'risk_level': 'Low',
            'start_date': datetime(2024, 2, 1),
            'end_date': datetime(2025, 3, 31),
            'procurement_route': 'Innovation Partnership',
            'team_lead': 'Lisa Chen',
            'region': 'Thames Valley',
            'status': 'Exceeding Targets - Customer Satisfaction 85%',
            'amp8_commitment': 'C-MeX Score - Target: Upper Quartile Performance'
        },
        {
            'package_name': 'Pollution Incident Reduction - River Thames',
            'procurement_stage': 'Contract Management',
            'estimated_value_gbp_m': 73.5,
            'category': 'Environmental Performance',
            'supplier': 'Yorkshire Water Services',
            'risk_level': 'High',
            'start_date': datetime(2024, 3, 1),
            'end_date': datetime(2025, 12, 31),
            'procurement_route': 'AMP8 Framework',
            'team_lead': 'David Williams',
            'region': 'Thames Valley',
            'status': 'Environmental Concerns - 12 Category 3 incidents YTD',
            'amp8_commitment': 'Pollution Incidents - Target: <15 Category 3+ incidents/year'
        },
        {
            'package_name': 'Thames Tideway Tunnel Integration Works',
            'procurement_stage': 'Contract Management',
            'estimated_value_gbp_m': 289.7,
            'category': 'Major Infrastructure',
            'supplier': 'Anglian Water Projects',
            'risk_level': 'Medium',
            'start_date': datetime(2024, 4, 1),
            'end_date': datetime(2026, 3, 31),
            'procurement_route': 'Major Capital Framework',
            'team_lead': 'James Anderson',
            'region': 'London',
            'status': 'On Track - Integration Phase Critical',
            'amp8_commitment': 'Sewer Overflows - Support TTT CSO reduction targets'
        },
        {
            'package_name': 'Supply Interruption Resilience Programme',
            'procurement_stage': 'Contract Management',
            'estimated_value_gbp_m': 127.3,
            'category': 'Water Supply Resilience',
            'supplier': 'Thames Water Engineering',
            'risk_level': 'Low',
            'start_date': datetime(2024, 1, 15),
            'end_date': datetime(2027, 3, 31),
            'procurement_route': 'Strategic Alliance',
            'team_lead': 'Michael Roberts',
            'region': 'Thames Valley',
            'status': 'Performance Improving - 8.2 mins/prop average',
            'amp8_commitment': 'Supply Interruptions - Target: <8 minutes/property/year'
        },
        {
            'package_name': 'Smart Water Network Implementation',
            'procurement_stage': 'Procurement',
            'estimated_value_gbp_m': 95.4,
            'category': 'Digital Transformation',
            'supplier': 'Market Evaluation',
            'risk_level': 'Medium',
            'start_date': datetime(2024, 9, 1),
            'end_date': datetime(2026, 12, 31),
            'procurement_route': 'Innovation Competition',
            'team_lead': 'Rachel Green',
            'region': 'Thames Valley',
            'status': 'Procurement Phase - AI/IoT Integration Focus',
            'amp8_commitment': 'Per Capita Consumption - Smart metering enabler'
        },
        {
            'package_name': 'Biodiversity Net Gain Implementation',
            'procurement_stage': 'Contract Award',
            'estimated_value_gbp_m': 34.6,
            'category': 'Environmental Enhancement',
            'supplier': 'Anglian Water Projects',
            'risk_level': 'Low',
            'start_date': datetime(2024, 6, 1),
            'end_date': datetime(2025, 8, 31),
            'procurement_route': 'Sustainability Framework',
            'team_lead': 'Sophie Taylor',
            'region': 'Thames Valley',
            'status': 'Exemplary Performance - 150 hectares enhanced',
            'amp8_commitment': 'Biodiversity - Target: 8% net gain by 2030'
        },
        {
            'package_name': 'Water Quality Compliance Enhancement',
            'procurement_stage': 'Contract Management',
            'estimated_value_gbp_m': 68.9,
            'category': 'Water Quality',
            'supplier': 'Thames Water Engineering',
            'risk_level': 'Low',
            'start_date': datetime(2024, 2, 15),
            'end_date': datetime(2025, 11, 30),
            'procurement_route': 'Quality Assurance Framework',
            'team_lead': 'Andrew Davis',
            'region': 'Thames Valley',
            'status': 'Meeting Standards - 99.97% compliance achieved',
            'amp8_commitment': 'Water Quality - Target: 99.96% regulatory compliance'
        }
    ]
    
    # Convert to DataFrame with proper data types
    df = pd.DataFrame(procurement_packages)
    
    # Add realistic procurement timeline and financial data
    df['days_to_award'] = [(pkg['start_date'] - datetime.now()).days if pkg['procurement_stage'] != 'Contract Management' else 0 for pkg in procurement_packages]
    df['contract_duration_months'] = [(pkg['end_date'] - pkg['start_date']).days / 30 for pkg in procurement_packages]
    df['spend_to_date_gbp_m'] = [
        pkg['estimated_value_gbp_m'] * random.uniform(0.1, 0.8) if pkg['procurement_stage'] == 'Contract Management' 
        else 0 for pkg in procurement_packages
    ]
    
    return df
    
    categories, suppliers, _ = generate_water_infrastructure_context()
    
    # Generate procurement projects with realistic characteristics
    projects = []
    project_id = 1
    
    for business_area, procurement_cats in categories.items():
        for category in procurement_cats:
            # Generate 1-3 projects per category
            num_projects = random.randint(1, 3)
            
            for i in range(num_projects):
                # Realistic contract values based on category
                if "Systems" in category or "Infrastructure" in business_area:
                    value_range = (5, 50)  # £5M - £50M for major infrastructure
                elif "Supply" in category or "Services" in category:
                    value_range = (0.5, 15)  # £0.5M - £15M for services/supplies
                else:
                    value_range = (1, 25)  # £1M - £25M for mixed projects
                
                contract_value = round(random.uniform(*value_range), 1)
                
                # Risk assessment based on value and complexity
                if contract_value > 30:
                    risk_weights = [0.2, 0.3, 0.5]  # Higher risk for large contracts
                elif contract_value > 10:
                    risk_weights = [0.4, 0.4, 0.2]  # Balanced risk for medium contracts
                else:
                    risk_weights = [0.6, 0.3, 0.1]  # Lower risk for smaller contracts
                
                rag_status = random.choices(['Green', 'Amber', 'Red'], weights=risk_weights)[0]
                
                # Timeline based on contract complexity
                if contract_value > 20:
                    duration_months = random.randint(18, 36)
                elif contract_value > 5:
                    duration_months = random.randint(12, 24)
                else:
                    duration_months = random.randint(6, 18)
                
                start_date = datetime.now() + timedelta(days=random.randint(-365, 365))
                
                # Realistic supplier response rates
                if "Digital" in category or "Smart" in category:
                    supplier_responses = random.randint(3, 8)  # Competitive tech market
                elif "Chemical" in category or "Testing" in category:
                    supplier_responses = random.randint(2, 5)  # Specialized suppliers
                else:
                    supplier_responses = random.randint(4, 12)  # General infrastructure
                
                projects.append({
                    'project_id': f"WI-{project_id:04d}",
                    'project_name': f"{category} - Phase {i+1}",
                    'business_area': business_area,
                    'procurement_category': category,
                    'contract_value_gbp_m': contract_value,
                    'rag_status': rag_status,
                    'duration_months': duration_months,
                    'start_date': start_date,
                    'supplier_responses': supplier_responses,
                    'procurement_route': random.choice(['Framework', 'Open Tender', 'Negotiated', 'Dynamic Purchasing']),
                    'stage': random.choice(['Planning', 'Tender', 'Evaluation', 'Award', 'Delivery', 'Complete']),
                    'sustainability_score': round(random.uniform(2.5, 5.0), 1),
                    'innovation_rating': random.choice(['Low', 'Medium', 'High']),
                    'local_content_percent': random.randint(15, 85)
                })
                
                project_id += 1
    
    return pd.DataFrame(projects)

def generate_realistic_supplier_network():
    """Generate realistic supplier network with tier structure"""
    
    categories, tier1_suppliers, _ = generate_water_infrastructure_context()
    
    suppliers = []
    supplier_id = 1
    
    # Generate Tier 1 suppliers
    for supplier_info in tier1_suppliers:
        spend = random.uniform(80, 200)  # £80M - £200M for major contractors
        
        performance_score = 0.85 if supplier_info["risk"] == "Low" else 0.75 if supplier_info["risk"] == "Medium" else 0.65
        performance_score += random.uniform(-0.1, 0.1)  # Add variance
        
        risk_colors = {"Low": "#28a745", "Medium": "#ffc107", "High": "#dc3545"}
        
        suppliers.append({
            'id': f"T1_{supplier_id:03d}",
            'name': supplier_info["name"],
            'tier': 1,
            'parent_id': 'Water_Utility',
            'spend_gbp_m': round(spend, 1),
            'risk_category': supplier_info["risk"],
            'risk_color': risk_colors[supplier_info["risk"]],
            'risk_score': 5 if supplier_info["risk"] == "High" else 3 if supplier_info["risk"] == "Medium" else 1,
            'performance': round(performance_score, 3),
            'location': random.choice(['London', 'Birmingham', 'Manchester', 'Leeds', 'Bristol']),
            'specialties': ', '.join(supplier_info["specialties"]),
            'contract_count': random.randint(8, 25),
            'years_relationship': random.randint(3, 15)
        })
        
        # Generate Tier 2 suppliers for each Tier 1
        num_tier2 = random.randint(2, 4)
        
        for j in range(num_tier2):
            t2_spend = spend * random.uniform(0.1, 0.3)  # 10-30% of parent spend
            t2_risk = random.choices(['Low', 'Medium', 'High'], weights=[0.5, 0.4, 0.1])[0]
            t2_performance = random.uniform(0.7, 0.95)
            
            tier2_names = [
                "Specialist Equipment Solutions", "Technical Services Group", "Component Manufacturing Ltd",
                "Installation Services Co", "Quality Testing Partners", "Materials Supply Chain",
                "Engineering Consultancy", "Maintenance Solutions Ltd", "Logistics & Distribution",
                "Environmental Services Group", "Digital Solutions Provider", "Training & Development Co"
            ]
            
            suppliers.append({
                'id': f"T2_{supplier_id:03d}_{j+1:02d}",
                'name': random.choice(tier2_names),
                'tier': 2,
                'parent_id': f"T1_{supplier_id:03d}",
                'spend_gbp_m': round(t2_spend, 1),
                'risk_category': t2_risk,
                'risk_color': risk_colors[t2_risk],
                'risk_score': 5 if t2_risk == "High" else 3 if t2_risk == "Medium" else 1,
                'performance': round(t2_performance, 3),
                'location': random.choice(['Reading', 'Oxford', 'Cambridge', 'Coventry', 'Nottingham']),
                'specialties': random.choice(list(categories.keys())),
                'contract_count': random.randint(2, 8),
                'years_relationship': random.randint(1, 8)
            })
        
        supplier_id += 1
    
    return pd.DataFrame(suppliers)

def generate_realistic_performance_commitments():
    """Generate realistic performance commitment tracking data"""
    
    _, _, commitments = generate_water_infrastructure_context()
    
    pc_data = []
    
    for pc in commitments:
        # Generate realistic performance with seasonal variation
        months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
        
        for month in months:
            # Add realistic seasonal factors
            seasonal_factor = 1.0
            if pc["name"] in ["Supply Interruptions", "Mains Repairs"] and month in ['Dec', 'Jan', 'Feb']:
                seasonal_factor = 1.3  # Winter challenges
            elif pc["name"] == "Leakage Reduction" and month in ['Jul', 'Aug', 'Sep']:
                seasonal_factor = 0.9  # Summer improvements
            elif pc["name"] == "Customer Satisfaction" and month in ['Dec', 'Jan']:
                seasonal_factor = 0.95  # Holiday period impacts
            
            # Generate actual performance with realistic variance
            if pc["unit"] == "%":
                actual = pc["target"] * seasonal_factor * random.uniform(0.985, 1.005)
            elif "minutes" in pc["unit"] or "repairs" in pc["unit"] or "incidents" in pc["unit"]:
                actual = pc["target"] * seasonal_factor * random.uniform(0.8, 1.2)
            else:
                actual = pc["target"] * seasonal_factor * random.uniform(0.95, 1.05)
            
            # Determine RAG status
            tolerance = 0.02 if pc["unit"] == "%" else 0.1
            
            if pc["unit"] == "%" or "score" in pc["unit"] or "kWh" in pc["unit"]:
                # Higher is better
                if actual >= pc["target"] * (1 - tolerance):
                    rag = "Green"
                elif actual >= pc["target"] * (1 - tolerance * 2):
                    rag = "Amber"
                else:
                    rag = "Red"
            else:
                # Lower is better
                if actual <= pc["target"] * (1 + tolerance):
                    rag = "Green"
                elif actual <= pc["target"] * (1 + tolerance * 2):
                    rag = "Amber"
                else:
                    rag = "Red"
            
            # Calculate financial impact
            if rag == "Red":
                variance = abs(actual - pc["target"]) / pc["target"]
                financial_impact = variance * pc["penalty_rate"] * random.uniform(0.8, 1.2)
            else:
                financial_impact = 0
            
            pc_data.append({
                'commitment_name': pc["name"],
                'target_value': pc["target"],
                'actual_value': round(actual, 2),
                'unit': pc["unit"],
                'month': month,
                'rag_status': rag,
                'variance_percent': round(((actual - pc["target"]) / pc["target"]) * 100, 2),
                'financial_impact_gbp_m': round(financial_impact, 2),
                'penalty_rate': pc["penalty_rate"],
                'improvement_actions': generate_improvement_actions(pc["name"], rag),
                'reporting_period': f"2024-{months.index(month) + 4 if months.index(month) < 9 else months.index(month) - 8:02d}",
                'risk_trend': random.choice(['Improving', 'Stable', 'Deteriorating'])
            })
    
    return pd.DataFrame(pc_data)

def generate_improvement_actions(commitment_name: str, rag_status: str) -> str:
    """Generate realistic improvement actions based on performance area and status"""
    
    actions_map = {
        "Water Quality Compliance": {
            "Red": "Emergency sampling protocol activated, additional treatment stages implemented",
            "Amber": "Enhanced monitoring at critical sites, process optimization underway",
            "Green": "Continuous monitoring maintained, proactive quality assurance"
        },
        "Supply Interruptions": {
            "Red": "Emergency response teams mobilized, network reinforcement accelerated",
            "Amber": "Predictive maintenance increased, vulnerable assets identified",
            "Green": "Routine maintenance optimized, resilience planning active"
        },
        "Leakage Reduction": {
            "Red": "Active leak detection intensified, smart meter rollout expedited",
            "Amber": "Pressure management optimization, targeted repairs prioritized",
            "Green": "Proactive network monitoring, efficiency improvements sustained"
        }
    }
    
    default_actions = {
        "Red": "Immediate action plan activated, additional resources deployed",
        "Amber": "Enhanced monitoring implemented, improvement measures active",
        "Green": "Performance maintained, continuous improvement focus"
    }
    
    return actions_map.get(commitment_name, default_actions).get(rag_status, "Performance under review")

def generate_realistic_market_intelligence():
    """Generate realistic market intelligence data for water infrastructure"""
    
    market_segments = [
        "Water Treatment Technology", "Distribution Infrastructure", "Wastewater Solutions",
        "Smart Water Systems", "Environmental Compliance", "Energy & Carbon Management",
        "Asset Management Services", "Customer Technology Solutions"
    ]
    
    intelligence_data = []
    
    for segment in market_segments:
        # Generate market insights
        market_size = random.uniform(200, 1500)  # £200M - £1.5B market size
        growth_rate = random.uniform(-2, 8)  # -2% to 8% annual growth
        
        # Generate realistic market dynamics
        if "Smart" in segment or "Digital" in segment:
            growth_rate = random.uniform(5, 15)  # Higher growth for digital
            consolidation_trend = "Rapid consolidation with tech giants acquiring specialists"
        elif "Environmental" in segment:
            growth_rate = random.uniform(3, 10)  # Strong regulatory-driven growth
            consolidation_trend = "Increasing focus on compliance capabilities"
        else:
            consolidation_trend = "Stable market with established players"
        
        intelligence_data.append({
            'market_segment': segment,
            'market_size_gbp_m': round(market_size, 0),
            'annual_growth_rate_percent': round(growth_rate, 1),
            'key_drivers': generate_market_drivers(segment),
            'consolidation_trend': consolidation_trend,
            'regulatory_impact': generate_regulatory_impact(segment),
            'innovation_focus': generate_innovation_focus(segment),
            'pricing_trend': random.choice(['Increasing', 'Stable', 'Decreasing']),
            'supply_chain_risk': random.choice(['Low', 'Medium', 'High']),
            'sustainability_pressure': random.choice(['Low', 'Medium', 'High']),
            'talent_availability': random.choice(['Abundant', 'Adequate', 'Constrained']),
            'competitive_intensity': random.choice(['Low', 'Medium', 'High'])
        })
    
    return pd.DataFrame(intelligence_data)

def generate_market_drivers(segment: str) -> str:
    """Generate realistic market drivers for each segment"""
    
    drivers_map = {
        "Water Treatment Technology": "Aging infrastructure replacement, stricter quality standards, climate resilience",
        "Distribution Infrastructure": "Network modernization, smart meter deployment, pressure management",
        "Wastewater Solutions": "Environmental regulations, capacity expansion, energy recovery",
        "Smart Water Systems": "Digital transformation, operational efficiency, customer engagement",
        "Environmental Compliance": "Regulatory tightening, biodiversity requirements, carbon reduction",
        "Energy & Carbon Management": "Net zero commitments, renewable energy adoption, efficiency targets",
        "Asset Management Services": "Predictive maintenance, data analytics, lifecycle optimization",
        "Customer Technology Solutions": "Digital channels, self-service capabilities, billing modernization"
    }
    
    return drivers_map.get(segment, "Market evolution, regulatory change, technology advancement")

def generate_regulatory_impact(segment: str) -> str:
    """Generate realistic regulatory impact assessment"""
    
    impacts = [
        "Significant regulatory drivers accelerating investment",
        "Moderate compliance requirements supporting steady growth",
        "Emerging regulations creating new market opportunities",
        "Established framework providing market stability",
        "Increasing regulatory scrutiny driving innovation"
    ]
    
    return random.choice(impacts)

def generate_innovation_focus(segment: str) -> str:
    """Generate realistic innovation focus areas"""
    
    innovation_map = {
        "Smart Water Systems": "AI-powered analytics, IoT sensors, real-time optimization",
        "Environmental Compliance": "Advanced monitoring, automated reporting, predictive compliance",
        "Energy & Carbon Management": "Renewable integration, energy recovery, carbon capture",
        "Water Treatment Technology": "Membrane technology, advanced oxidation, smart dosing"
    }
    
    default_innovations = [
        "Process automation and digitalization",
        "Sustainability and circular economy solutions",
        "Advanced materials and nanotechnology",
        "Data analytics and predictive capabilities"
    ]
    
    return innovation_map.get(segment, random.choice(default_innovations))
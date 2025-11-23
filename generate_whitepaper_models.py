import os
import json
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Comprehensive list of wildfire models from Appendix A of the white paper
WILDFIRE_MODELS = [
    # Operational Fire Spread Models
    {
        "filename": "farsite.qmd",
        "title": "FARSITE - Fire Area Simulator",
        "category": "Operational Fire Spread Models",
        "focus": "spatially explicit fire growth simulation, multiple fuel models, weather integration, suppression tactics modeling",
        "organization": "USDA Forest Service",
        "type": "Semi-empirical"
    },
    {
        "filename": "flammap.qmd",
        "title": "FlamMap - Fire Behavior Mapping and Analysis",
        "category": "Operational Fire Spread Models",
        "focus": "potential fire behavior calculations, minimum travel time, treatment optimization, landscape-scale analysis",
        "organization": "USDA Forest Service",
        "type": "Semi-empirical"
    },
    {
        "filename": "behaveplus.qmd",
        "title": "BehavePlus Fire Modeling System",
        "category": "Operational Fire Spread Models",
        "focus": "surface fire spread, crown fire, spotting distance, fire effects, safety zone calculations",
        "organization": "USDA Forest Service",
        "type": "Semi-empirical"
    },
    {
        "filename": "fspro.qmd",
        "title": "FSPro - Fire Spread Probability",
        "category": "Operational Fire Spread Models",
        "focus": "probabilistic fire spread modeling, risk assessment, decision support for large fires",
        "organization": "USDA Forest Service",
        "type": "Probabilistic"
    },
    {
        "filename": "wfdss.qmd",
        "title": "WFDSS - Wildland Fire Decision Support System",
        "category": "Decision Support Systems",
        "focus": "integrated decision support, risk assessment, strategic planning, multi-objective optimization",
        "organization": "USDA Forest Service & DOI",
        "type": "Integrated System"
    },
    
    # Physics-Based Models
    {
        "filename": "firetec.qmd",
        "title": "FIRETEC - Physics-Based Fire Model",
        "category": "Physics-Based Models",
        "focus": "computational fluid dynamics, detailed physics, fire-atmosphere coupling, complex terrain",
        "organization": "Los Alamos National Laboratory",
        "type": "Physics-based"
    },
    {
        "filename": "wfds.qmd",
        "title": "WFDS - Wildland-Urban Interface Fire Dynamics Simulator",
        "category": "Physics-Based Models",
        "focus": "WUI fires, structural ignition, detailed combustion physics, smoke transport",
        "organization": "NIST",
        "type": "Physics-based"
    },
    {
        "filename": "firefoam.qmd",
        "title": "FireFOAM - OpenFOAM Fire Solver",
        "category": "Physics-Based Models",
        "focus": "open-source CFD, large eddy simulation, turbulent combustion, research applications",
        "organization": "FM Global/OpenFOAM",
        "type": "Physics-based"
    },
    {
        "filename": "quic-fire.qmd",
        "title": "QUIC-Fire - Fast Physics-Based Model",
        "category": "Physics-Based Models",
        "focus": "fast-running physics model, urban interface, smoke dispersion, GPU acceleration",
        "organization": "Los Alamos National Laboratory",
        "type": "Physics-based"
    },
    
    # Coupled Weather-Fire Models
    {
        "filename": "wrf-sfire.qmd",
        "title": "WRF-SFIRE - Coupled Atmosphere-Fire Model",
        "category": "Coupled Weather-Fire Models",
        "focus": "two-way fire-atmosphere coupling, mesoscale weather, operational forecasting, smoke transport",
        "organization": "NCAR/University of Denver",
        "type": "Coupled model"
    },
    {
        "filename": "arps-canopy.qmd",
        "title": "ARPS-CANOPY - Advanced Regional Prediction System",
        "category": "Coupled Weather-Fire Models",
        "focus": "mesoscale atmospheric modeling, canopy interactions, fire weather prediction",
        "organization": "University of Oklahoma",
        "type": "Coupled model"
    },
    {
        "filename": "meso-nh-forefire.qmd",
        "title": "Meso-NH/ForeFire - French Coupled Model",
        "category": "Coupled Weather-Fire Models",
        "focus": "European fire modeling, Mediterranean fires, atmospheric coupling, research applications",
        "organization": "Météo-France/Université de Corse",
        "type": "Coupled model"
    },
    
    # Canadian Models
    {
        "filename": "cffdrs.qmd",
        "title": "CFFDRS - Canadian Forest Fire Danger Rating System",
        "category": "Fire Danger Rating Systems",
        "focus": "fire weather index, fire behavior prediction, fuel moisture codes, national standard",
        "organization": "Canadian Forest Service",
        "type": "Empirical"
    },
    {
        "filename": "prometheus.qmd",
        "title": "Prometheus - Canadian Fire Growth Model",
        "category": "Operational Fire Spread Models",
        "focus": "elliptical fire growth, Canadian fuel types, operational use, deterministic spread",
        "organization": "Canadian Forest Service",
        "type": "Semi-empirical"
    },
    {
        "filename": "burn-p3.qmd",
        "title": "Burn-P3 - Probability, Prediction, and Planning",
        "category": "Probabilistic Models",
        "focus": "burn probability modeling, risk assessment, landscape planning, Monte Carlo simulation",
        "organization": "Canadian Forest Service",
        "type": "Probabilistic"
    },
    
    # Australian Models
    {
        "filename": "phoenix-rapidfire.qmd",
        "title": "Phoenix RapidFire",
        "category": "Operational Fire Spread Models",
        "focus": "Australian conditions, eucalyptus forests, ember transport, operational forecasting",
        "organization": "University of Melbourne/Bushfire CRC",
        "type": "Semi-empirical"
    },
    {
        "filename": "spark.qmd",
        "title": "Spark - Wildfire Simulation Toolkit",
        "category": "Operational Fire Spread Models",
        "focus": "GPU-accelerated, ensemble simulations, operational forecasting, Australian fuels",
        "organization": "CSIRO",
        "type": "Semi-empirical"
    },
    {
        "filename": "australis.qmd",
        "title": "AUSTRALIS - Australian Fire Spread Simulator",
        "category": "Operational Fire Spread Models",
        "focus": "grassland fires, prescribed burning, Australian ecosystems, operational planning",
        "organization": "CSIRO",
        "type": "Semi-empirical"
    },
    
    # European Models
    {
        "filename": "firesite.qmd",
        "title": "FIRESITE - European Fire Simulation",
        "category": "Operational Fire Spread Models",
        "focus": "Mediterranean fires, European fuel models, multi-scale modeling, decision support",
        "organization": "European Forest Institute",
        "type": "Semi-empirical"
    },
    {
        "filename": "tiger.qmd",
        "title": "TIGER - Wildfire Spread Model",
        "category": "Research Models",
        "focus": "cellular automata, Mediterranean ecosystems, fire suppression, tactical planning",
        "organization": "University of Lisbon",
        "type": "Cellular automata"
    },
    
    # Machine Learning and AI Models
    {
        "filename": "wildfire-analyst.qmd",
        "title": "Wildfire Analyst Enterprise",
        "category": "Commercial Platforms",
        "focus": "real-time simulation, web-based platform, decision support, API integration",
        "organization": "Technosylva",
        "type": "Integrated platform"
    },
    {
        "filename": "ml-fire-prediction.qmd",
        "title": "Machine Learning Fire Prediction Systems",
        "category": "AI/ML Applications",
        "focus": "deep learning, neural networks, satellite data integration, next-generation prediction",
        "organization": "Various (Google, IBM, Microsoft)",
        "type": "Machine learning"
    },
    
    # Smoke and Emissions Models
    {
        "filename": "bluesky.qmd",
        "title": "BlueSky Smoke Modeling Framework",
        "category": "Smoke and Air Quality",
        "focus": "smoke emissions, air quality forecasting, trajectory modeling, health impacts",
        "organization": "USDA Forest Service",
        "type": "Integrated framework"
    },
    {
        "filename": "hysplit.qmd",
        "title": "HYSPLIT - Atmospheric Transport Model",
        "category": "Smoke and Air Quality",
        "focus": "smoke dispersion, trajectory analysis, air quality, atmospheric transport",
        "organization": "NOAA",
        "type": "Atmospheric model"
    },
    {
        "filename": "cmaq-smoke.qmd",
        "title": "CMAQ - Community Multiscale Air Quality Model",
        "category": "Smoke and Air Quality",
        "focus": "regional air quality, smoke chemistry, photochemical modeling, regulatory applications",
        "organization": "EPA",
        "type": "Chemical transport model"
    },
    
    # Fuel and Vegetation Models
    {
        "filename": "landfire.qmd",
        "title": "LANDFIRE - Landscape Fire and Resource Management",
        "category": "Fuel and Vegetation Data",
        "focus": "fuel mapping, vegetation data, disturbance tracking, national coverage",
        "organization": "USGS/USFS/DOI",
        "type": "Data system"
    },
    {
        "filename": "fuelcast.qmd",
        "title": "FuelCast - Live Fuel Moisture System",
        "category": "Fuel Moisture Models",
        "focus": "live fuel moisture content, remote sensing, predictive modeling, operational forecasting",
        "organization": "San Diego Gas & Electric/Technosylva",
        "type": "Predictive system"
    },
    {
        "filename": "iftdss.qmd",
        "title": "IFTDSS - Interagency Fuel Treatment Decision Support",
        "category": "Fuel Treatment Planning",
        "focus": "fuel treatment optimization, landscape planning, economic analysis, collaborative planning",
        "organization": "USDA Forest Service",
        "type": "Planning system"
    }
]

def generate_model_content(model_info):
    """Generate comprehensive content for a wildfire model"""
    
    prompt = f"""
    Create a comprehensive research directory page about {model_info['title']} for wildfire researchers and practitioners.
    
    Model Details:
    - Category: {model_info['category']}
    - Type: {model_info['type']}
    - Organization: {model_info['organization']}
    - Focus areas: {model_info['focus']}
    
    Structure the content with these sections:
    
    ## Overview
    Provide 2-3 paragraphs explaining what this model/system is, its primary purpose, and why it's important in wildfire management.
    
    ## Key Features and Capabilities
    List and explain the main features and what makes this model unique.
    
    ## Technical Specifications
    - Model type and approach
    - Input data requirements
    - Output products
    - Spatial and temporal resolution
    - Computational requirements
    
    ## Applications and Use Cases
    - Operational uses
    - Research applications
    - Planning and management applications
    - Case studies or notable deployments
    
    ## Strengths and Limitations
    - What this model does well
    - Known limitations or constraints
    - Best use conditions
    
    ## Data Requirements
    - Input data needed
    - Data formats
    - Data sources
    
    ## Training and Resources
    - Available training materials
    - Documentation
    - User communities
    - Support resources
    
    ## Integration with Other Systems
    - Compatible models and systems
    - Data exchange formats
    - Workflow integration
    
    ## Recent Updates and Developments
    - Latest version information
    - Recent improvements
    - Ongoing research
    
    ## Access and Availability
    - How to obtain the software
    - Licensing information
    - System requirements
    - Cost (if applicable)
    
    Write in a professional, technical tone suitable for researchers, fire managers, and practitioners.
    Include specific technical details, actual use cases, and practical information.
    Be comprehensive and accurate, focusing on practical application.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in wildfire modeling and simulation systems with deep knowledge of operational fire management tools."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating content for {model_info['title']}: {str(e)}")
        return None

def create_model_qmd_file(model_info, content):
    """Create a Quarto markdown file for a model"""
    
    qmd_template = f"""---
title: "{model_info['title']}"
description: "Comprehensive guide to {model_info['title']} - {model_info['focus']}"
date: {datetime.now().strftime('%Y-%m-%d')}
categories: [{model_info['category']}]
author: "AI Research Assistant"
toc: true
toc-depth: 3
---

# {model_info['title']}

::: {{.callout-note}}
## Quick Facts
- **Category**: {model_info['category']}
- **Model Type**: {model_info['type']}
- **Developed by**: {model_info['organization']}
- **Primary Focus**: {model_info['focus']}
:::

{content}

---

## Related Models and Resources

### Similar Models in This Category
Explore other {model_info['category'].lower()} models in our directory.

### Integration Partners
Models that commonly integrate with {model_info['title'].split(' - ')[0]}.

---

## Contributing to This Page

This page is part of the [Wildfire Simulation & Modeling Research Directory](https://wildfire-directory.netlify.app) maintained by [Rallypoint One](https://rallypoint1.com).

If you have:
- Updates or corrections
- Additional use cases or case studies
- Training resources or documentation
- Integration examples

Please [open an issue on GitHub](https://github.com/RallypointOne/wildfire-directory/issues) or [contact us](https://rallypoint1.com/contact).

---

*Last updated: {datetime.now().strftime('%B %d, %Y')}*
*This page was automatically generated using AI-assisted research. Content is regularly updated to reflect the latest developments.*
"""
    
    return qmd_template

def create_category_index_pages():
    """Create index pages for each category"""
    
    categories = {}
    for model in WILDFIRE_MODELS:
        category = model['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(model)
    
    index_pages = []
    
    for category, models in categories.items():
        filename = f"{category.lower().replace(' ', '-').replace('/', '-')}-index.qmd"
        
        content = f"""---
title: "{category}"
description: "Complete listing of {category.lower()} for wildfire research and operations"
date: {datetime.now().strftime('%Y-%m-%d')}
toc: true
---

# {category}

This section contains detailed information about {len(models)} {category.lower()} used in wildfire research and operations.

## Models in This Category

"""
        
        for model in models:
            model_name = model['title'].split(' - ')[0]
            content += f"""
### [{model['title']}]({model['filename']})
**Organization**: {model['organization']}  
**Type**: {model['type']}  
**Focus**: {model['focus']}

---
"""
        
        content += f"""

## Category Overview

The {category} category includes models and systems that focus on specific aspects of wildfire behavior, management, and analysis. These tools are essential for:

- Operational decision-making
- Research and development
- Planning and risk assessment
- Training and education

## Choosing the Right Model

When selecting a model from this category, consider:
- Your specific use case and objectives
- Available data and computational resources
- Required spatial and temporal resolution
- Integration with existing workflows
- Training and support availability

---

*Part of the [Wildfire Research Directory](https://wildfire-directory.netlify.app) by [Rallypoint One](https://rallypoint1.com)*
"""
        
        index_pages.append((filename, content))
    
    return index_pages

def main():
    """Generate content for all wildfire models from Appendix A"""
    
    print("🔥 Starting Wildfire Models Content Generation from White Paper Appendix A...")
    print(f"📚 Generating content for {len(WILDFIRE_MODELS)} models...")
    
    generated_files = []
    failed_models = []
    
    # Generate individual model pages
    for i, model in enumerate(WILDFIRE_MODELS, 1):
        print(f"\n[{i}/{len(WILDFIRE_MODELS)}] 📝 Generating: {model['title']}...")
        
        content = generate_model_content(model)
        
        if content:
            qmd_content = create_model_qmd_file(model, content)
            
            with open(model['filename'], 'w', encoding='utf-8') as f:
                f.write(qmd_content)
            
            generated_files.append(model['filename'])
            print(f"✅ Successfully created: {model['filename']}")
        else:
            failed_models.append(model['title'])
            print(f"❌ Failed to generate: {model['title']}")
    
    # Generate category index pages
    print("\n📑 Generating category index pages...")
    category_pages = create_category_index_pages()
    for filename, content in category_pages:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        generated_files.append(filename)
        print(f"✅ Created category index: {filename}")
    
    # Summary
    print(f"\n✨ Content Generation Complete!")
    print(f"📊 Summary:")
    print(f"  - Successfully generated: {len(generated_files)} files")
    print(f"  - Failed: {len(failed_models)} models")
    print(f"  - Categories created: {len(category_pages)}")
    
    if failed_models:
        print(f"\n⚠️ Failed models (can retry):")
        for model in failed_models:
            print(f"  - {model}")
    
    print(f"\n💡 Next steps:")
    print(f"  1. Review generated content")
    print(f"  2. Commit and push to GitHub")
    print(f"  3. Site will auto-deploy to Netlify")
    
    return len(generated_files)

if __name__ == "__main__":
    main()

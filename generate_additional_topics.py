import os
import json
from datetime import datetime
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# 10 Additional Essential Topics for Wildfire Research Directory
ADDITIONAL_TOPICS = [
    {
        "filename": "farsite-system.qmd",
        "title": "FARSITE Fire Simulation System - Complete Guide",
        "category": "Simulation Systems",
        "focus": "comprehensive FARSITE implementation, calibration, validation, case studies, advanced techniques, troubleshooting",
        "description": "In-depth guide to the FARSITE Fire Area Simulator including setup, operation, and advanced applications"
    },
    {
        "filename": "fire-weather-indices.qmd",
        "title": "Fire Weather Indices - FWI, FFDI, and Global Systems",
        "category": "Fire Danger Rating",
        "focus": "Canadian FWI system, Australian FFDI, US NFDRS, European EFFIS, calculation methods, operational use",
        "description": "Comprehensive overview of fire weather indices used globally for fire danger assessment"
    },
    {
        "filename": "burn-severity-mapping.qmd",
        "title": "Burn Severity Mapping and Assessment",
        "category": "Post-Fire Assessment",
        "focus": "dNBR, RdNBR, CBI methods, satellite-based assessment, field validation, BAER applications, ecological impacts",
        "description": "Methods and tools for assessing and mapping burn severity after wildfires"
    },
    {
        "filename": "debris-flow-prediction.qmd",
        "title": "Post-Fire Debris Flow Prediction and Risk",
        "category": "Post-Fire Hazards",
        "focus": "debris flow models, rainfall thresholds, hazard assessment, USGS tools, mitigation strategies, early warning",
        "description": "Predicting and mitigating post-fire debris flows and mudslides"
    },
    {
        "filename": "wui-modeling.qmd",
        "title": "Wildland-Urban Interface (WUI) Modeling and Risk",
        "category": "WUI Risk Assessment",
        "focus": "WUI mapping, structure ignition, defensible space, community planning, building codes, evacuation modeling",
        "description": "Comprehensive approaches to modeling and managing wildfire risk in the WUI"
    },
    {
        "filename": "climate-fire-projections.qmd",
        "title": "Climate Change and Future Fire Projections",
        "category": "Climate-Fire Interactions",
        "focus": "climate models, fire regime changes, vegetation shifts, feedback loops, adaptation strategies, scenario planning",
        "description": "Understanding and projecting how climate change will affect future wildfire activity"
    },
    {
        "filename": "indigenous-fire-management.qmd",
        "title": "Indigenous Fire Management and Cultural Burning",
        "category": "Traditional Practices",
        "focus": "traditional ecological knowledge, cultural burning practices, prescribed fire, collaboration models, restoration",
        "description": "Indigenous approaches to fire management and their integration with modern practices"
    },
    {
        "filename": "satellite-fire-detection.qmd",
        "title": "Satellite Fire Detection and Monitoring Systems",
        "category": "Remote Sensing",
        "focus": "MODIS, VIIRS, Landsat, Sentinel, GOES, geostationary platforms, active fire products, validation, limitations",
        "description": "Satellite systems and algorithms for detecting and monitoring active wildfires"
    },
    {
        "filename": "carbon-emissions-modeling.qmd",
        "title": "Wildfire Carbon Emissions and Climate Impacts",
        "category": "Emissions and Climate",
        "focus": "emission factors, carbon accounting, greenhouse gases, air quality impacts, climate feedback, mitigation",
        "description": "Modeling carbon emissions from wildfires and their climate implications"
    },
    {
        "filename": "insurance-risk-tools.qmd",
        "title": "Insurance Industry Wildfire Risk Assessment Tools",
        "category": "Risk Management",
        "focus": "catastrophe models, property risk assessment, portfolio analysis, pricing models, mitigation credits, resilience",
        "description": "Tools and methods used by insurance industry for wildfire risk assessment"
    }
]

def generate_topic_content(topic_info):
    """Generate comprehensive content for a wildfire research topic"""
    
    prompt = f"""
    Create a comprehensive, authoritative research directory page about: {topic_info['title']}
    
    Topic Details:
    - Category: {topic_info['category']}
    - Focus areas: {topic_info['focus']}
    - Description: {topic_info['description']}
    
    Structure the content with these detailed sections:
    
    ## Overview
    Provide 3-4 paragraphs explaining this topic's importance, current state, and role in wildfire management and research.
    
    ## Core Concepts and Principles
    Explain the fundamental concepts, theories, and scientific principles underlying this topic.
    
    ## Methods and Approaches
    Detail the main methodologies, techniques, and approaches used in this area.
    
    ## Current Tools and Technologies
    List and describe specific tools, software, platforms, and technologies currently used.
    Include both operational and research tools.
    
    ## Data Sources and Requirements
    - Key datasets used
    - Data collection methods
    - Data formats and standards
    - Availability and access
    
    ## Applications and Use Cases
    Provide real-world examples of how this is applied in:
    - Operational fire management
    - Research studies
    - Planning and policy
    - Risk assessment
    
    ## Case Studies and Examples
    Describe 2-3 specific examples or case studies demonstrating successful application.
    
    ## Current Research and Developments
    - Active research areas
    - Recent advances
    - Emerging technologies
    - Future directions
    
    ## Challenges and Limitations
    - Technical challenges
    - Operational constraints
    - Data limitations
    - Areas needing improvement
    
    ## Best Practices and Guidelines
    - Industry standards
    - Recommended procedures
    - Quality assurance
    - Common pitfalls to avoid
    
    ## Integration with Other Systems
    How this topic connects with other wildfire management tools and approaches.
    
    ## Resources and Training
    - Educational resources
    - Training programs
    - Certification options
    - Professional organizations
    - Key publications
    
    ## Stakeholders and Users
    Who uses this information and how:
    - Fire managers
    - Researchers
    - Policy makers
    - Communities
    - Industry sectors
    
    Write in a professional, technical tone suitable for researchers, practitioners, and decision-makers.
    Include specific examples, actual tools, and practical guidance.
    Be comprehensive, accurate, and focused on real-world application.
    Make this the definitive reference page for this topic.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a leading expert in wildfire science, fire management, and risk assessment with deep knowledge of operational tools, research methods, and policy applications."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating content for {topic_info['title']}: {str(e)}")
        return None

def create_topic_qmd_file(topic_info, content):
    """Create a Quarto markdown file for a topic"""
    
    qmd_template = f"""---
title: "{topic_info['title']}"
description: "{topic_info['description']}"
date: {datetime.now().strftime('%Y-%m-%d')}
categories: [{topic_info['category']}]
author: "AI Research Assistant - Rallypoint One"
toc: true
toc-depth: 3
---

# {topic_info['title']}

::: {{.callout-important}}
## Topic Overview
**Category**: {topic_info['category']}  
**Focus Areas**: {topic_info['focus']}  
**Last Updated**: {datetime.now().strftime('%B %d, %Y')}
:::

{content}

---

## Related Topics in This Directory

### Related Models and Systems
Browse our comprehensive [model directory](index.qmd) for specific simulation and modeling tools related to this topic.

### Integration Opportunities
This topic integrates with multiple models and systems documented in our directory. See specific model pages for technical integration details.

---

## Contributing to This Page

This page is part of the [Wildfire Simulation & Modeling Research Directory](https://wildfire-directory.netlify.app) maintained by [Rallypoint One](https://rallypoint1.com).

### How You Can Contribute:
- **Share Case Studies**: Document successful applications of these methods
- **Provide Updates**: Submit new tools, research, or methodologies
- **Report Corrections**: Help us maintain accuracy
- **Add Resources**: Share training materials or documentation

**Contact Options:**
- [Open an Issue on GitHub](https://github.com/RallypointOne/wildfire-directory/issues)
- [Contact Rallypoint One](https://rallypoint1.com/contact)
- Email: info@rallypoint1.com

---

## Professional Services

**Rallypoint One** offers consulting services related to {topic_info['category'].lower()}:
- Implementation support
- Custom analysis and modeling
- Training and capacity building
- Risk assessment and planning
- Technology integration

[Learn more about our services](https://rallypoint1.com)

---

*This page was automatically generated using AI-assisted research and is continuously updated to reflect the latest developments in wildfire science and management.*

*Part of the NSF ASCEND Engine Wildfire Research Initiative*
"""
    
    return qmd_template

def create_topics_index():
    """Create an index page for the new topics"""
    
    content = f"""---
title: "Essential Wildfire Topics"
description: "Comprehensive guides to key wildfire science and management topics"
date: {datetime.now().strftime('%Y-%m-%d')}
toc: true
---

# Essential Wildfire Topics

Beyond individual models and systems, these comprehensive guides cover critical topics in wildfire science, management, and risk assessment.

## Topics by Category

### 🔥 Fire Danger and Weather
- [Fire Weather Indices (FWI, FFDI, and Global Systems)](fire-weather-indices.qmd)
- [Climate Change and Future Fire Projections](climate-fire-projections.qmd)

### 🛰️ Detection and Monitoring
- [Satellite Fire Detection and Monitoring Systems](satellite-fire-detection.qmd)
- [Burn Severity Mapping and Assessment](burn-severity-mapping.qmd)

### 🏘️ Risk Assessment
- [Wildland-Urban Interface (WUI) Modeling and Risk](wui-modeling.qmd)
- [Insurance Industry Wildfire Risk Assessment Tools](insurance-risk-tools.qmd)
- [Post-Fire Debris Flow Prediction and Risk](debris-flow-prediction.qmd)

### 🌍 Environmental Impacts
- [Wildfire Carbon Emissions and Climate Impacts](carbon-emissions-modeling.qmd)

### 📚 Management Approaches
- [Indigenous Fire Management and Cultural Burning](indigenous-fire-management.qmd)
- [FARSITE Fire Simulation System - Complete Guide](farsite-system.qmd)

## Why These Topics Matter

These topics represent critical areas of wildfire science and management that:
- Bridge multiple modeling approaches
- Address emerging challenges
- Support decision-making at all levels
- Integrate traditional and modern knowledge
- Enable comprehensive risk assessment

## How to Use These Guides

Each topic page provides:
1. **Comprehensive Overview** - Current state of knowledge
2. **Practical Applications** - Real-world implementation
3. **Tools and Resources** - Specific software and datasets
4. **Case Studies** - Documented examples
5. **Future Directions** - Emerging research and needs

---

*Part of the [Wildfire Research Directory](https://wildfire-directory.netlify.app) by [Rallypoint One](https://rallypoint1.com)*
"""
    
    return content

def update_main_navigation():
    """Generate code to add these topics to the main navigation"""
    
    nav_update = """
## 📚 Essential Topics

Our directory now includes comprehensive guides on critical wildfire topics:

### Fire Danger and Risk
- [Fire Weather Indices (FWI, FFDI)](fire-weather-indices.qmd)
- [WUI Risk Modeling](wui-modeling.qmd)
- [Insurance Risk Assessment](insurance-risk-tools.qmd)

### Detection and Assessment
- [Satellite Fire Detection](satellite-fire-detection.qmd)
- [Burn Severity Mapping](burn-severity-mapping.qmd)
- [Debris Flow Prediction](debris-flow-prediction.qmd)

### Climate and Environment
- [Climate Change Projections](climate-fire-projections.qmd)
- [Carbon Emissions Modeling](carbon-emissions-modeling.qmd)

### Management Approaches
- [Indigenous Fire Management](indigenous-fire-management.qmd)
- [FARSITE Complete Guide](farsite-system.qmd)

[View All Essential Topics](essential-topics-index.qmd)
"""
    
    return nav_update

def main():
    """Generate content for additional wildfire topics"""
    
    print("🔥 Starting Additional Wildfire Topics Content Generation...")
    print(f"📚 Generating {len(ADDITIONAL_TOPICS)} comprehensive topic pages...")
    
    # Check API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("❌ ERROR: OPENAI_API_KEY not found!")
        return 0
    
    generated_files = []
    failed_topics = []
    
    # Generate individual topic pages
    for i, topic in enumerate(ADDITIONAL_TOPICS, 1):
        print(f"\n[{i}/{len(ADDITIONAL_TOPICS)}] 📝 Generating: {topic['title']}...")
        
        content = generate_topic_content(topic)
        
        if content:
            qmd_content = create_topic_qmd_file(topic, content)
            
            with open(topic['filename'], 'w', encoding='utf-8') as f:
                f.write(qmd_content)
            
            generated_files.append(topic['filename'])
            print(f"✅ Successfully created: {topic['filename']}")
        else:
            failed_topics.append(topic['title'])
            print(f"❌ Failed to generate: {topic['title']}")
    
    # Create topics index page
    print("\n📑 Creating Essential Topics index page...")
    index_content = create_topics_index()
    with open('essential-topics-index.qmd', 'w', encoding='utf-8') as f:
        f.write(index_content)
    generated_files.append('essential-topics-index.qmd')
    print("✅ Created essential-topics-index.qmd")
    
    # Generate navigation update
    print("\n📋 Generating navigation update...")
    nav_content = update_main_navigation()
    with open('nav-update.txt', 'w', encoding='utf-8') as f:
        f.write(nav_content)
    print("✅ Created nav-update.txt (add this to your index.qmd)")
    
    # Summary
    print(f"\n✨ Content Generation Complete!")
    print(f"📊 Summary:")
    print(f"  - Successfully generated: {len(generated_files)} files")
    print(f"  - Failed: {len(failed_topics)} topics")
    print(f"  - Total pages created: {len(generated_files)}")
    
    if failed_topics:
        print(f"\n⚠️ Failed topics (can retry):")
        for topic in failed_topics:
            print(f"  - {topic}")
    
    print(f"\n💡 Next steps:")
    print(f"  1. Review generated content")
    print(f"  2. Add navigation from nav-update.txt to index.qmd")
    print(f"  3. Commit and push to GitHub")
    print(f"  4. Site will auto-deploy to Netlify")
    
    # Cost estimate
    cost_estimate = len(ADDITIONAL_TOPICS) * 0.15  # Approximate cost per topic
    print(f"\n💰 Estimated OpenAI API cost: ${cost_estimate:.2f}")
    
    return len(generated_files)

if __name__ == "__main__":
    result = main()
    exit(0 if result > 0 else 1)

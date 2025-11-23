import os
import json
from datetime import datetime
import openai

# Configure OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

# Topics to generate content for
TOPICS = [
    {
        "filename": "wrf-fire.qmd",
        "title": "WRF-Fire Model",
        "category": "Coupled Fire-Atmosphere Models",
        "focus": "weather-coupled wildfire simulation, atmospheric interactions, operational forecasting"
    },
    {
        "filename": "machine-learning.qmd",
        "title": "Machine Learning in Fire Prediction",
        "category": "AI/ML Applications",
        "focus": "neural networks, random forests, deep learning for fire spread prediction"
    },
    {
        "filename": "fuel-moisture.qmd",
        "title": "Fuel Moisture Content Modeling",
        "category": "Fuel Dynamics",
        "focus": "live and dead fuel moisture, remote sensing, prediction models"
    },
    {
        "filename": "smoke-modeling.qmd",
        "title": "Smoke Dispersion and Air Quality",
        "category": "Atmospheric Effects",
        "focus": "smoke plume dynamics, air quality impacts, health effects modeling"
    },
    {
        "filename": "evacuation.qmd",
        "title": "Evacuation Planning and Simulation",
        "category": "Emergency Management",
        "focus": "evacuation routes, traffic simulation, community warning systems"
    }
]

def generate_page_content(topic_info):
    """Generate content for a single topic using OpenAI"""
    
    prompt = f"""
    Create a comprehensive research directory page about {topic_info['title']} for wildfire researchers.
    Category: {topic_info['category']}
    Focus areas: {topic_info['focus']}
    
    Structure the content with these sections:
    1. Overview (2-3 paragraphs explaining the topic and its importance)
    2. Key Concepts (main technical concepts and terminology)
    3. Current Research (latest developments and active research areas)
    4. Software and Tools (specific tools, models, and software packages)
    5. Research Groups and Institutions (major contributors to this field)
    6. Datasets and Resources (available data sources)
    7. Recent Publications (important papers - just titles and brief descriptions)
    8. Challenges and Future Directions
    
    Write in a professional, technical tone suitable for researchers and practitioners.
    Include specific model names, research institutions, and technical details.
    Make the content informative and comprehensive.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert in wildfire modeling and simulation research."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating content for {topic_info['title']}: {str(e)}")
        return None

def create_qmd_file(topic_info, content):
    """Create a Quarto markdown file with the generated content"""
    
    qmd_template = f"""---
title: "{topic_info['title']}"
description: "Comprehensive resource on {topic_info['title'].lower()} in wildfire research"
date: {datetime.now().strftime('%Y-%m-%d')}
categories: [{topic_info['category']}]
author: "AI Research Assistant"
toc: true
---

{content}

---

## How to Contribute

If you have corrections, additions, or suggestions for this page, please:
1. [Open an issue on GitHub](https://github.com/RallypointOne/wildfire-directory/issues)
2. [Contact Rallypoint One](https://rallypoint1.com/contact)

---

*This page was automatically generated using AI-assisted research on {datetime.now().strftime('%B %d, %Y')}. Content is regularly updated to reflect the latest developments in wildfire research.*

*Part of the [Wildfire Research Directory](https://wildfire-directory.netlify.app) by [Rallypoint One](https://rallypoint1.com)*
"""
    
    return qmd_template

def main():
    """Generate content for all topics"""
    
    print("🔥 Starting Wildfire Research Content Generation...")
    print(f"📚 Generating {len(TOPICS)} topic pages...")
    
    generated_files = []
    
    for topic in TOPICS:
        print(f"\n📝 Generating: {topic['title']}...")
        
        # Generate content using AI
        content = generate_page_content(topic)
        
        if content:
            # Create the QMD file
            qmd_content = create_qmd_file(topic, content)
            
            # Write the file
            with open(topic['filename'], 'w', encoding='utf-8') as f:
                f.write(qmd_content)
            
            generated_files.append(topic['filename'])
            print(f"✅ Successfully created: {topic['filename']}")
        else:
            print(f"❌ Failed to generate: {topic['title']}")
    
    # Create an index of generated content
    if generated_files:
        print(f"\n✨ Successfully generated {len(generated_files)} pages!")
        print("\nGenerated files:")
        for file in generated_files:
            print(f"  - {file}")
        
        # Update the index page to include new content
        print("\n📋 Updating index page with new content links...")
        update_index_page(TOPICS, generated_files)
    else:
        print("\n⚠️ No files were generated. Check your OpenAI API key.")
    
    return len(generated_files)

from context import generate_context_queries, generate_onet_title, query_collections
from jd_generation_V2 import main_workflow
from frontend import main_frontend
from typing import List, Dict
from dotenv import load_dotenv
import json, json_repair
import os
import pathlib
from datetime import datetime

load_dotenv('.env', override=True)


def main():   
    
    json_schema_path = "/home/JD_Generation_Optimized/JD_Schema.json"
    with open(json_schema_path, 'r') as file:
        jd_structure = json.load(file)  

    
    user_requirement = """
    *Title: HR Business Partner
    *Experience: 5+ years in HR management, preferably in a similar role
    *Education: Degree in Business Administration, Psychology, International Cultural and Business Studies, or related field
    *HR strategy, workforce planning, succession planning, leadership coaching, labor relations, Employee experience, organizational design, change management
    *General knowledge of HR practices and Austrian labor law
    *Fluent in English (business), conversational in German
    *Tools: Familiarity with Microsoft Office and/or Google Workspace
    """
    
    #list of section to be included in JD
    #write a function to generate this - JD generation
    # inputs - user requirement, list of sections(sections to be included in JD)
    # output - list of sections in a dictionary format with key as section name and content as value
    #SEO TO BE COMMENTED OUT FOR TIME BEING
    
    seo_instructions = """
        Keyword Optimization: Use relevant keywords naturally throughout the job description. ...
        Job Title Clarity: Keep job titles concise and clear. ...
        Structured and Scannable Content: Organize your job description with clear headings. ...
        Rich Snippets and Schema Markup: Implement structured data ...
        Engaging and Honest Content: Write clear, honest, and engaging job descriptions ...
    """
    
    updated_SEO_instructions = {
        "structure": {
            "job_title": {
                "format": "Position - Location/Work Type (if applicable)",
                "requirements": [
                    "Use clear, specific, commonly searched title",
                    "Include role-specific keywords",
                    "Mention location/remote status if relevant"
                ]
            },
            "summary": {
                "format": "2-3 concise sentences",
                "requirements": [
                    "State role's key purpose",
                    "Highlight organizational impact",
                    "Include primary keyword naturally"
                ]
            },
            "company_overview": {
                "format": "2-3 engaging sentences",
                "requirements": [
                    "Company mission and values",
                    "Unique selling points",
                    "Industry position/achievements"
                ]
            },
            "responsibilities": {
                "format": "5-7 bullet points",
                "requirements": [
                    "Start with action verbs",
                    "Include measurable outcomes",
                    "Incorporate role-specific keywords"
                ]
            },
            "qualifications": {
                "format": "Separate required vs preferred",
                "requirements": [
                    "Education requirements",
                    "Years of experience",
                    "Technical skills",
                    "Soft skills",
                    "Certifications if needed"
                ]
            },
            "benefits": {
                "format": "Bulleted list",
                "requirements": [
                    "Highlight unique perks",
                    "Include salary range if possible",
                    "Mention growth opportunities"
                ]
            }
        },
        "seo_guidelines": {
            "keyword_usage": [
                "Include 3-5 primary keywords",
                "Natural keyword placement",
                "Avoid keyword stuffing"
            ],
            "formatting": [
                "Use clear headings (H1, H2, H3)",
                "Short paragraphs (2-3 sentences)",
                "Bullet points for lists",
                "Mobile-friendly layout"
            ],
            "content_best_practices": [
                "Active voice",
                "Inclusive language",
                "Scannable format",
                "Clear call-to-action"
            ]
        },
        "meta_data": {
            "title_tag": "{job_title} - {company_name} - {location}",
            "meta_description": "Join {company_name} as a {job_title}. {key_responsibility} in {location}. {years_experience} required. Apply now!",
            "url_structure": "/careers/{department}/{job-title}-{location}"
        }
    }

    
    company_persona = """
    Humble Bridge is a leading AI/ML company dedicated to driving digital transformation across various industries. ...
    """
    
        
        
    # Step 1: Generate context queries
    job_title = generate_onet_title(user_requirement)
    # Parse the string into a dictionary
    
    try:
        job_title_dict = json.loads(job_title)        
    except Exception as e:
        job_title_dict = json_repair.loads(job_title)        
        
    print("JOB TITLE IS --> " + job_title_dict['onetonline_occupation_title'])
    # Generate Context
    #CHANGE LATER   
    prompts = generate_context_queries(user_requirement, job_title)
    
    # Make sure db_uri is defined in main_updated.py, e.g.
    db_uri = "tcp://localhost:19530"

    # Then pass db_uri to the query_collections function
    collections = ['jds']
    contexts = query_collections(prompts, collections, db_uri)  

    # Main Workflow
    #backend_response, frontend_response = main_workflow(
    #    contexts, user_requirement, jd_structure, seo_instructions, company_persona, job_title
    #)
    
        # Main Workflow call with updated SEO instructions
    backend_response, frontend_response, normalized_content = main_workflow(
        contexts, 
        user_requirement, 
        jd_structure, 
        seo_instructions,  
        company_persona, 
        job_title,
        json.dumps(updated_SEO_instructions, indent=2)
    )

    folder_path = 'Altogether_V3'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get the current timestamp in the desired format
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create filenames for all three outputs
    frontend_filename = os.path.join(folder_path, f"Frontend_{timestamp}.json")
    backend_filename = os.path.join(folder_path, f"Backend_{timestamp}.json")
    normalized_filename = os.path.join(folder_path, f"Normalized_{timestamp}.md")

    # Write the responses to their respective files
    with open(frontend_filename, 'w') as f:
        json.dump(backend_response, f, indent=2)
        
    with open(backend_filename, 'w') as f:
        json.dump(frontend_response, f, indent=2)
        
    # Save the normalized content as markdown
    with open(normalized_filename, 'w') as f:
        f.write(normalized_content)
        
    print("SAVED BACKEND RESPONSE AS -> " + backend_filename)
    print("SAVED FRONTEND RESPONSE AS -> " + frontend_filename)
    print("SAVED NORMALIZED CONTENT AS -> " + normalized_filename)
        
        
        
if __name__ == "__main__":
    main()
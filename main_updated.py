from context import generate_context_queries, generate_onet_title, query_collections
from jd_generation import main_workflow
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
    
    seo_instructions = """
        Keyword Optimization: Use relevant keywords naturally throughout the job description. ...
        Job Title Clarity: Keep job titles concise and clear. ...
        Structured and Scannable Content: Organize your job description with clear headings. ...
        Rich Snippets and Schema Markup: Implement structured data ...
        Engaging and Honest Content: Write clear, honest, and engaging job descriptions ...
    """
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
    backend_response, frontend_response = main_workflow(
        contexts, user_requirement, jd_structure, seo_instructions, company_persona, job_title
    )

    folder_path = 'Altogether_V2'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Get the current timestamp in the desired format
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create the filename with "Frontend" and the timestamp
    filename = os.path.join(folder_path, f"Frontend_{timestamp}.json")
    filename2 = os.path.join(folder_path, f"Backend_{timestamp}.json")

    # Write the final frontend response to the JSON file
    with open(filename, 'w') as f:
        json.dump(backend_response, f, indent=2)
        
    # Write the final frontend response to the JSON file
    with open(filename2, 'w') as f:
        json.dump(frontend_response, f, indent=2)
        
        
    print("SAVED BACKEND RESPONSE AS -> " + filename)
    print("SAVED FRONTEND RESPONSE AS -> " + filename2)
        
        
        
if __name__ == "__main__":
    main()
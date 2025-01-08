from jd_generation_V2 import generate_jd_sections
from typing import List, Dict
from dotenv import load_dotenv
import json
import os

load_dotenv('.env', override=True)

def main():
    # Sample user requirement (using the one from your code)
    user_requirement = """
    *Title: HR Business Partner
    *Experience: 5+ years in HR management, preferably in a similar role
    *Education: Degree in Business Administration, Psychology, International Cultural and Business Studies, or related field
    *HR strategy, workforce planning, succession planning, leadership coaching, labor relations, Employee experience, organizational design, change management
    *General knowledge of HR practices and Austrian labor law
    *Fluent in English (business), conversational in German
    *Tools: Familiarity with Microsoft Office and/or Google Workspace
    """
    
    # List of sections to be included in JD
    sections = [
        "Job Title",
        "Location",
        "Job Type",
        "Salary",
        "Company Name",
        "Job Summary",
        "Responsibilities",
        "Requirements",
        "Preferred Requirements"
    ]
    
    # Generate JD sections
    jd_sections = generate_jd_sections(user_requirement, sections)
    
    # Create output directory if it doesn't exist
    os.makedirs('alternative_V1', exist_ok=True)
    
    # Structure the output
    output_data = {
        "user_req": user_requirement,
        "list_of_sections_included": sections,
        "dict_of_sections_generated": jd_sections
    }
            
    # Save to file
    output_file = os.path.join('alternative_V1', 'jd_output.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main() 
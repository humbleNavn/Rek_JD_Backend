import json
from typing import List, Dict


def get_all_keys(elt):
    try:
        if isinstance(elt,list):
            result = [{key: value for key, value in item.items() } for item in elt]
            keys = [item['Category'] for item in result]

            return keys            
        
        else:
            keys = []
            for key, value in elt.items():
                keys.append(key)
                #if isinstance(value, dict):  # If the value is a dictionary, recurse into it
                    #keys.extend(get_all_keys(value))
            return keys
    except Exception as e:
        print(e)
        print("PROBLEM HERE --->")
        print(elt)

def generate_jd_prompt_for_frontend(full_response): 
    """
    Generates a new prompt to ask the LLM to produce a raw structured job description
    based on the parsed full_response from the previous step.
    The response should be in a specific format with HTML content inside the value field.
    """
    
    keys = get_all_keys(full_response)

    # Create the prompt, including the 'keys' in the Key Guidelines section
    prompt = f"""
    You are an AI Assistant. Based on the structured job details below, generate a **comprehensive and human-readable** job description. 
    You must use **all sections** provided in the structured data to create the full job description, without omitting any section.

    The structured data may contain **various types of sections**, such as job summaries, responsibilities, skills, qualifications, benefits, company information, and more. 
    Each section will have an identifier (the `id`) and its corresponding content (the `value`), which you will format appropriately.

    **DO NOT skip any section**, even if it is an unexpected or custom category. Every section in the `full_response` should be represented in the output, including any additional or non-standard sections.

    The output must strictly follow this format:

    The response should be a list of dictionaries, each containing the following two keys:
    - `id`: A string representing the section identifier (e.g., `summary`, `skills`, `responsibilities`, `requirements`, `location`, or **any custom section names** present in the structured data).
    - `value`: A string of HTML content, which should be the section text formatted with appropriate HTML tags (e.g., `<h3>`, `<p>`, `<ul>`, `<li>`).

    Example format:
    [
        {{
            "id": "section_name_1",
            "value": "<h3>Section Name 1</h3><p>Detailed description or content for section 1 goes here.</p>"
        }},
        {{
            "id": "section_name_2",
            "value": "<h3>Section Name 2</h3><ul><li>Item 1</li><li>Item 2</li></ul>"
        }},
        {{
            "id": "section_name_3",
            "value": "<h3>Section Name 3</h3><p>Content for section 3 goes here.</p>"
        }}
    ]

    **Key Guidelines**:
    - Ensure you **process all sections** in the `full_response` meticulously, formatting each section properly. 
    - Do **NOT skip** any sections even if they are non-standard or unexpected. Every key-value pair in the structured data should be included.
    - Please **focus on only including the sections present** in the structured data, and ensure each section is formatted with the correct HTML tags. Avoid generating any content that is not in the input data.
    - Here are the **sections (keys)** present in the structured data that you need to include: {keys}

    Structured Data:
    {json.dumps(full_response, indent=2)}

    The goal is to ensure that the entire job description is generated, using **all sections** and categories, based on the structured data provided. Each section should be clearly labeled with a heading (`<h3>`) and its content formatted appropriately (list items, paragraphs, etc.).
    """
    return prompt

def generate_additional_jd_prompt(full_response): 
    """
    Generates a new prompt to ask the LLM to produce a raw structured job description
    based on the parsed full_response from the previous step.
    The response should be in a specific format with HTML content inside the value field.
    """
    
    keys = get_all_keys(full_response)

    # Create the prompt, including the 'keys' in the Key Guidelines section
    prompt = f"""
    You are an AI Assistant. Based on the structured job details below, generate a **comprehensive and human-readable** job description. 
    You must use **all sections** provided in the structured data to create the full job description, without omitting any section.

    The structured data may contain **various types of sections**, such as job summaries, responsibilities, skills, qualifications, benefits, company information, and more. 
    Each section will have an identifier (the `id`) and its corresponding content (the `values`), which you will format appropriately.

    **DO NOT skip any section**, even if it is an unexpected or custom category. Every section in the `full_response` should be represented in the output, including any additional or non-standard sections.

    The output must strictly follow this format:

    The response should be a list of dictionaries, each containing the following keys:
    - `id`: A string representing the section identifier (e.g., `summary`, `skills`, `responsibilities`, `requirements`, `location`, or **any custom section names** present in the structured data).
    - `type`: A string representing the type of input field, which should be **checkbox** for every case.
    - `label`: A string representing the label or title of the section.
    - `values`: A list of strings representing the options or choices for the section, if applicable (e.g., options for checkboxes).

    Example format:
    [
        {{
            "id": "Level",
            "type": "checkbox",
            "label": "Level",
            "values": [
                "Python", 
                "Django", 
                "REST APIs", 
                "PostgreSQL", 
                "Docker"
            ]
        }},
        {{
            "id": "Experience",
            "type": "checkbox",
            "label": "Experience",
            "values": [
                "3 years", 
                "5 years", 
                "10+ years"
            ]
        }},
        {{
            "id": "Location",
            "type": "checkbox",
            "label": "Location",
            "values": ["New York", "San Francisco", "Remote"]
        }}
    ]

    **Key Guidelines**:
    - Ensure you **process all sections** in the `full_response` meticulously, formatting each section properly. 
    - Do **NOT skip** any sections even if they are non-standard or unexpected. Every key-value pair in the structured data should be included.
    - Please **focus on only including the sections present** in the structured data, and ensure each section is formatted with the correct HTML tags. Avoid generating any content that is not in the input data.
    - Here are the **sections (keys)** present in the structured data that you need to include: {keys}

    Structured Data:
    {json.dumps(full_response, indent=2)}

    The goal is to ensure that the entire job description is generated, using **all sections** and categories, based on the structured data provided. Each section should be clearly labeled with a heading (`<h3>`) and its content formatted appropriately (list items, paragraphs, etc.).
    """
    return prompt

def main_frontend():
    # Example logic to combine JD and frontend responses
    ...

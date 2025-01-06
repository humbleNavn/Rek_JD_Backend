import json, json_repair
from context import generate_context_queries
from frontend import generate_jd_prompt_for_frontend, generate_additional_jd_prompt
from llm import call_llm
from typing import List, Dict


def generate_job_description(contexts: dict, jd_structure: dict, seo_instructions: str, user_requirement: str, company_persona: str) -> str:
    """Generates a Job Description (JD) in JSON format without the Additional Suggestions section, filling missing data when context is empty."""
    
    # Convert the contexts dictionary to a string, if it's empty provide a default message
    context_str = json.dumps(contexts, indent=2) if contexts else "No additional context available for this job description."
    
    # Start building the prompt
    prompt = f"""
    Generate a comprehensive Job Description (JD) in JSON format based on the user's requirement using all relevant context retrieved from the RAG system. Follow the structure below without including the 'Additional Suggestions' section.

    The JD should adhere to the following JSON structure:

    **JD Structure**:
    ```json
    {json.dumps(jd_structure, indent=2)}
    ```

    **User Requirement**:
    ```{user_requirement}```

    **Context**:
    ```{context_str}```

    **SEO Instructions**: 
    ```{seo_instructions}```

    **Company Persona**: 
    ```{company_persona}```

    Instructions:
    - Fill the provided JD structure with relevant content.
    - If any section lacks data (e.g., Responsibilities, Qualifications), generate content based on the user's requirement, the company persona, and the job type.
    - Ensure the output is in valid JSON format.
    - Avoid duplicating points across sections.
    - Each field in the JD structure should be filled, even if context data is missing.
    - If some fields are missing from the context, fill those fields with content that fits the job description and company persona.

    Please return the generated JD in JSON format.
    """

    # Call the language model (this function will likely be implemented separately)
    return call_llm(prompt)


def generate_additional_suggestions(job_description: dict, contexts: dict) -> str:
    """Generates the 'Additional Suggestions' section based on the generated JD and context."""
    job_description_str = json.dumps(job_description, indent=2)
    context_str = json.dumps(contexts, indent=2)

    prompt = f"""
    Based on the following Job Description (JD) and context, generate the 'Additional Suggestions' section. 
    Ensure that each list (Requirement, Responsibilities, Qualifications, Skills) is prioritized with the most relevant items at the top.

    **Job Description**:
    ```{job_description_str}```

    **Context**:
    ```{context_str}```

    **Additional Suggestions Structure**:
    {{
        "Requirement": [list of min 20],
        "Responsibilities": [list of min 20],
        "Qualifications": [list of min 20],
        "Skills": [list of min 20]
    }}

    Instructions:
    - Prioritize the suggestions based on their relevance to the JD.
    - Use only the provided context for generating suggestions.
    """
    return call_llm(prompt)


def normalize_Backend_Response(jd_backendSchemaResponse: dict, updated_SEO_instructions: str) -> str:
    """
    Converts the JSON-structured JD into a formatted text document following updated SEO guidelines.
    
    Args:
        jd_backendSchemaResponse (dict): The JSON structured job description
        updated_SEO_instructions (str): Updated SEO guidelines in JSON format
    
    Returns:
        str: A formatted string containing the job description in a readable format
    """
    
    jd_content = json.dumps(jd_backendSchemaResponse, indent=2)
    
    prompt = f"""
    Convert the following JSON-structured Job Description into a well-formatted text document.
    
    **Job Description JSON**:
    ```
    {jd_content}
    ```
    
    **SEO Structure and Guidelines**:
    ```
    {updated_SEO_instructions}
    ```
    
    Instructions:
    1. Format each section according to the SEO structure:
       - Job Title: Follow the format "Position with Location or Work Type"
       - Summary: Write 2-3 concise sentences with key purpose and impact
       - Company Overview: Include mission, values, and unique selling points
       - Responsibilities: Create 5-7 bullet points starting with action verbs
       - Qualifications: Separate required vs preferred qualifications
       - Benefits: List unique perks and growth opportunities

    2. Apply SEO best practices:
       - Use specified heading hierarchy (H1, H2, H3)
       - Implement natural keyword placement
       - Create scannable content with bullet points
       - Maintain mobile-friendly formatting
       - Use active voice consistently

    3. Content formatting:
       - Each section should have a clear heading
       - Use bullet points for lists
       - Keep paragraphs short (2-3 sentences)
       - Include a clear call-to-action
       - Maintain professional yet engaging tone

    4. Meta information:
       - Structure the title according to the meta_data format
       - Include all required meta information
       - Follow URL structure guidelines

    Return the formatted job description as a text document, ensuring all sections are properly organized and SEO-optimized according to the provided guidelines.
    """
    
    return call_llm(prompt)


# Main workflow
def main_workflow(contexts: dict, user_requirement: str, jd_structure: str, seo_instructions: str, company_persona: str, job_title: str, updated_SEO_instructions: str):
    # Step 1: Generate the main Job Description
    jd_backendSchema = generate_job_description(contexts, jd_structure, seo_instructions, user_requirement, company_persona)
    try:
        jd_backendSchemaResponse = json.loads(jd_backendSchema)
    except:
        jd_backendSchemaResponse = json_repair.loads(jd_backendSchema)

            
    jd_frontend_Prompt = generate_jd_prompt_for_frontend(jd_backendSchemaResponse)
    
    jd_frontend_response = call_llm(jd_frontend_Prompt)
    try:
        jd_frontend_response = json.loads(jd_frontend_response)
    except:
        jd_frontend_response = json_repair.loads(jd_frontend_response)

    
    #ALTER KEY VALUES FOR FRONTEND - JD SCHEMA
    modified_jd_keys = []
    for item in jd_frontend_response:
        try:
            # Check if the item is a dictionary and contains the 'id' key
            if isinstance(item, dict) and 'id' in item:
                modified_id = item['id'].lower().replace(' ', '_')  # Convert to lowercase and replace spaces with '_'
                item['id'] = modified_id
                modified_jd_keys.append(modified_id)    
            else:
                print(f"Skipping item due to invalid structure: {item}")
        except Exception as e:
            print(f"Error processing item: {e}")
            print(f"FRONTEND_JD {str(jd_frontend_response)}")



    additional_suggestions_backend_prompt = generate_additional_suggestions(jd_structure, contexts)
    #additional_suggestions_backend_response = json.loads(additional_suggestions_backend_prompt)
    
    additional_jd__frontend_prompt = generate_additional_jd_prompt(additional_suggestions_backend_prompt)
    additional_jd__frontend_response = call_llm(additional_jd__frontend_prompt)
    
    try:
        additional_jd__frontend_response = json.loads(additional_jd__frontend_response)
    except:
        additional_jd__frontend_response = json_repair.loads(additional_jd__frontend_response)
        

    
    #ALTER KEY VALUES FOR FRONTEND - ADDITIONAL
    additional_keys = []
    for additional in additional_jd__frontend_response:
        modified_additional = additional['id'].lower()# Convert to lowercase and replace spaces with '_'
        additional_keys.append(modified_additional)
        
        
    # Compare additional_keys with modified_jd_keys and replace
    replaced_additional_keys = []

    for additional_key in additional_keys:
        # Try to find a match in modified_jd_keys
        matched_key = next((item for item in modified_jd_keys if additional_key in item), None)
        
        if matched_key:
            replaced_additional_keys.append(matched_key)  # Replace with the matched key
        else:
            replaced_additional_keys.append(additional_key)  # Keep the original if no match
            
    for i, additional in enumerate(additional_jd__frontend_response):
        # Update the 'id' in additional_Data with the replaced key
        additional['id'] = replaced_additional_keys[i]

    final_response = {
        "title_section": {"title": job_title},
        "jd_format": jd_frontend_response,
        "suggestions": additional_jd__frontend_response,
        "normalized_content": normalize_Backend_Response(jd_backendSchemaResponse, updated_SEO_instructions),
        "meta_data": {
            "title_tag": f"{job_title} - {company_persona}",
            "meta_description": normalize_Backend_Response(jd_backendSchemaResponse, updated_SEO_instructions)[:160] + "...",  # First 160 characters for meta description
            "url_structure": f"/careers/{job_title.lower().replace(' ', '-')}"
        }
    }



    ## Combine the JD with Additional Suggestions
    #job_description["Additional Suggestions"] = additional_suggestions

    # Add the normalized response to the final output
    normalized_jd = normalize_Backend_Response(jd_backendSchemaResponse, updated_SEO_instructions)
    
    final_response["normalized_content"] = normalized_jd
    
    # Return all three responses: frontend, backend, and normalized
    return final_response, jd_backendSchemaResponse, normalized_jd

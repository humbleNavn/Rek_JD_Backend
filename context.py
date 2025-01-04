import json, json_repair
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.milvus import MilvusVectorStore
from typing import List, Dict
from llm import call_llm
from concurrent.futures import ThreadPoolExecutor


def load_index(collection_name: str, db_uri: str = "tcp://localhost:19530", dim: int = 1536) -> VectorStoreIndex:
    """Connects to Milvus and loads the specified index."""
    vector_store = MilvusVectorStore(uri=db_uri, collection_name=collection_name, dim=dim, overwrite=False)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(vector_store=vector_store, storage_context=storage_context)


def query_collections(prompts: Dict[str, str], collections: List[str], db_uri: str) -> List[Dict[str, str]]:
    """Queries the specified collections concurrently with given prompts."""
    results = []

    def run_query(index, collection_name, prompt_key, prompt):
        if prompt:  # Ensure prompt is not empty or None
            print(f"Running query on prompt '{prompt_key}' for collection '{collection_name}'")
            query_engine = index.as_query_engine()
            try:
                response = query_engine.query(prompt)  # Store the full response object
                print(f"Full Response for '{prompt_key}': {response}")  # Print full response for debugging

                # Adjust based on response structure
                if hasattr(response, 'text'):
                    context = response.text
                elif hasattr(response, 'content'):
                    context = response.content  # or any other attribute holding the main content
                else:
                    context = str(response)  # Fallback to string conversion if no clear attribute

                # Add structured result
                results.append({
                    "query": prompt,
                    "collection_name": collection_name,
                    "context": context
                })
            except Exception as e:
                print(f"Error querying with prompt '{prompt_key}': {e}")
                results.append({
                    "query": prompt,
                    "collection_name": collection_name,
                    "context": f"Error: {str(e)}"
                })
        else:
            print(f"Skipping empty prompt '{prompt_key}' for collection '{collection_name}'")
            results.append({
                "query": prompt,
                "collection_name": collection_name,
                "context": "No valid prompt provided."
            })

    # Load indexes for collections
    indexes = {col: load_index(col, db_uri) for col in collections}

    # Run queries concurrently across prompts and collections
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for collection_name, index in indexes.items():
            for prompt_key, prompt in prompts.items():
                futures.append(executor.submit(run_query, index, collection_name, prompt_key, prompt))

        # Collect results as futures complete
        for future in futures:
            future.result()  # Wait for each future to complete

    return results



def generate_onet_title(user_requirement):
    prompt = f"""I need to get the appropriate Occupation title in Onetonline for this requirement ```{user_requirement}```, 
    only reply in string of dictionary with key:value format with the 
    "onetonline_occupation_title", "onet_job_code"
    dont be creative, if you dont know put unknown"""
    res = call_llm(prompt)
    return res

def generate_context_queries(user_requirement: str, title: str) -> Dict[str, str]:
    print(f'User Requirement: {user_requirement}')
    onet_title = title    
    user_requirement = f"""{user_requirement} - {onet_title}"""
    print('Update user Requirement', user_requirement)
    """Generates context extraction prompts based on user requirements."""
    prompt_template = f"""
    Given the job requirements:

    user_requirement: ```{user_requirement}```

    Generate three prompts to extract specific information - structured data as context. The prompts should focus on the following elements:

    Responsibilities: Pull data from Tasks and Work Activities to capture job tasks, core duties, and primary activities for the role.
    Skills: Use information from Skills, Tools & Technology, and Abilities to retrieve essential technical and soft skills required for the position.
    Qualifications: Reference Job Zone, Education, and Knowledge for minimum educational background, experience, certifications, and relevant industry knowledge.
    
    for all the prompts, use the complete user_requirement with onetonline - onet_title and job code if available
    
    Output in JSON format as follows:

    {{
        "prompts": {{
            "Responsibilities": "[Generate a prompt for getting Responsibilities using Tasks and Work Activities based on the user input, make it bullet points (with all possible context min 20 items)]",
            "Skills": "[Generate a prompt for using Skills, Tools & Technology, and Abilities based on the user input, make it bullet points (with all possible context min 20 items)]",
            "Qualifications": "[Generate a prompt for Qualifications using Job Zone, Education, and Knowledge based on the user input, make it bullet points (with all possible context min 20 items)]"
        }}
    }}
    
    Please also make sure you add to each prompt to fetch all possible context which are relevant as a bullet point
    """
    response = call_llm(prompt_template)
    
    print('>>>>> Prompts\n',response)
    
    try:
        return json.loads(response)["prompts"]
    except json.JSONDecodeError:
        print("THE RESPONSE HERE --")
        print(json_repair.loads(response)["prompts"])
        
        return json_repair.loads(response)["prompts"]


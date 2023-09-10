import openai
import os

class Arguments:
    
    openai.api_key = os.getenv("OPENAI_API_KEY") # OpenAPIKey
    temp = 0.5
    map_custom_prompt = "Prompts/map_custom_prompt.txt" # Enter your map_custom_prompt file path here
    combine_custom_prompt = "Prompts/combine_custom_prompt.txt" # Enter your combine_custom_prompt file path here

    #Enter the path of the document here
    document_path = "/Users/badarshaban/Downloads/crime-and-punishment.pdf"
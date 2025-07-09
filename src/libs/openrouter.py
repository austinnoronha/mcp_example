import requests
import json
from src.utils.config import OPEN_ROUTER_API_KEY


def ask_model(user_prompt: str):
    """
    Build a prompt with a Custom Prompt.

    Args:
        user_prompt (str): The main user prompt/content.
        
    Returns:
        str: The assistant's response content, or None if an error occurs.
    """
    
    # Plain text system message with \n for newlines (not Markdown)
    system_message = (
        "You are an expert project assistant. Build my project with best coding practices.\n"
        "My Project Information and Context on Technology: \n"
        f"{user_prompt}"+"\n"
        "Folder structure modular design: \n"
        "├── app/ \n"
        "│   ├── core/               # Configs, utils, security \n"
        "│   ├── api/                # FastAPI routes \n"
        "│   ├── models/             # Pydantic/SQLAlchemy models \n"
        "│   ├── tasks/              # Celery tasks \n"
        "│   └── main.py             # FastAPI app entrypoint \n"
        "├── tests/                  # Pytest tests (API, tasks, etc.) \n"
        "├── .env                   # Environment variables \n"
        "├── requirements.txt       # Dependencies \n"
        "├── docker-compose.yml     # Redis + App + Worker setup (optional) \n"
        "└── README.md              # Setup Readme with basic information about the project \n"
        "Start by creating the our project.toml file. (if not present) \n "
        "Run the cmd on the terminal to intialize it.\n"
        "Next create venv and poetry with its.\n"
        "Next please create the folder strcuture and files. Try to create __init__.py file.\n"
        "Note: when I ask to create code/function/class try to use best industry standards \n",
        "of that technology specified and add enough documentation to the respective file/function/code.\n"
    )
    
    return system_message
    
# def ask_openrouter_model(user_prompt: str):
#     """
#     Sends a prompt to the OpenRouter model, prepending a system message to guide the model's behavior.

#     Args:
#         user_prompt (str): The main user prompt/content.
        
#     Returns:
#         str: The assistant's response content, or None if an error occurs.
#     """
    
#     # Plain text system message with \n for newlines (not Markdown)
#     system_message = (
#         "You are an expert project assistant. Think step by step, clarify requirements, "
#         "and transform the user's request into a clear, actionable project prompt for Coding Agent. "
#         "Be concise, practical, and include best practices.\n"
#         "The response MUST start with: \n"
#         "You are a trained expert in the skillset mentioned by the user prompt.\n"
#         "Now help me build a project...\n"
#         "with ...\n"
#         "Folder structure ...\n"
#         "Now lets start by creating the our project.toml file. Run the cmd on the terminal to intialize it.\n"
#         "Next we can create venv and poetry with its.\n"
#         "Next please create the folder strcuture and files. Try to create __init__.py file.\n"
#         "Note: when I ask to create code/function/class try to use best industry standards \n",
#         "of that technology specified and add enough documentation to the respective file/function/code.\n"
#         "Do not use Markdown formatting. Use plain text and separate sections with newlines."
#     )
        
#     try:
#         response = requests.post(
#             url="https://openrouter.ai/api/v1/chat/completions",
#             headers={
#                 "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
#                 # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
#                 # "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
#             },
#             data=json.dumps(
#                 {
#                     # "model": "openai/gpt-4o", # Optional
#                     "model": "deepseek/deepseek-r1:free",
#                     "messages": [
#                         {"role": "system", "content": system_message},
#                         {"role": "user", "content": user_prompt}
#                     ],
#                 }
#             ),
#         )
#         response.raise_for_status()
#         data = response.json()
#         # Try to extract the assistant's message content
#         try:
#             content = data['choices'][0]['message']['content']
#             print("[SUCCESS] Assistant's response:")
#             print(content)
#             return content
#         except (KeyError, IndexError, TypeError) as parse_err:
#             print(f"[ERROR] Could not parse assistant's response: {parse_err}")
#             print("Full response:", data)
#     except requests.exceptions.RequestException as e:
#         print(f"[ERROR] Request failed: {e}")
#     except Exception as ex:
#         print(f"[ERROR] Unexpected error: {ex}")

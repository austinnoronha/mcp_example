import requests
import json
from src.utils.config import OPEN_ROUTER_API_KEY


def main():
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPEN_ROUTER_API_KEY}",
                # "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                # "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
            data=json.dumps(
                {
                    # "model": "openai/gpt-4o", # Optional
                    "model": "deepseek/deepseek-r1:free",
                    "messages": [
                        {"role": "user", "content": "What is the meaning of life?"}
                    ],
                }
            ),
        )
        response.raise_for_status()
        data = response.json()
        # Try to extract the assistant's message content
        try:
            content = data['choices'][0]['message']['content']
            print("[SUCCESS] Assistant's response:")
            print(content)
        except (KeyError, IndexError, TypeError) as parse_err:
            print(f"[ERROR] Could not parse assistant's response: {parse_err}")
            print("Full response:", data)
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
    except Exception as ex:
        print(f"[ERROR] Unexpected error: {ex}")


if __name__ == "__main__":
    main()

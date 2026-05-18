import requests
import json
import os
import sys

CONFIG_PATH = "config.json"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: '{CONFIG_PATH}' missing. Please copy 'config.json.template' to '{CONFIG_PATH}'.")
        sys.exit(1)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def query_agent(prompt_type, market_data, portfolio_data):
    config = load_config()
    
    # Highly structured system prompt using explicit delimiters
    system_instruction = (
        "You are an Elite Portfolio Management AI Engine. You must follow these constraints:\n"
        "1. Be blunt, technical, and hyper-decisive.\n"
        "2. Do not include any conversational fluff, greetings, intro lines, or sign-offs.\n"
        f"3. Filter and skew all insights to match the user's background: {config['field_of_work']}.\n"
        f"4. Integrate 1 relevant tip/formula for their competitive exam: {config['competitive_exam']} targeting {config['target_colleges']}."
    )
    
    # Clean template routing
    if prompt_type == "opening_30m":
        user_prompt = (
            f"<market_data>\n{market_data}\n</market_data>\n"
            "Task: Generate a sharp 30-minute post-open market analysis summary. Include 1 intense math or operational management tip for the CAT exam."
        )
    elif prompt_type == "recommend":
        user_prompt = (
            f"<screened_assets>\n{market_data}\n</screened_assets>\n"
            "Task: Select exactly 1 Large-cap, 1 Mid-cap, and 1 Small-cap asset from the screened list. Write exactly one technical sentence for each explaining its investment entry trigger."
        )
    elif prompt_type == "midday":
        user_prompt = (
            f"<portfolio>\n{portfolio_data}\n</portfolio>\n"
            f"<market_conditions>\n{market_data}\n</market_conditions>\n"
            "Task: Provide an immediate execution command: MAINTAIN positions or PARTIAL LIQUIDATION. Give a 1-sentence analytical reason."
        )
    elif prompt_type == "closing":
        user_prompt = (
            f"<portfolio>\n{portfolio_data}\n</portfolio>\n"
            f"<market_conditions>\n{market_data}\n</market_conditions>\n"
            "Task: Provide an End-of-Day ledger summary and state a definitive instruction for overnight holding or position exits."
        )

    # Use standard Ollama generation payload structure
    payload = {
        "model": config.get("ollama_model", "llama3"),
        "system": system_instruction,
        "prompt": user_prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,  # Lower temperature prevents the model from stalling out or hallucinating
            "top_p": 0.9
        }
    }
    
    try:
        res = requests.post(config.get("ollama_url"), json=payload, timeout=180)
        output_text = res.json().get("response", "").strip()
        
        # Fallback tracking if Ollama still gives us a completely blank output string
        if not output_text:
            return "Agent System Alert: Local LLM returned a blank inference response string. Check memory constraints."
        return output_text
        
    except requests.exceptions.Timeout:
        return "Local Engine Timeout: Ollama processing boundary limit reached."
    except Exception as e:
        return f"Inference Interface Error: {e}"

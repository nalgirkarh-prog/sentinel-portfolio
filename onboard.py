import json
import os

PROFILE_PATH = "data/profile.json"

def run_onboarding():
    os.makedirs("data", exist_ok=True)
    if os.path.exists(PROFILE_PATH):
        return json.load(open(PROFILE_PATH))
        
    print("\033[94m🏎️ [Agentic AI Initialization Input Required]\033[0m")
    field = input("What is your field of work/study? ")
    exam = input("What competitive exam are you planning for? ")
    colleges = input("What are your target colleges through the exam? ")
    
    profile = {
        "field_of_work": field,
        "competitive_exam": exam,
        "target_colleges": colleges
    }
    
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=4)
    print("\033[92mProfile logged securely to hardware. Initializing engine...\033[0m\n")
    return profile

if __name__ == "__main__":
    run_onboarding()

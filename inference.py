import os
import json
import textwrap
from openai import OpenAI
from models import SmartTrafficEnv, TrafficAction

# Load environment variables configured in PowerShell or .env
API_BASE_URL = os.environ.get("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.environ.get("HF_TOKEN")

# Initialize the client using the Hugging Face router
client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def main():
    # Initialize your custom environment
    env = SmartTrafficEnv()
    task = "easy"
    
    print("[START]")
    print(f"[STEP] task={task}")
    
    # Safely handle the reset state
    state_obj = env.reset(task)
    state = state_obj.model_dump() if hasattr(state_obj, "model_dump") else state_obj.dict() if hasattr(state_obj, "dict") else state_obj
    
    total_reward = 0.0
    
    # Run the evaluation loop for up to 50 steps
    for step in range(1, 51):
        # Format the system prompt instructions for the LLM
        system_prompt = textwrap.dedent("""
            You are an AI controlling a smart traffic intersection.
            You are given the current queues at North, South, East, and West, and emergency vehicle status.
            You must output ONLY a valid JSON object representing your action.
            The action has a single key 'signal_phase'. Use 0 for North-South green, or 1 for East-West green.
            Example:
            {"signal_phase": 0}
        """).strip()
        
        user_prompt = f"Current state: {json.dumps(state)}"
        
        try:
            # Ask the model for the next action
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=50,
                temperature=0.0
            )
            
            # Extract and clean the JSON response
            reply = response.choices.message.content.strip()
            if reply.startswith("```json"):
                reply = reply.replace("```json", "").replace("```", "").strip()
            elif reply.startswith("```"):
                reply = reply.replace("```", "").strip()
                
            action_data = json.loads(reply)
            action_value = int(action_data.get("signal_phase", 0))
            
        except Exception as e:
            # Fallback to 0 if the model hallucinates formatting
            action_value = 0
        
        # Convert action to Pydantic model and take a step
        action = TrafficAction(signal_phase=action_value)
        result = env.step(action)
        
        # FIX: Extract data using dot notation so Pydantic doesn't throw a TypeError
        reward = result.reward
        done = result.done
        next_state_obj = result.observation
        
        # Prepare state for the next LLM prompt
        state = next_state_obj.model_dump() if hasattr(next_state_obj, "model_dump") else next_state_obj.dict() if hasattr(next_state_obj, "dict") else next_state_obj
        total_reward += reward
        
        # Output exactly the logging format you need
        print(f"[STEP] step={step} action={action_value} reward={reward:.3f}")
        
        if done:
            print(f"[DONE] Total Reward: {total_reward:.3f}")
            break

if __name__ == "__main__":
    main()
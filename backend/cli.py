import sys
import os

# Ensure the backend folder is in the Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from agents.salon_agent import SalonAgent

def main():
    print("Initializing LuxeGlow Salon Assistant...")
    try:
        agent = SalonAgent()
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return
        
    print("\n--- LuxeGlow Salon Terminal Assistant ---")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.strip().lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if not user_input.strip():
                continue
                
            reply = agent.chat(user_input)
            print(f"\nLuxeGlow: {reply}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    main()

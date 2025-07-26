import logging
from src.services import process_human_message

# Configure logging for testing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    # Test the agent with a sample message
    test_data = {
        "lead": {
            "name": "Jane Doe",
            "email": "jane@example.com"
        },
        "message": "Hi, is a 2‑bedroom available in Oakwood Village and do you allow cats?",
        "preferences": {
            "bedrooms": 2,
            "move_in": "2025‑07‑01"
        },
        "community_id": "oakwood-village"
    }
    
    result = process_human_message(test_data)
    
    print("=== AGENT TEST RESULT ===")
    print(f"Reply: {result['reply']}")
    print(f"Action: {result['action']}")
    print(f"Proposed Time: {result['proposed_time']}")
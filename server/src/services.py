import logging
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from src.tools import check_availability, check_pet_policy, get_pricing, propose_tour, ask_clarification, handoff_human
from src.repository import MessageRepository
from src.models import MessageType


load_dotenv()

logger = logging.getLogger(__name__)


def create_agent():
    """Create and configure the agent"""
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        anthropic_api_key=anthropic_api_key,
    )

    agent_tools = [check_availability, check_pet_policy, get_pricing, propose_tour, ask_clarification, handoff_human]
    
    system_prompt = SystemMessage(
        """
        You are a friendly leasing agent helping potential tenants find their perfect home.
        
        Your responses should be:
        - In first person (use "I", "we", "our")
        - Conversational and welcoming
        - Direct and specific about availability and policies
        - Include the person's name when addressing them
        - Mention specific details like unit numbers, pet fees, and availability dates
        - Write in brief conversational paragraphs (no numbered lists)
        
        DECISION MAKING:
        After gathering information, you MUST use one of these decision tools:
        
        1. PROPOSE TOUR: Use propose_tour when you have:
           - Confirmed availability of a unit
           - Lead's name and preferences
           - Unit details (bedrooms, community, availability date)
           - The lead seems interested and ready to see the property
        
        2. ASK CLARIFICATION: Use ask_clarification when:
           - The lead's request is ambiguous
           - Missing key details (move-in date, budget, specific preferences)
           - Need more information to provide accurate assistance
        
        3. HANDOFF HUMAN: Use handoff_human when:
           - No units are available in requested criteria
           - Complex requests that require human expertise
           - Special circumstances or exceptions needed
           - Lead requests to speak with a human
           - After providing information about unavailable units, offer to connect with human agent
        
        IMPORTANT: You MUST use one of these decision tools at the end of your response. Do not just provide information without making a decision.
        
        Example tone: "Hi Jane! Unit 12B is available and cats are welcome (one-time $50 fee). Tours are open this Saturday 10 am–2 pm—does 11 am work?"
        
        Keep responses concise, conversational and brief. Avoid numbered lists or bullet points.
        Use the tools provided to get accurate information about availability, pet policies, and pricing.
        Do not make up any information - only use what the tools provide.
        """
    )
    
    agent_graph = create_react_agent(
        model=llm,
        tools=agent_tools,
        prompt=system_prompt,
    )
    
    return agent_graph


def process_human_message(request_data: dict) -> dict:
    """
    Process a human message through the agent and return the result
    
    Args:
        request_data: Dictionary containing lead, message, preferences, and community_id
        
    Returns:
        dict: The agent's response with messages and any tool call results
    """
    try:
        # Extract data from request
        lead = request_data.get("lead", {})
        message = request_data.get("message", "")
        preferences = request_data.get("preferences", {})
        community_id = request_data.get("community_id", "")
        
        # Log lead information
        logger.info("Processing lead inquiry", extra={
            "lead_name": lead.get("name"),
            "lead_email": lead.get("email"),
            "community_id": community_id,
            "bedrooms": preferences.get("bedrooms"),
            "move_in_date": preferences.get("move_in"),
            "user_message": message
        })
        
        # Create a more specific prompt for the agent using the structured data
        enhanced_message = f"""
        Lead: {lead.get('name', 'Unknown')} ({lead.get('email', 'No email')})
        Community: {community_id}
        Preferences: {preferences.get('bedrooms', 'Unknown')} bedrooms, move-in: {preferences.get('move_in', 'Unknown')}
        Message: {message}
        
        Please check availability for {preferences.get('bedrooms', '')} bedroom apartments in {community_id} and provide information about pet policies.
        """
        
        # Create agent
        agent_graph = create_agent()
        
        inputs = {
            "messages": [HumanMessage(content=enhanced_message)],
            "is_last_step": False,
            "remaining_steps": 10
        }
        
        result = agent_graph.invoke(inputs)
        
        # Log all messages to see tool calls
        logger.info(f"Agent returned {len(result['messages'])} messages")
        for i, message in enumerate(result['messages']):
            logger.info(f"Message {i}: {message.content[:200]}...")
            logger.info(f"Message {i} type: {type(message)}")
            logger.info(f"Message {i} attributes: {dir(message)}")
            if hasattr(message, 'tool_calls') and message.tool_calls:
                logger.info(f"Message {i} has tool calls: {message.tool_calls}")
            elif hasattr(message, 'additional_kwargs') and message.additional_kwargs:
                logger.info(f"Message {i} additional_kwargs: {message.additional_kwargs}")
            elif hasattr(message, 'tool_call_id'):
                logger.info(f"Message {i} tool_call_id: {message.tool_call_id}")
        
        # Extract the final message content and check for tool calls
        final_message = result['messages'][-1].content
        
        # Handle case where content might be empty or not a string
        if not final_message or not isinstance(final_message, str):
            # Look for the last message with actual content
            for message in reversed(result['messages']):
                if message.content and isinstance(message.content, str):
                    final_message = message.content
                    break
            else:
                final_message = "I'm sorry, I couldn't process your request properly."
        
        action = ""
        proposed_time = ""
        
        # Check all messages for tool calls to extract action information
        for message in result['messages']:
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    if tool_call.get('name') in ['propose_tour', 'ask_clarification', 'handoff_human']:
                        try:
                            # Tool call args are already a dict, not JSON string
                            tool_args = tool_call.get('args', {})
                            if tool_call.get('name') == 'propose_tour':
                                action = "propose_tour"
                                # Extract tour slots from the tool result
                                tool_result = json.loads(tool_call.get('output', '{}'))
                                if 'tour_slots' in tool_result:
                                    proposed_time = ", ".join(tool_result['tour_slots'])
                                else:
                                    proposed_time = "11:00 AM, 2:00 PM"  # Default fallback
                            elif tool_call.get('name') == 'ask_clarification':
                                action = "ask_clarification"
                            elif tool_call.get('name') == 'handoff_human':
                                action = "handoff_human"
                        except Exception as e:
                            logger.error(f"Error parsing tool call: {e}")
                            pass
        
        logger.info("Agent processed message", extra={
            "lead_name": lead.get("name"),
            "community_id": community_id,
            "final_response": final_message,
            "message_count": len(result['messages']),
            "action": action
        })
        
        # Persist messages to database
        message_repo = MessageRepository()
        from src.session import get_session
        session_gen = get_session()
        with next(session_gen) as session:
            # Persist the human message (original user message)
            human_message = message_repo.create_human_message(session, request_data.get("message", ""))
            logger.info(f"Persisted human message with ID: {human_message.id}")
            
            # Persist the AI response (final message content)
            ai_message = message_repo.create_ai_message(session, final_message)
            logger.info(f"Persisted AI message with ID: {ai_message.id}")
        
        # Clean up the message by replacing newlines with spaces
        cleaned_message = final_message.replace('\n', ' ').strip()
        
        response = {
            "reply": cleaned_message,
            "action": action
        }
        
        if action == "propose_tour":
            response["proposed_time"] = proposed_time
        
        return response
        
    except Exception as e:
        logger.error(f"Agent processing failed: {e}", exc_info=True)
        return {
            "reply": "I'm sorry, I encountered an error while processing your request. Please try again.",
            "action": "",
            "proposed_time": ""
        } 
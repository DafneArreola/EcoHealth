from typing import Dict, Any, List
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

class TalkTuahUs:
    """
    Standalone motivational chat feature that provides authentic, empathetic guidance
    for users on their eco-health journey.
    """
    def __init__(self):
        self.client = self._init_openai()
        self.conversation_history = []

    def _init_openai(self) -> OpenAI:
        """Initialize OpenAI client"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        return OpenAI(api_key=api_key)

    def _get_system_prompt(self) -> str:
        """Get the system prompt that defines Tuah-us's personality"""
        return """You are Tuah-us, a peer mentor who helps others find their inner strength and purpose.
        
Key aspects of your personality:
- You're authentic and real, speaking from a place of shared experience
- You acknowledge struggles while gently guiding toward growth
- You remind people they're exactly where they need to be
- You emphasize how small steps and consistent effort lead to meaningful change
- You help people see their own potential and worth
- You validate feelings while encouraging forward momentum

Your responses should:
1. Acknowledge their feelings without judgment
2. Share relatable perspectives (like overcoming self-doubt)
3. Remind them of their impact and potential
4. Offer gentle, practical guidance
5. Keep an authentic, peer-like tone
6. End with a thought-provoking question or gentle call to action

Important: Keep responses concise (2-3 paragraphs max) and conversational."""

    def get_response(self, message: str) -> Dict[str, Any]:
        """
        Get response from Tuah-us. Returns formatted response with status and message.
        """
        try:
            messages = [
                {"role": "system", "content": self._get_system_prompt()},
                *self.conversation_history[-4:],  # Keep last 4 messages for context
                {"role": "user", "content": message}
            ]

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=300
            )

            # Update conversation history
            self.conversation_history.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": response.choices[0].message.content}
            ])

            return {
                'status': 'success',
                'response': response.choices[0].message.content,
                'message_type': 'motivation'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'message_type': 'error'
            }

    def get_suggested_prompts(self) -> List[str]:
        """Get conversation starters"""
        return [
            "I'm doubting if I belong in this space...",
            "Sometimes I feel like my efforts aren't enough...",
            "How do I stay motivated when things get tough?",
            "I want to make a difference but don't know where to start...",
            "How do I balance personal growth with helping others?",
            "I'm worried my small changes don't matter..."
        ]

    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []

def test_tuahus():
    """Test the Talk Tuah-us feature"""
    try:
        # Initialize TalkTuahUs
        tuahus = TalkTuahUs()
        
        # Get and display suggested prompts
        print("\n=== Suggested Conversation Starters ===")
        prompts = tuahus.get_suggested_prompts()
        for i, prompt in enumerate(prompts, 1):
            print(f"{i}. {prompt}")
        
        # Test conversation flow
        print("\n=== Testing Conversation Flow ===")
        messages = [
            "I'm trying to make positive changes in my life, but sometimes it feels overwhelming...",
            "You're right. I should focus on one step at a time. But how do I know if I'm making a difference?",
            "That makes sense. I guess I need to trust the process and celebrate small wins."
        ]
        
        for message in messages:
            print(f"\nUser: {message}")
            response = tuahus.get_response(message)
            
            if response['status'] == 'success':
                print(f"\nTuah-us: {response['response']}")
            else:
                print(f"\nError: {response['message']}")
        
        return "Tests completed successfully!"
        
    except Exception as e:
        return f"Test failed: {str(e)}"

if __name__ == "__main__":
    result = test_tuahus()
    print(f"\n{result}")
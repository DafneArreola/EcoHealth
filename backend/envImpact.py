from typing import Dict, Any
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

class EnvironmentalImpact:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    def get_quick_insight(self, data_point: Dict[str, Any]) -> str:
        """
        Get a quick environmental impact insight based on a single data point.
        Returns a short, impactful phrase.
        """
        try:
            # Create a simple prompt focusing on the specific data point
            prompt = f"""Given this environmental data point:
            {data_point}
            
            Provide a single SHORT, impactful phrase (max 15 words) about its environmental impact.
            Focus on either industry effect or environmental consequence.
            Be direct and specific.
            Don't use phrases like "Your" or "You're" - keep it general and fact-focused."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a concise environmental analyst. Provide short, direct impact statements."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=60  # Keep it very short
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error analyzing impact: {str(e)}"

    def get_multi_point_insight(self, data_points: Dict[str, Any]) -> str:
        """
        Get a quick environmental impact insight based on multiple data points.
        Returns a short, impactful phrase.
        """
        try:
            prompt = f"""Given these environmental data points:
            {data_points}
            
            Provide a single SHORT, impactful phrase (max 15 words) about their combined environmental impact.
            Focus on either industry effect (good or bad) or environmental consequence.
            Be direct and specific."""

            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a concise environmental analyst. Provide short, direct impact statements based on user data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=60  # Keep it very short
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error analyzing impact: {str(e)}"
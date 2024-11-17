# ecohealth_cli.py
import json
import os
from datetime import datetime
import openai

class EcoHealthCLI:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_API_KEY')
        if not self.openai_key:
            print("Warning: OpenAI API key not found in environment variables.")
            self.openai_key = input("Please enter your OpenAI API key: ")
        openai.api_key = self.openai_key
        
        self.user_data = {
            "environmental_data": {
                "transportation": {},
                "diet": {},
                "consumption": {}
            },
            "health_data": {}
        }

    def calculate_transport_emissions(self, miles_per_day):
        """Calculate yearly CO2 emissions from transportation"""
        co2_per_mile = 0.411
        return round(miles_per_day * 365 * co2_per_mile, 2)

    def calculate_dietary_impact(self, diet_choices):
        """Calculate dietary environmental impact score"""
        impact_scores = {
            "high": 8,
            "medium": 5,
            "low": 2
        }
        return impact_scores.get(diet_choices.lower(), 2)

    def evaluate_consumption(self, zero_waste_efforts):
        """Evaluate waste reduction efforts"""
        return len(zero_waste_efforts) * 2

    def get_chatgpt_analysis(self, data):
        """Get analysis from ChatGPT"""
        try:
            prompt = f"""
            Analyze this user's environmental impact based on the following:
            - CO2 emissions from transportation: {data['co2_emissions']} kg CO2/year
            - Dietary environmental impact: {data['dietary_impact']} (scale of 1-10)
            - Waste reduction score: {data['waste_score']} (scale of 1-10)

            Provide specific, actionable recommendations for improvement.
            """
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=200
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Error generating recommendations: {str(e)}"

    def collect_transportation_data(self):
        """Collect transportation data from user"""
        print("\n=== Transportation Data ===")
        try:
            miles = float(input("Average miles driven per day: "))
            transport_type = input("Primary mode of transportation (car/public/bike/walk): ")
            
            self.user_data["environmental_data"]["transportation"] = {
                "miles_per_day": miles,
                "primary_mode": transport_type
            }
            
            return self.calculate_transport_emissions(miles)
        except ValueError:
            print("Please enter a valid number for miles.")
            return 0

    def collect_diet_data(self):
        """Collect diet data from user"""
        print("\n=== Diet Information ===")
        print("Red meat consumption level:")
        print("1. High (daily)")
        print("2. Medium (2-3 times per week)")
        print("3. Low (once a week or less)")
        
        choice = input("Select your consumption level (1-3): ")
        levels = {"1": "high", "2": "medium", "3": "low"}
        diet_level = levels.get(choice, "low")
        
        self.user_data["environmental_data"]["diet"] = {
            "red_meat_consumption": diet_level,
            "dietary_preferences": {"red_meat": diet_level}
        }
        
        return self.calculate_dietary_impact(diet_level)

    def collect_consumption_data(self):
        """Collect consumption and waste data"""
        print("\n=== Consumption & Waste ===")
        print("Enter your zero-waste efforts (comma-separated):")
        print("Examples: reusable bags, water bottle, composting, bulk shopping")
        
        efforts = input("> ").split(',')
        efforts = [e.strip() for e in efforts if e.strip()]
        
        self.user_data["environmental_data"]["consumption"] = {
            "zero_waste_efforts": efforts
        }
        
        return self.evaluate_consumption(efforts)

    def save_results(self, analysis):
        """Save results to a JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ecohealth_analysis_{timestamp}.json"
        
        results = {
            "user_data": self.user_data,
            "analysis": analysis,
            "timestamp": timestamp
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {filename}")

    def run_analysis(self):
        """Main analysis flow"""
        print("\nWelcome to EcoHealth Analysis Terminal Version!")
        print("============================================")
        
        # Collect data
        co2_emissions = self.collect_transportation_data()
        dietary_impact = self.collect_diet_data()
        waste_score = self.collect_consumption_data()
        
        # Prepare analysis data
        analysis_data = {
            "co2_emissions": co2_emissions,
            "dietary_impact": dietary_impact,
            "waste_score": waste_score
        }
        
        # Get ChatGPT analysis
        print("\nGenerating analysis and recommendations...")
        chatgpt_analysis = self.get_chatgpt_analysis(analysis_data)
        
        # Display results
        print("\n=== Analysis Results ===")
        print(f"CO2 Emissions: {co2_emissions} kg CO2/year")
        print(f"Dietary Impact Score: {dietary_impact}/10")
        print(f"Waste Reduction Score: {waste_score}/10")
        print("\n=== Recommendations ===")
        print(chatgpt_analysis)
        
        # Save results
        save = input("\nWould you like to save these results? (y/n): ")
        if save.lower() == 'y':
            self.save_results({
                "metrics": analysis_data,
                "recommendations": chatgpt_analysis
            })

def main():
    cli = EcoHealthCLI()
    cli.run_analysis()

if __name__ == "__main__":
    main()
from flask import Flask, request, jsonify
import openai

app = Flask(EcoHealth)

# Set your ChatGPT API key
openai.api_key = "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"

# Route to evaluate environmental impact
@app.route('/environmental_impact', methods=['POST'])
def environmental_impact():
    user_data = request.json

    # Parse user data
    transportation = user_data.get("environmental_data", {}).get("transportation", {})
    diet = user_data.get("environmental_data", {}).get("diet", {})
    consumption = user_data.get("environmental_data", {}).get("consumption", {})
    health = user_data.get("health_data", {})

    # Sample calculations
    co2_emissions = calculate_transport_emissions(transportation)
    dietary_impact = calculate_dietary_impact(diet)
    waste_reduction_score = evaluate_consumption_patterns(consumption)

    # Generate chatbot response
    prompt = f"""
    Analyze this user's environmental impact based on the following:
    - CO2 emissions from transportation: {co2_emissions} kg CO2/year
    - Dietary environmental impact: {dietary_impact} (scale of 1-10)
    - Waste reduction efforts: {waste_reduction_score} (scale of 1-10)

    Provide personalized feedback and actionable recommendations.
    """
    chat_response = generate_chatgpt_response(prompt)

    return jsonify({"analysis": {
        "co2_emissions": co2_emissions,
        "dietary_impact": dietary_impact,
        "waste_reduction_score": waste_reduction_score,
        "chatbot_response": chat_response
    }})

def calculate_transport_emissions(transportation):
    # Example calculation for transportation emissions
    miles_per_day = transportation.get("miles_per_day", 0)
    co2_per_mile = 0.411  # Average CO2 emissions per mile for a gas vehicle
    return round(miles_per_day * 365 * co2_per_mile, 2)

def calculate_dietary_impact(diet):
    # Example dietary impact calculation
    red_meat = diet.get("dietary_preferences", {}).get("red_meat", "low")
    if red_meat == "high":
        return 8
    elif red_meat == "medium":
        return 5
    else:
        return 2

def evaluate_consumption_patterns(consumption):
    # Example scoring for waste reduction
    zero_waste_efforts = consumption.get("zero_waste_efforts", [])
    return len(zero_waste_efforts) * 2  # Example scoring logic

def generate_chatgpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True)

    

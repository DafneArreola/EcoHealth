from typing import Dict, Any
import json
from datetime import datetime
import copy

class DigitalTwin:
    """
    Digital Twin core class that maintains user's health and environmental state
    and provides simulation capabilities.
    """
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.current_state = {
            'environmental': {
                'transportation': {
                    'score': 0,
                    'key_factors': []
                },
                'diet': {
                    'score': 0,
                    'key_factors': []
                },
                'consumption': {
                    'score': 0,
                    'key_factors': []
                },
                'overall_score': 0
            },
            'health': {
                'exercise': {
                    'score': 0,
                    'key_factors': []
                },
                'sleep': {
                    'score': 0,
                    'key_factors': []
                },
                'wellness': {
                    'score': 0,
                    'key_factors': []
                },
                'overall_score': 0
            },
            'combined_score': 0,
            'carbon_footprint': 0,
            'last_updated': None
        }
    
    def update_state(self, new_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update Digital Twin state with new data"""
        try:
            # Calculate carbon footprint first
            self.current_state['carbon_footprint'] = self.calculate_carbon_footprint(new_data)
            
            # Process environmental data
            if 'environmental' in new_data:
                self._process_environmental(new_data['environmental'])
            
            # Process health data
            if 'health' in new_data:
                self._process_health(new_data['health'])
            
            # Calculate combined score
            self._calculate_combined_score()
            
            # Update timestamp
            self.current_state['last_updated'] = datetime.now().isoformat()
            
            # Save state (in a real implementation, this would persist to a database)
            self._save_state()
            
            return {
                'status': 'success',
                'updated_state': self.current_state
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def simulate_scenario(self, changes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate impact of potential changes on user's state
        """
        try:
            # Create a copy of current state for simulation
            simulation = copy.deepcopy(self.current_state)
            
            # Example prompt for ChatGPT (in real implementation, would call ChatGPT API)
            prompt = self._generate_simulation_prompt(simulation, changes)
            
            # Simulate changes (simplified for PoC)
            simulated_impact = self._calculate_simulated_impact(simulation, changes)
            
            return {
                'status': 'success',
                'current_state': self.current_state,
                'simulated_state': simulated_impact,
                'analysis': {
                    'environmental_impact': {
                        'score_change': simulated_impact['environmental']['overall_score'] - 
                                      self.current_state['environmental']['overall_score'],
                        'carbon_reduction': simulated_impact['carbon_footprint'] - 
                                         self.current_state['carbon_footprint']
                    },
                    'health_impact': {
                        'score_change': simulated_impact['health']['overall_score'] - 
                                      self.current_state['health']['overall_score']
                    },
                    'timeline': self._estimate_timeline(changes)
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _process_environmental(self, data: Dict[str, Any]) -> None:
        """Process environmental data and update scores"""
        if 'transportation' in data:
            self._update_transportation_score(data['transportation'])
        if 'diet' in data:
            self._update_diet_score(data['diet'])
        if 'consumption' in data:
            self._update_consumption_score(data['consumption'])
        
        # Calculate overall environmental score
        scores = [
            self.current_state['environmental']['transportation']['score'],
            self.current_state['environmental']['diet']['score'],
            self.current_state['environmental']['consumption']['score']
        ]
        self.current_state['environmental']['overall_score'] = sum(scores) / len(scores)
    
    def _process_health(self, data: Dict[str, Any]) -> None:
        """Process health data and update scores"""
        if 'exercise' in data:
            self._update_exercise_score(data['exercise'])
        if 'sleep' in data:
            self._update_sleep_score(data['sleep'])
        if 'wellness' in data:
            self._update_wellness_score(data['wellness'])
        
        # Calculate overall health score
        scores = [
            self.current_state['health']['exercise']['score'],
            self.current_state['health']['sleep']['score'],
            self.current_state['health']['wellness']['score']
        ]
        self.current_state['health']['overall_score'] = sum(scores) / len(scores)
    
    def _calculate_combined_score(self) -> None:
        """Calculate combined health and environmental score"""
        self.current_state['combined_score'] = (
            self.current_state['environmental']['overall_score'] +
            self.current_state['health']['overall_score']
        ) / 2
    
    def _generate_simulation_prompt(self, state: Dict[str, Any], changes: Dict[str, Any]) -> str:
        """Generate prompt for ChatGPT simulation"""
        return f"""
        Given current state:
        {json.dumps(state, indent=2)}
        
        And proposed changes:
        {json.dumps(changes, indent=2)}
        
        Predict:
        1. Updated environmental scores
        2. Updated health scores
        3. Carbon footprint impact
        4. Timeline for changes
        5. Potential challenges
        """
    
    def _calculate_simulated_impact(self, simulation: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate simulated impact of changes (simplified for PoC)
        In real implementation, this would use ChatGPT for more sophisticated analysis
        """
        # Simple simulation logic (example)
        for change in changes.get('changes', []):
            if change['type'] == 'transportation':
                if 'increase public transit' in change['change'].lower():
                    simulation['environmental']['transportation']['score'] += 10
                    simulation['carbon_footprint'] -= 0.5
            elif change['type'] == 'diet':
                if 'plant-based' in change['change'].lower():
                    simulation['environmental']['diet']['score'] += 8
                    simulation['health']['wellness']['score'] += 5
                    simulation['carbon_footprint'] -= 0.3
        
        # Recalculate overall scores
        self._process_environmental(simulation['environmental'])
        self._process_health(simulation['health'])
        self._calculate_combined_score()
        
        return simulation
    
    def _estimate_timeline(self, changes: Dict[str, Any]) -> str:
        """Estimate timeline for changes to take effect"""
        # Simple timeline estimation (would be more sophisticated in real implementation)
        timelines = []
        for change in changes.get('changes', []):
            if 'timeline' in change:
                timelines.append(change['timeline'])
        
        return max(timelines) if timelines else "1 month"
    
    def _save_state(self) -> None:
        """
        Save current state (placeholder for database integration)
        In real implementation, this would persist to SQLite/database
        """
        pass

    def _update_transportation_score(self, data: Dict[str, Any]) -> None:
        """Calculate transportation score based on user data"""
        score = 50  # Base score
        key_factors = []

        # Scoring logic for transportation
        if data.get('primary_mode') == 'hybrid car':
            score += 10
            key_factors.append("Uses hybrid vehicle")
        elif data.get('primary_mode') == 'electric car':
            score += 20
            key_factors.append("Uses electric vehicle")
        elif data.get('primary_mode') == 'public transit':
            score += 25
            key_factors.append("Primary public transit user")

        # Miles per day impact
        miles_per_day = data.get('miles_per_day', 0)
        if miles_per_day <= 20:
            score += 20
            key_factors.append("Low daily mileage")
        elif miles_per_day <= 50:
            score += 10
            key_factors.append("Moderate daily mileage")
        else:
            score -= 10
            key_factors.append("High daily mileage")

        # Public transit usage
        transit_usage = data.get('public_transit', '0 times per week')
        if 'times per week' in transit_usage:
            times = int(transit_usage.split()[0])
            if times >= 3:
                score += 15
                key_factors.append("Regular public transit user")

        # Update the state
        self.current_state['environmental']['transportation']['score'] = min(100, max(0, score))
        self.current_state['environmental']['transportation']['key_factors'] = key_factors

    def _update_diet_score(self, data: Dict[str, Any]) -> None:
        """Calculate diet score based on user data"""
        score = 50  # Base score
        key_factors = []

        # Diet type scoring
        diet_type = data.get('type', 'unrestricted').lower()
        if diet_type == 'vegan':
            score += 25
            key_factors.append("Vegan diet")
        elif diet_type == 'vegetarian':
            score += 20
            key_factors.append("Vegetarian diet")
        elif diet_type == 'pescatarian':
            score += 15
            key_factors.append("Pescatarian diet")

        # Local food percentage
        local_food = data.get('local_food_percent', 0)
        if local_food >= 60:
            score += 15
            key_factors.append(f"{local_food}% local food consumption")
        elif local_food >= 30:
            score += 10
            key_factors.append("Moderate local food consumption")

        # Composting
        if data.get('composting'):
            score += 10
            key_factors.append("Practices composting")

        # Update the state
        self.current_state['environmental']['diet']['score'] = min(100, max(0, score))
        self.current_state['environmental']['diet']['key_factors'] = key_factors

    def _update_consumption_score(self, data: Dict[str, Any]) -> None:
        """Calculate consumption score based on user data"""
        score = 50  # Base score
        key_factors = []

        # Packaging preferences
        if data.get('packaging') == 'minimal':
            score += 15
            key_factors.append("Prefers minimal packaging")

        # Repair habits
        if 'repair' in data.get('repair_habits', '').lower():
            score += 10
            key_factors.append("Prioritizes repairs over replacement")

        # Zero waste efforts
        zero_waste = data.get('zero_waste_efforts', [])
        if zero_waste:
            score += min(len(zero_waste) * 5, 20)  # Cap at 20 points
            key_factors.append(f"Uses {len(zero_waste)} zero-waste practices")

        # Update the state
        self.current_state['environmental']['consumption']['score'] = min(100, max(0, score))
        self.current_state['environmental']['consumption']['key_factors'] = key_factors

    def _update_exercise_score(self, data: Dict[str, Any]) -> None:
        """Calculate exercise score based on user data"""
        score = 50  # Base score
        key_factors = []

        # Frequency scoring
        frequency = data.get('frequency', '').lower()
        if '4-5' in frequency:
            score += 25
            key_factors.append("Exercises 4-5 times per week")
        elif '2-3' in frequency:
            score += 15
            key_factors.append("Exercises 2-3 times per week")

        # Duration scoring
        duration = data.get('average_duration', 0)
        if duration >= 45:
            score += 15
            key_factors.append(f"{duration} min average duration")
        elif duration >= 30:
            score += 10
            key_factors.append("Moderate exercise duration")

        # Activity variety
        activities = data.get('activities', [])
        if len(activities) >= 3:
            score += 10
            key_factors.append("Diverse exercise routine")

        # Update the state
        self.current_state['health']['exercise']['score'] = min(100, max(0, score))
        self.current_state['health']['exercise']['key_factors'] = key_factors

    def _update_sleep_score(self, data: Dict[str, Any]) -> None:
        """Calculate sleep score based on user data"""
        score = 50  # Base score
        key_factors = []

        # Hours of sleep scoring
        hours = data.get('average_hours', 0)
        if 7 <= hours <= 9:
            score += 25
            key_factors.append(f"Optimal sleep duration ({hours} hours)")
        elif 6 <= hours < 7 or 9 < hours <= 10:
            score += 15
            key_factors.append("Near-optimal sleep duration")

        # Sleep quality scoring
        quality = data.get('quality', '').lower()
        if quality == 'good':
            score += 25
            key_factors.append("Good sleep quality")
        elif quality == 'fair':
            score += 15
            key_factors.append("Fair sleep quality")

        # Update the state
        self.current_state['health']['sleep']['score'] = min(100, max(0, score))
        self.current_state['health']['sleep']['key_factors'] = key_factors

    def _update_wellness_score(self, data: Dict[str, Any]) -> None:
        """Calculate wellness score based on user data"""
        score = 50  # Base score
        key_factors = []

        # Stress level scoring
        stress = data.get('stress_level', '').lower()
        if stress == 'low':
            score += 20
            key_factors.append("Low stress levels")
        elif stress == 'moderate':
            score += 10
            key_factors.append("Moderate stress levels")
        elif stress == 'high':
            score -= 10
            key_factors.append("High stress levels")

        # Update the state
        self.current_state['health']['wellness']['score'] = min(100, max(0, score))
        self.current_state['health']['wellness']['key_factors'] = key_factors
        
    def calculate_carbon_footprint(self, data: Dict[str, Any]) -> float:
        """Calculate estimated carbon footprint (tons CO2/year)"""
        carbon = 0.0

        # Transportation impact
        if 'environmental' in data and 'transportation' in data['environmental']:
            trans_data = data['environmental']['transportation']
            miles_per_day = trans_data.get('miles_per_day', 0)
            
            # Basic calculation (simplified for PoC)
            if trans_data.get('primary_mode') == 'hybrid car':
                carbon += miles_per_day * 0.2 * 365 / 2000  # Assuming 0.2 kg CO2 per mile
            elif trans_data.get('primary_mode') == 'gas car':
                carbon += miles_per_day * 0.4 * 365 / 2000  # Assuming 0.4 kg CO2 per mile

        # Diet impact
        if 'environmental' in data and 'diet' in data['environmental']:
            diet_data = data['environmental']['diet']
            if diet_data.get('type') == 'vegan':
                carbon += 1.5  # Base carbon footprint for vegan diet
            elif diet_data.get('type') == 'vegetarian':
                carbon += 2.0
            else:
                carbon += 2.5

        return carbon


# Example usage:
if __name__ == "__main__":
    # Create Digital Twin instance for Jessica
    jessica_twin = DigitalTwin("jessica_chen")
    
    # Update with initial data
    initial_data = {
        "environmental": {
            "transportation": {
                "primary_mode": "hybrid car",
                "miles_per_day": 120,
                "public_transit": "0 times per week"
            },
            "diet": {
                "type": "unrestricted",
                "local_food_percent": 60,
                "composting": True
            },
            "consumption": {
                "packaging": "prefers minimal",
                "repair_habits": "tries to repair before replacing",
                "zero_waste_efforts": ["reusable bags", "water bottle"]
            }
        },
        "health": {
            "exercise": {
                "frequency": "4-5 times per week",
                "activities": ["yoga", "cycling", "hiking"],
                "average_duration": 45
            },
            "sleep": {
                "average_hours": 7.5,
                "quality": "good"
            },
            "wellness": {
                "stress_level": "moderate"
            }
        }
    }
    
    # Update state and print results
    result = jessica_twin.update_state(initial_data)
    print("Initial State:")
    print(json.dumps(result, indent=2))
    
    # Test simulation
    scenario = {
        "changes": [
            {
                "type": "transportation",
                "change": "increase public transit to 3 times/week",
                "timeline": "1 month"
            },
            {
                "type": "diet",
                "change": "increase plant-based meals to 4 days/week",
                "timeline": "2 weeks"
            }
        ]
    }
    
    simulation_results = jessica_twin.simulate_scenario(scenario)
    print("\nSimulation Results:")
    print(json.dumps(simulation_results, indent=2))
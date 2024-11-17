from talk_tuah import TalkTuahUs
import json

# Initialize
tuahus = TalkTuahUs()

# Get a response
response = tuahus.get_response("I'm finding it hard to stay motivated...")
if response['status'] == 'success':
    print(response['response'])

# Get prompts
prompts = tuahus.get_suggested_prompts()

# Clear history if needed
tuahus.clear_history()
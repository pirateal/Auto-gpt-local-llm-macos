
import json

def execute_search_command(input_query):
    # Mocking a search function that returns a list of URLs based on the query
    if input_query:
        search_results = [
            "https://example.com/python-snake-game-tutorial-1",
            "https://example.com/python-snake-game-tutorial-2",
            "https://example.com/python-snake-game-tutorial-3"
        ]
        return json.dumps({"results": search_results})
    else:
        return json.dumps({"error": "No input query provided"})

def handle_search_command():
    # Simulating user input for a search command
    user_input = "Python snake game tutorial"
    result = execute_search_command(user_input)
    
    # Processing the result
    try:
        results = json.loads(result)
        if 'results' in results and results['results']:
            # Ensure we don't go out of range
            top_result = results['results'][0] if len(results['results']) > 0 else "No results found"
            return f"Top search result: {top_result}"
        else:
            return "Error: No search results found."
    except Exception as e:
        return f"Error processing search results: {str(e)}"

# Running the function to handle a search command
search_result = handle_search_command()
print(search_result)

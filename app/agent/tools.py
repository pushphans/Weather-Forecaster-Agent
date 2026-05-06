from langchain.tools import tool


@tool
def get_weather(location: str) -> str:
    """Get the current weather for a given city or location."""
    print("Fetching weather data for:", location)
    # Mock database
    mock_db = {
        "Jammu": "35°C and Sunny",
        "Delhi": "40°C and Hot",
        "Srinagar": "22°C and Pleasant",
    }
    return mock_db.get(location, f"Weather data not available for {location}.")


@tool
def get_flight_price(source: str, destination: str) -> str:
    """Get the cheapest flight price between a source and a destination city."""
    print(f"Fetching flight price from {source} to {destination}")
    # Mock database
    if source.lower() == "jammu" and destination.lower() == "srinagar":
        return "₹3500 via Air India Express"
    return f"Flight price from {source} to {destination} not found."


# Ye list tu apne LLM ko .bind_tools() ke sath pass karega aur ToolNode mein bhi dega
tools_list = [get_weather, get_flight_price]

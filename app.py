import streamlit as st
import requests
import os

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Andhra Pradesh Travel Planner",
    layout="wide"
)

# --------------------------------------------------
# Data
# --------------------------------------------------
ap_travel_data = {
    "cities": {
        "Kakinada": {
            "attractions": ["Kakinada Beach", "Local Temple"],
            "hotels": [
                {"name": "Seaside Inn", "rating": 4.2, "price": 120},
                {"name": "Town Guest House", "rating": 3.8, "price": 80}
            ]
        },
        "Annavaram": {
            "attractions": ["Annavaram Temple", "Local Market"],
            "hotels": [
                {"name": "Annavaram Lodge", "rating": 4.0, "price": 70}
            ]
        },
        "Lambasinghi": {
            "attractions": ["Lambasinghi Nature Trek"],
            "hotels": [
                {"name": "Lambasinghi Guest House", "rating": 4.1, "price": 90}
            ]
        },
        "Visakhapatnam": {
            "attractions": ["Kailash Giri", "R K Beach", "Shopping Areas"],
            "hotels": [
                {"name": "Sea View Hotel", "rating": 4.5, "price": 200}
            ]
        },
        "Rajahmundry": {
            "attractions": ["Godavari River Park", "Downtown Market"],
            "hotels": [
                {"name": "Riverfront Guest House", "rating": 4.1, "price": 100}
            ]
        },
        "Aruku": {
            "attractions": ["Aruku Valley", "Coffee Plantations"],
            "hotels": [
                {"name": "Aruku Hills Stay", "rating": 4.4, "price": 130}
            ]
        }
    },
    "bus_routes": {
        "Annavaram": 100,
        "Lambasinghi": 200,
        "Visakhapatnam": 300,
        "Rajahmundry": 150
    },
    "flights": {
        "Visakhapatnam": 2500
    }
}

# --------------------------------------------------
# Weather City Mapping (IMPORTANT FIX)
# --------------------------------------------------
weather_city_map = {
    "Kakinada": "Kakinada,IN",
    "Annavaram": "Annavaram,IN",
    "Lambasinghi": "Chintapalli,IN",
    "Visakhapatnam": "Visakhapatnam,IN",
    "Rajahmundry": "Rajahmundry,IN",
    "Aruku": "Araku Valley,IN"
}

# --------------------------------------------------
# API Key (Streamlit Secrets / Environment Variable)
# --------------------------------------------------
OPENWEATHER_API_KEY = st.secrets.get(
    "OPENWEATHER_API_KEY",
    os.getenv("OPENWEATHER_API_KEY")
)

# --------------------------------------------------
# Weather Function
# --------------------------------------------------
def get_weather(city):
    if not OPENWEATHER_API_KEY:
        return "Weather API key not configured"

    try:
        api_city = weather_city_map.get(city, city)
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={api_city}&appid={OPENWEATHER_API_KEY}&units=metric"
        )
        data = requests.get(url, timeout=5).json()

        if data.get("cod") != 200:
            return "Weather unavailable"

        description = data["weather"][0]["description"].title()
        temperature = data["main"]["temp"]

        return f"{description}, {temperature} °C"

    except Exception:
        return "Weather unavailable"

# --------------------------------------------------
# UI
# --------------------------------------------------
st.title("Andhra Pradesh Travel Planner")
st.caption("Starting Point: Kakinada")

st.sidebar.header("Travel Selection")
cities = list(ap_travel_data["cities"].keys())
selected_city = st.sidebar.selectbox("Choose Destination", cities)

if st.sidebar.button("Generate Plan"):
    st.subheader(f"Destination: {selected_city}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Transport", "Hotels", "Attractions", "Weather", "Itinerary"]
    )

    # --------------------------------------------------
    # Transport Tab
    # --------------------------------------------------
    with tab1:
        transport_options = []

        if selected_city == "Kakinada":
            transport_options.append("Local travel only: Auto, Cab, City Bus")
        else:
            transport_options.append("Local travel available at destination")

        if selected_city in ap_travel_data["bus_routes"]:
            fare = ap_travel_data["bus_routes"][selected_city]
            transport_options.append(
                f"Bus available from Kakinada. Fare: ₹{fare}"
            )

        if selected_city in ap_travel_data["flights"]:
            fare = ap_travel_data["flights"][selected_city]
            transport_options.append(
                f"Flight available from Rajahmundry. Fare: ₹{fare}"
            )

        for option in transport_options:
            st.success(option)

    # --------------------------------------------------
    # Hotels Tab
    # --------------------------------------------------
    with tab2:
        for hotel in ap_travel_data["cities"][selected_city]["hotels"]:
            st.markdown(
                f"""
                **{hotel['name']}**  
                Rating: {hotel['rating']}  
                Price per night: ₹{hotel['price']}
                """
            )
            st.divider()

    # --------------------------------------------------
    # Attractions Tab
    # --------------------------------------------------
    with tab3:
        for attraction in ap_travel_data["cities"][selected_city]["attractions"]:
            st.write(f"- {attraction}")

    # --------------------------------------------------
    # Weather Tab
    # --------------------------------------------------
    with tab4:
        st.info(get_weather(selected_city))

    # --------------------------------------------------
    # Itinerary Tab
    # --------------------------------------------------
    with tab5:
        attractions = ap_travel_data["cities"][selected_city]["attractions"]
        for day in range(3):
            if day < len(attractions):
                st.write(f"Day {day + 1}: Visit {attractions[day]}")
            else:
                st.write(f"Day {day + 1}: Explore local food and markets")

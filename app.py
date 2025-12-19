import streamlit as st
import requests

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
            "hotels": [{"name": "Annavaram Lodge", "rating": 4.0, "price": 70}]
        },
        "Lambasinghi": {
            "attractions": ["Lambasinghi Nature Trek"],
            "hotels": [{"name": "Lambasinghi Guest House", "rating": 4.1, "price": 90}]
        },
        "Visakhapatnam": {
            "attractions": ["Kailash Giri", "R K Beach", "Shopping Areas"],
            "hotels": [{"name": "Sea View Hotel", "rating": 4.5, "price": 200}]
        },
        "Rajahmundry": {
            "attractions": ["Godavari River Park", "Downtown Market"],
            "hotels": [{"name": "Riverfront Guest House", "rating": 4.1, "price": 100}]
        },
        "Aruku": {
            "attractions": ["Aruku Valley", "Coffee Plantations"],
            "hotels": [{"name": "Aruku Hills Stay", "rating": 4.4, "price": 130}]
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

OPENWEATHER_API_KEY = "db387806b254dde28cb5eae4f65aad66"

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()
        return f"{data['weather'][0]['description']}, {data['main']['temp']}°C"
    except:
        return "Weather unavailable"

st.title("Andhra Pradesh Travel Planner")
st.write("Starting Point: Kakinada")

cities = list(ap_travel_data["cities"].keys())
selected_city = st.selectbox("Select Destination", cities)

if st.button("Generate Travel Plan"):
    st.subheader(selected_city)

    st.subheader("Transport")
    if selected_city == "Kakinada":
        st.info("Local travel only: Auto / Cab / Bus")
    elif selected_city in ap_travel_data["bus_routes"]:
        st.success(f"Bus available. Fare: ₹{ap_travel_data['bus_routes'][selected_city]}")
    elif selected_city in ap_travel_data["flights"]:
        st.success(f"Flight available from Rajahmundry. Fare: ₹{ap_travel_data['flights'][selected_city]}")
    else:
        st.warning("No direct transport available")

    st.subheader("Hotels")
    for h in ap_travel_data["cities"][selected_city]["hotels"]:
        st.write(f"{h['name']} | Rating {h['rating']} | ₹{h['price']}")

    st.subheader("Attractions")
    for a in ap_travel_data["cities"][selected_city]["attractions"]:
        st.write(a)

    st.subheader("Weather")
    st.info(get_weather(selected_city))

    st.subheader("Three-Day Itinerary")
    attractions = ap_travel_data["cities"][selected_city]["attractions"]
    for i in range(3):
        if i < len(attractions):
            st.write(f"Day {i + 1}: Visit {attractions[i]}")
        else:
            st.write(f"Day {i + 1}: Explore local food and markets")

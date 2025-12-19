import streamlit as st
import requests

st.set_page_config(page_title="Andhra Pradesh Travel Planner", layout="wide")

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
        return f"{data['weather'][0]['description'].title()}, {data['main']['temp']} °C"
    except:
        return "Weather unavailable"

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

            
    with tab1:
        transport_options = []
        if selected_city == "Kakinada":
            transport_options.append("Local travel only: Auto, Cab, City Bus")
        else:
            transport_options.append("Local travel available at your destination")
        if selected_city in ap_travel_data["bus_routes"]:
            fare = ap_travel_data["bus_routes"][selected_city]
            transport_options.append(f"Bus available from Kakinada. Fare: ₹{fare}")
        if selected_city in ap_travel_data["flights"]:
            fare = ap_travel_data["flights"][selected_city]
            transport_options.append(f"Flight available from Rajahmundry. Fare: ₹{fare}")
        if transport_options:
            for option in transport_options:
                st.success(option)
        else:
            st.warning("No direct transport available")


    with tab2:
        for h in ap_travel_data["cities"][selected_city]["hotels"]:
            st.markdown(
                f"""
                **{h['name']}**  
                Rating: {h['rating']}  
                Price per night: ₹{h['price']}
                """
            )
            st.divider()

    with tab3:
        for a in ap_travel_data["cities"][selected_city]["attractions"]:
            st.write(f"- {a}")

    with tab4:
        st.info(get_weather(selected_city))

    with tab5:
        attractions = ap_travel_data["cities"][selected_city]["attractions"]
        for i in range(3):
            if i < len(attractions):
                st.write(f"Day {i + 1}: Visit {attractions[i]}")
            else:
                st.write(f"Day {i + 1}: Explore local food and markets")

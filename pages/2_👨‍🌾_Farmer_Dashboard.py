import pandas as pd
import streamlit as st
from utils.database import animals_collection
from utils.model import load_dataset, prepare_model, predict_milk_production, provide_advice

def show_farmer_dashboard():
    if 'user' not in st.session_state or st.session_state.user is None or st.session_state.login_type != 'farmer':
        st.warning("Please login as a farmer to view this page.")
        return

    st.title(f"Welcome, {st.session_state.user['username']}")

    # Show list of animals
    st.subheader("Your Animals")
    animals = list(animals_collection.find({"farmer": st.session_state.user['username']}))
    if animals:
        animal_df = pd.DataFrame(animals)
        animal_df = animal_df.sort_values('milk_production', ascending=False)
        st.dataframe(animal_df[['breed', 'milk_production']])
    else:
        st.info("You have no animals registered yet.")

    # Add new animal form
    st.subheader("Add New Animal")
    new_animal = {
        "farmer": st.session_state.user['username'],
        "breed": st.selectbox("Breed", ['Friesian', 'Jersey', 'Holstein', 'Ayrshire', 'Guernsey'], key="new_animal_breed"),
        "age": st.number_input("Age (years)", min_value=1, max_value=20, key="new_animal_age"),
        "weight": st.number_input("Weight (kg)", min_value=100, max_value=1000, key="new_animal_weight"),
        "milk_production": st.number_input("Current Milk Production (L/day)", min_value=0.0, step=0.1, key="new_animal_milk")
    }
    if st.button("Add Animal", key="add_animal_button"):
        animals_collection.insert_one(new_animal)
        st.success("Animal added successfully")
        

    # Milk production prediction
    st.subheader("Predict Milk Production")
    # Load the dataset and prepare the model
    file_path = "dataset.csv"
    data = load_dataset(file_path)
    model = prepare_model(data)

    input_data = {
        'Breed': st.selectbox("Breed for prediction", ['Friesian', 'Jersey', 'Holstein', 'Ayrshire', 'Guernsey'], key="pred_breed"),
        'Age': st.number_input("Age for prediction (years)", min_value=1, max_value=20, step=1, key="pred_age"),
        'Weight': st.number_input("Weight for prediction (kg)", min_value=100, max_value=1000, step=1, key="pred_weight"),
        'LactationPeriod': st.number_input("Lactation Period (days)", min_value=100, max_value=400, step=1, key="pred_lactation"),
        'HealthStatus': st.selectbox("Health Status", ['Healthy', 'Sick'], key="pred_health"),
        'FeedType': st.selectbox("Feed Type", ['Hay', 'Silage', 'Alfalfa', 'Grain', 'Pasture'], key="pred_feed"),
        'FeedAmount': st.number_input("Feed Amount (kg/day)", min_value=0.0, max_value=50.0, step=0.1, key="pred_feed_amount"),
        'WaterIntake': st.number_input("Water Intake (L/day)", min_value=0.0, max_value=200.0, step=0.1, key="pred_water"),
        'Temperature': st.number_input("Temperature (°C)", min_value=-10.0, max_value=50.0, step=0.1, key="pred_temp"),
        'Humidity': st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, step=0.1, key="pred_humidity"),
        'BarnCondition': st.selectbox("Barn Condition", ['Clean', 'Moderate', 'Dirty'], key="pred_barn"),
        'PastMilkProduction': st.number_input("Past Milk Production (L/day)", min_value=0.0, max_value=50.0, step=0.1, key="pred_past_milk"),
        'MilkingFrequency': st.number_input("Milking Frequency (per day)", min_value=0, max_value=10, step=1, key="pred_milking_freq"),
        'VetVisits': st.number_input("Veterinary Visits (per month)", min_value=0, max_value=10, step=1, key="pred_vet_visits")
    }

    if st.button("Predict Milk Production", key="predict_milk_button"):
        predicted_milk_production = predict_milk_production(model, input_data)
        st.success(f"Predicted Milk Production: {predicted_milk_production:.2f} liters per day")
        
        advice = provide_advice(input_data)
        if advice:
            st.subheader("Advice for Animal Care")
            for item in advice:
                st.warning(f"⚠️ {item}")

if __name__ == "__main__":
    show_farmer_dashboard()
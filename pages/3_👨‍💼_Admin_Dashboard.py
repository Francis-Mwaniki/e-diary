import streamlit as st
import pandas as pd
import plotly.express as px
from utils.database import users_collection, animals_collection

def show_admin_dashboard():
    if 'user' not in st.session_state or st.session_state.user is None or st.session_state.login_type != 'admin':
        st.warning("Please login as an admin to view this page.")
        return

    st.title(f"Welcome, Admin {st.session_state.user['username']}")

    # User management
    st.subheader("User Management")
    users = list(users_collection.find({"role": "farmer"}))
    for i, user in enumerate(users):
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.write(f"Username: {user['username']}, Status: {'Active' if user['is_active'] else 'Inactive'}")
        if col2.button("Toggle Status", key=f"toggle_{user['username']}_{i}"):
            users_collection.update_one(
                {"_id": user['_id']},
                {"$set": {"is_active": not user['is_active']}}
            )
           
        if col3.button("Delete User", key=f"delete_{user['username']}_{i}"):
            users_collection.delete_one({"_id": user['_id']})
            animals_collection.delete_many({"farmer": user['username']})
           

    # Farm statistics
    st.subheader("Farm Statistics")
    total_animals = animals_collection.count_documents({})
    total_milk_production = sum(animal['milk_production'] for animal in animals_collection.find())
    st.write(f"Total number of animals: {total_animals}")
    st.write(f"Total daily milk production: {total_milk_production:.2f} liters")

    # Visualizations
    st.subheader("Data Visualizations")
    animals_data = list(animals_collection.find())
    if animals_data:
        df = pd.DataFrame(animals_data)
        
        fig1 = px.histogram(df, x='milk_production', nbins=30, title="Milk Production Distribution")
        st.plotly_chart(fig1)

        fig2 = px.box(df, x='breed', y='milk_production', title="Milk Production by Breed")
        st.plotly_chart(fig2)
    else:
        st.info("No animal data available for visualization.")

if __name__ == "__main__":
    show_admin_dashboard()
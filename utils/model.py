import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor

def load_dataset(file_path):
    return pd.read_csv(file_path)

# load the dataset
data = load_dataset('dataset.csv')
def prepare_model(data):
    X = data.drop(columns=['MilkProduction'])
    y = data['MilkProduction']

    numerical_features = ['Age', 'Weight', 'LactationPeriod', 'FeedAmount', 'WaterIntake', 
                          'Temperature', 'Humidity', 'PastMilkProduction', 'MilkingFrequency', 'VetVisits']
    categorical_features = ['Breed', 'HealthStatus', 'FeedType', 'BarnCondition']

    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)])

    model = Pipeline(steps=[('preprocessor', preprocessor),
                            ('regressor', RandomForestRegressor(n_estimators=100, random_state=0))])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    model.fit(X_train, y_train)
    print(f'Model training score: {model.score(X_train, y_train)}')

    return model

def predict_milk_production(model, input_data):
    input_df = pd.DataFrame([input_data])
    return model.predict(input_df)[0]

def provide_advice(input_data):
    advice = []
    if input_data['HealthStatus'] == 'Sick':
        advice.append("Your cow is sick. Consult a veterinarian for appropriate medical treatment.")
    if input_data['FeedAmount'] < 20:
        advice.append("Increase the feed amount to at least 20 kg per day to ensure adequate nutrition.")
    if input_data['WaterIntake'] < 40:
        advice.append("Increase the water intake to at least 40 liters per day to ensure proper hydration.")
    if input_data['Temperature'] > 30:
        advice.append("Ensure proper ventilation and cooling to prevent heat stress.")
    if input_data['Humidity'] > 80:
        advice.append("Ensure proper ventilation to prevent respiratory problems.")
    if input_data['BarnCondition'] == 'Dirty':
        advice.append("Clean the barn regularly to prevent diseases and infections.")
    if input_data['MilkingFrequency'] < 2:
        advice.append("Increase the milking frequency to at least twice a day for optimal milk production.")
    if input_data['VetVisits'] < 4:
        advice.append("Schedule regular veterinary visits to ensure the health and well-being of your cow.")
    return advice
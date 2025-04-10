import flask
from flask import Flask, request, jsonify
import pandas as pd
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load model and expected feature columns
model = joblib.load('../notebook/best_model_Bagging_Regressor.pkl')
expected_columns = joblib.load('../notebook/model_features.pkl')

# Dynamically extract crops and areas
crop_prefix = "Item_"
area_prefix = "Area_"
crops = sorted([col[len(crop_prefix):] for col in expected_columns if col.startswith(crop_prefix)])
areas = sorted([col[len(area_prefix):] for col in expected_columns if col.startswith(area_prefix)])

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse input JSON
        data = request.json
        avg_rain = data.get('average_rain_fall_mm_per_year', 1200.0)
        pesticides = data.get('pesticides_tonnes', 500.0)
        avg_temp = data.get('avg_temp', 18.5)
        selected_crop = data.get('selected_crop')
        selected_area = data.get('selected_area')

        # Validate crop and area
        if selected_crop not in crops or selected_area not in areas:
            return jsonify({'error': 'Invalid crop or area selected'}), 400

        # Build input dict
        input_data = {
            'average_rain_fall_mm_per_year': [avg_rain],
            'pesticides_tonnes': [pesticides],
            'avg_temp': [avg_temp],
        }

        # One-hot encode crop and area
        for crop in crops:
            input_data[f'Item_{crop}'] = [1 if crop == selected_crop else 0]
        for area in areas:
            input_data[f'Area_{area}'] = [1 if area == selected_area else 0]

        # Convert to DataFrame
        input_df = pd.DataFrame(input_data)

        # Reindex to match expected columns (fill missing with 0)
        input_df = input_df.reindex(columns=expected_columns, fill_value=0)

        # Prediction
        prediction = model.predict(input_df)
        print(prediction)
        return jsonify({'predicted_yield': round(prediction[0], 2)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

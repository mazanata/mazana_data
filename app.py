from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Home(Resource):
    def get(self):
        return {'version': '1.0'}

class ConvertTemp(Resource):
    def get(self):
        # Get arguments from query parameters
        temp = float(request.args.get('temp'))
        scale = request.args.get('scale').lower()
        target_scale = request.args.get('target_scale').lower()

        # Perform temperature conversion
        converted_temp = self.convert_temperature(temp, scale, target_scale)
        
        if converted_temp is None:
            return {'error': 'Invalid scale or target scale'}, 400

        return {'converted_temp': converted_temp, 'target_scale': target_scale}

    def convert_temperature(self, temp, scale, target_scale):
        # Conversion logic
        if scale == target_scale:
            return temp

        if scale == 'celsius':
            if target_scale == 'fahrenheit':
                return temp * 9/5 + 32
            elif target_scale == 'kelvin':
                return temp + 273.15

        elif scale == 'fahrenheit':
            if target_scale == 'celsius':
                return (temp - 32) * 5/9
            elif target_scale == 'kelvin':
                return (temp - 32) * 5/9 + 273.15

        elif scale == 'kelvin':
            if target_scale == 'celsius':
                return temp - 273.15
            elif target_scale == 'fahrenheit':
                return (temp - 273.15) * 9/5 + 32

        # If scales are invalid
        return None

api.add_resource(Home, '/')
api.add_resource(ConvertTemp, '/convert-temp')

if __name__ == '__main__':
    app.run(debug=True)

Flask==3.0.3
Flask-RESTful==0.3.10
pytest==8.3.2



import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Home route test
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'version': '1.0'}

# Fahrenheit to Celsius
@pytest.mark.parametrize("temp, expected", [(212, 100.0), (32, 0.0), (-40, -40.0)])
def test_convert_temp_f_to_c(client, temp, expected):
    response = client.get(f'/convert-temp?temp={temp}&scale=fahrenheit&target_scale=celsius')
    assert response.status_code == 200
    assert response.json['converted_temp'] == pytest.approx(expected, rel=1e-2)

# Celsius to Fahrenheit
@pytest.mark.parametrize("temp, expected", [(100, 212.0), (0, 32.0), (-40, -40.0)])
def test_convert_temp_c_to_f(client, temp, expected):
    response = client.get(f'/convert-temp?temp={temp}&scale=celsius&target_scale=fahrenheit')
    assert response.status_code == 200
    assert response.json['converted_temp'] == pytest.approx(expected, rel=1e-2)

# Kelvin to Celsius
@pytest.mark.parametrize("temp, expected", [(273.15, 0.0), (373.15, 100.0), (233.15, -40.0)])
def test_convert_temp_k_to_c(client, temp, expected):
    response = client.get(f'/convert-temp?temp={temp}&scale=kelvin&target_scale=celsius')
    assert response.status_code == 200
    assert response.json['converted_temp'] == pytest.approx(expected, rel=1e-2)

# Kelvin to Fahrenheit
@pytest.mark.parametrize("temp, expected", [(273.15, 32.0), (373.15, 212.0), (233.15, -40.0)])
def test_convert_temp_k_to_f(client, temp, expected):
    response = client.get(f'/convert-temp?temp={temp}&scale=kelvin&target_scale=fahrenheit')
    assert response.status_code == 200
    assert response.json['converted_temp'] == pytest.approx(expected, rel=1e-2)

# Invalid scale handling
def test_convert_temp_invalid_scale(client):
    response = client.get('/convert-temp?temp=100&scale=unknown&target_scale=celsius')
    assert response.status_code == 400
    assert 'error' in response.json





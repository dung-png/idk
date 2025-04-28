import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px

# This is a placeholder for a built-in API key.
# In a real application, you would handle API keys more securely.
BUILT_IN_API_KEY = "2341866a33e6f42c7b76a75c179f72f9"

def get_weather_data(city, units):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={BUILT_IN_API_KEY}&units={units}"
    response = requests.get(url)
    return response.json()

def get_forecast_data(city, units):
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={BUILT_IN_API_KEY}&units={units}"
    forecast_response = requests.get(forecast_url)
    return forecast_response.json()

def get_unit_api(unit_label):
    if "Celsius" in unit_label:
        return "metric"
    elif "Fahrenheit" in unit_label:
        return "imperial"
    else:
        return "standard"

def convert_temp_unit(temp, unit):
    if unit == "metric":
        return f"{temp} °C"
    elif unit == "imperial":
        return f"{temp} °F"
    else:
        return f"{temp} K"

def format_forecast_time(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime("%H:%M, %d %b")

st.set_page_config(page_title="Weather DASMBLARK", layout="wide")

with st.sidebar:
    st.title("🌤️ Comprehensive Weather Center")
    City = st.selectbox("🌆Choose City", options=["Ho Chi Minh City", "Hanoi", "Da Nang", "Hai Phong", "Can Tho", "Nha Trang", "Hue", "Vung Tau", "Bien Hoa", "Quy Nhon", "Thanh Hoa", "Nam Dinh", "Thai Nguyen", "Vinh", "Long Xuyen", "Rach Gia", "Ca Mau", "Bac Lieu", "Phan Thiet", "Pleiku", "Da Lat", "Lao Cai", "Ha Long", "Uong Bi", "Bac Ninh", "Bac Giang", "Thai Binh", "Hung Yen", "Tuy Hoa", "Kon Tum", "Son La", "Dien Bien Phu", "Phu Ly", "Ha Tinh", "Quang Ngai", "Tam Ky", "Cam Pha", "Sam Son", "Mong Cai", "My Tho", "Cao Lanh", "Dong Ha", "Tuy Hoa", "Yen Bai", "Vinh Yen", "Dong Xoai", "Ha Giang", "Lạng Sơn", "Cao Bằng", "Tuyên Quang", "Bắc Kạn", "Hòa Bình", "Ninh Bình", "Phú Thọ", "Quảng Trị", "Đồng Hới", "Tây Ninh", "Vĩnh Long", "Sa Đéc", "Trà Vinh", "Bến Tre", "Sóc Trăng", "Gia Nghia", "Hội An", "Tam Kỳ", "Cam Ranh", "Vị Thanh", "Phan Rang-Tháp Chàm", "Tuy Hòa", "Móng Cái", "Sa Pa", "Điện Biên", "Hà Đông", "Thủ Dầu Một", "Dĩ An", "Thuận An", "Biên Hòa", "Long Khánh", "Bà Rịa", "Phú Quốc", "Châu Đốc", "Hà Tiên", "Sầm Sơn", "Cửa Lò", "Đông Hà", "Huế", "Tam Kỳ", "Hội An", "Quy Nhơn", "Tuy Hòa", "Buôn Ma Thuột", "Gia Nghĩa", "Kon Tum", "Pleiku", "Đà Lạt", "Bảo Lộc", "Phan Thiết", "Vũng Tàu", "Bà Rịa", "Tây Ninh", "Thủ Dầu Một", "Biên Hòa", "Long Xuyên", "Rạch Giá", "Cà Mau", "Bạc Liêu", "Sóc Trăng", "Trà Vinh", "Vĩnh Long", "Sa Đéc", "Cao Lãnh", "Mỹ Tho", "Bến Tre", "Tân An", "Vị Thanh", "Phú Quốc", "Châu Đốc", "Hà Tiên", "Lai Châu", "Sơn La", "Điện Biên Phủ", "Yên Bái", "Tuyên Quang", "Hà Giang", "Cao Bằng", "Lạng Sơn", "Bắc Kạn", "Thái Nguyên", "Việt Trì", "Hạ Long", "Uông Bí", "Cẩm Phả", "Móng Cái", "Hải Dương", "Hưng Yên", "Vĩnh Yên", "Bắc Ninh", "Phủ Lý", "Nam Định", "Thái Bình", "Ninh Bình", "Tam Điệp", "Thanh Hóa", "Bỉm Sơn", "Sầm Sơn", "Vinh", "Đông Hà", "Huế", "Đà Nẵng", "Tam Kỳ", "Hội An", "Quảng Ngãi", "Tuy Hòa", "Quy Nhơn", "Pleiku", "Kon Tum", "Buôn Ma Thuột", "Gia Nghĩa", "Đà Lạt", "Bảo Lộc", "Phan Thiết", "Vũng Tàu", "Bà Rịa", "Tây Ninh", "Thủ Dầu Một", "Biên Hòa", "Long Xuyên", "Rạch Giá", "Cà Mau", "Bạc Liêu", "Sóc Trăng", "Trà Vinh", "Vĩnh Long", "Sa Đéc", "Cao Lãnh", "Mỹ Tho", "Bến Tre", "Tân An", "Vị Thanh", "Phú Quốc", "Châu Đốc", "Hà Tiên", "Lạng Sơn", "Cao Bằng", "Hà Giang", "Yên Bái", "Lào Cai", "Điện Biên Phủ", "Sơn La", "Lai Châu", "Hòa Bình", "Phú Thọ", "Tuyên Quang", "Bắc Kạn", "Thái Nguyên", "Việt Trì", "Bắc Ninh", "Hưng Yên", "Hải Dương", "Thái Bình", "Nam Định", "Ninh Bình", "Tam Điệp", "Thanh Hóa", "Vinh", "Huế", "Đà Nẵng", "Tam Kỳ", "Hội An", "Quảng Ngãi", "Quy Nhơn", "Tuy Hòa", "Nha Trang", "Đà Lạt", "Buôn Ma Thuột", "Pleiku", "Kon Tum", "Gia Nghĩa", "Phan Thiết", "Vũng Tàu", "Biên Hòa", "Thủ Dầu Một", "Tây Ninh", "Mỹ Tho", "Long Xuyên", "Rạch Giá", "Cà Mau", "Bạc Liêu", "Sóc Trăng", "Trà Vinh", "Vĩnh Long", "Sa Đéc", "Cao Lãnh", "Châu Đốc", "Hà Tiên", "Tokyo", "Shanghai", "Beijing", "Seoul", "Mumbai", "Delhi", "Bangkok", "Singapore", "Kuala Lumpur", "Jakarta", "Hong Kong", "Taipei", "Osaka", "Nagoya", "Yokohama", "Manila", "Ho Chi Minh City", "Hanoi", "Dhaka", "Karachi", "Lahore", "Riyadh", "Jeddah", "Dubai", "Abu Dhabi", "Tehran", "Istanbul", "Jerusalem", "Baghdad", "Kabul", "Pyongyang", "Ulaanbaatar", "Phnom Penh", "Vientiane", "Yangon", "Colombo", "Kathmandu", "London", "Paris", "Berlin", "Rome", "Madrid", "Moscow", "Saint Petersburg", "Kyiv", "Warsaw", "Bucharest", "Budapest", "Vienna", "Prague", "Amsterdam", "Brussels", "Copenhagen", "Stockholm", "Oslo", "Helsinki", "Dublin", "Lisbon", "Athens", "Milan", "Naples", "Barcelona", "Valencia", "Munich", "Hamburg", "Cologne", "Frankfurt", "Zurich", "Geneva", "Rotterdam", "The Hague", "Edinburgh", "Glasgow", "Cardiff", "Belfast", "Seville", "Lyon", "Marseille", "New York City", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose", "Toronto", "Montreal", "Calgary", "Ottawa", "Mexico City", "Guadalajara", "Monterrey", "Vancouver", "Seattle", "Boston", "Washington D.C.", "Miami", "Atlanta", "Denver", "Orlando", "Las Vegas", "Minneapolis", "St. Louis", "Sao Paulo", "Rio de Janeiro", "Buenos Aires", "Bogota", "Lima", "Santiago", "Caracas", "Brasilia", "Medellin", "Montevideo", "Quito", "Guayaquil", "La Paz", "Sucre", "Cairo", "Lagos", "Kinshasa", "Johannesburg", "Cape Town", "Algiers", "Casablanca", "Accra", "Nairobi", "Addis Ababa", "Dar es Salaam", "Alexandria", "Abidjan", "Kano", "Ibadan", "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Auckland", "Wellington"])
    Unit = st.selectbox("🌡️Unit", options=["Celsius: ℃", "Fahrenheit: ℉", "Kelvin: K"])
    Analyse = st.button("Analyse", "btn1", "Get Weather Details", use_container_width=True)

if Analyse:
    unit_api = get_unit_api(Unit)
    weather_data = get_weather_data(City, unit_api)
    forecast_data = get_forecast_data(City, unit_api)

    if weather_data.get("cod") == 200:
        st.subheader(f"Current Weather in {City}")
        main_info = weather_data.get('main')
        wind_info = weather_data.get('wind')
        clouds_info = weather_data.get('clouds')
        weather_desc = weather_data.get('weather', [{}])[0].get('main', '').lower()

        # Change background color based on weather
        if 'clear' in weather_desc:
            st.markdown("<style>body {background-color:lightblue;}</style>", unsafe_allow_html=True)
        elif 'clouds' in weather_desc:
            st.markdown("<style>body {background-color:lightgray;}</style>", unsafe_allow_html=True)
        elif 'rain' in weather_desc or 'drizzle' in weather_desc:
            st.markdown("<style>body {background-color:lightcoral;}</style>", unsafe_allow_html=True)
        elif 'thunderstorm' in weather_desc:
            st.markdown("<style>body {background-color:darkgray;}</style>", unsafe_allow_html=True)
        elif 'snow' in weather_desc:
            st.markdown("<style>body {background-color:whitesmoke;}</style>", unsafe_allow_html=True)
        else:
            st.markdown("<style>body {background-color:lightyellow;}</style>", unsafe_allow_html=True)

        if main_info:
            temp_unit_display = Unit.split(':')[1]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Temperature", convert_temp_unit(main_info.get('temp'), unit_api))
            with col2:
                st.metric("Feels Like", convert_temp_unit(main_info.get('feels_like'), unit_api))
            with col3:
                st.metric("Min Temp", convert_temp_unit(main_info.get('temp_min'), unit_api))
            with col4:
                st.metric("Max Temp", convert_temp_unit(main_info.get('temp_max'), unit_api))

            col5, col6 = st.columns(2)
            with col5:
                st.metric("Humidity", f"{main_info.get('humidity', 'N/A')}%")
            with col6:
                st.metric("Pressure", f"{main_info.get('pressure', 'N/A')} hPa")

           # Temperature Chart (Modified to be a bar chart for single values)
            temp_data = pd.DataFrame({
                'Metric': ['Temperature', 'Feels Like', 'Min Temp', 'Max Temp'],
                'Value': [main_info['temp'], main_info['feels_like'],
                          main_info['temp_min'], main_info['temp_max']]
            })
            fig_temp = px.area(temp_data, x='Metric', y='Value',
                               title=f"Temperature Details ({temp_unit_display})")
            st.plotly_chart(fig_temp, use_container_width=True)

            # Humidity Chart
            humidity_df = pd.DataFrame({'Humidity': [main_info['humidity']]})
            fig_humidity = px.bar(humidity_df, y='Humidity', title="Humidity Level")
            st.plotly_chart(fig_humidity, use_container_width=True)

            if wind_info:
                # Wind Speed Chart
                wind_df = pd.DataFrame({'Wind Speed': [wind_info.get('speed')]})
                fig_wind = px.bar(wind_df, y='Wind Speed', title=f"Wind Speed (m/s)")
                st.plotly_chart(fig_wind, use_container_width=True)

            if clouds_info:
                # Cloudiness Chart
                clouds_df = pd.DataFrame({'Cloudiness': [clouds_info.get('all')]})
                fig_clouds = px.line(clouds_df, y='Cloudiness', title="Cloudiness (%)")
                st.plotly_chart(fig_clouds, use_container_width=True)

        else:
            st.error("Could not retrieve main weather information.")
    else:
        st.error("Failed to retrieve current weather data for this city.")

    if forecast_data.get("cod") == "200":
        st.subheader("5-Day Weather Forecast")
        forecast_list = forecast_data.get('list')
        if forecast_list:
            forecast_df = pd.DataFrame(forecast_list)
            forecast_df['dt_txt'] = pd.to_datetime(forecast_df['dt_txt'])
            forecast_df['temp'] = forecast_df['main'].apply(lambda x: x['temp'])
            forecast_df['feels_like'] = forecast_df['main'].apply(lambda x: x['feels_like'])
            forecast_df['description'] = forecast_df['weather'].apply(lambda x: x[0]['description'])

            forecast_df_display = forecast_df[['dt_txt', 'temp', 'feels_like', 'description']].copy()
            forecast_df_display['temp'] = forecast_df_display['temp'].apply(lambda x: convert_temp_unit(x, unit_api))
            forecast_df_display['feels_like'] = forecast_df_display['feels_like'].apply(lambda x: convert_temp_unit(x, unit_api))

            st.dataframe(forecast_df_display)

            # Temperature Forecast Chart
            fig_forecast_temp = px.area(forecast_df, x='dt_txt', y='temp',
                                       title=f"5-Day Temperature Forecast ({temp_unit_display})")
            st.plotly_chart(fig_forecast_temp, use_container_width=True)
        else:
            st.warning("Forecast data not available.")
    else:
        st.warning("Could not retrieve forecast data.")
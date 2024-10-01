import requests
from datetime import datetime, timezone
import smtplib

my_email = 'maheshwariarjun04@gmail.com'
my_password = 'zpvtzwfztshmutpy'


MY_LAT = 51.507351  
MY_LONG = -0.127758  

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    print(f"ISS Position: Latitude: {iss_latitude}, Longitude: {iss_longitude}")  # Debugging

    
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    return False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,  
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    print(f"Sunrise-Sunset API Data: {data}")  

    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]

    sunrise_time = datetime.fromisoformat(sunrise).replace(tzinfo=timezone.utc)
    sunset_time = datetime.fromisoformat(sunset).replace(tzinfo=timezone.utc)

    print(f"Sunrise Time (UTC): {sunrise_time}, Sunset Time (UTC): {sunset_time}")  

    
    time_now = datetime.now(timezone.utc)
    print(f"Current Time (UTC): {time_now}")  


    if time_now >= sunset_time or time_now <= sunrise_time:
        return True
    return False

if is_iss_overhead() and is_night():
    print("The ISS is overhead and it's night!") 
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg="Subject:Look Up\n\nThe ISS is above you right now!"
        )
else:
    print("ISS is not overhead or it's not night.") 

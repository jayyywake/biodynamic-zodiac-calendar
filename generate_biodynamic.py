import ephem
import math
import datetime
from ics import Calendar, Event

def get_moon_zodiac_sign(date):
    # Compute moon position for the given date
    moon = ephem.Moon()
    moon.compute(date)
    
    # Convert equatorial coordinates to ecliptic (Tropical Zodiac)
    ecl = ephem.Ecliptic(moon)
    lon_deg = math.degrees(ecl.lon)
    
    signs = [
        ("Aries", "🔥 Fire - Fruit/Seed"),
        ("Taurus", "🌱 Earth - Root"),
        ("Gemini", "💨 Air - Flower"),
        ("Cancer", "💧 Water - Leaf"),
        ("Leo", "🔥 Fire - Fruit/Seed"),
        ("Virgo", "🌱 Earth - Root"),
        ("Libra", "💨 Air - Flower"),
        ("Scorpio", "💧 Water - Leaf"),
        ("Sagittarius", "🔥 Fire - Fruit/Seed"),
        ("Capricorn", "🌱 Earth - Root"),
        ("Aquarius", "💨 Air - Flower"),
        ("Pisces", "💧 Water - Leaf")
    ]
    
    # Each sign is exactly 30 degrees of the 360-degree circle
    sign_index = int(lon_deg / 30) % 12
    return signs[sign_index]

def generate_biodynamic_calendar():
    cal = Calendar()
    today = datetime.datetime.utcnow().date()
    
    # 90-day rolling window keeps the file lightweight and fast-loading
    for i in range(90):
        current_date = today + datetime.timedelta(days=i)
        
        # Check the moon's position at noon to determine the dominant energy of the day
        check_time = datetime.datetime.combine(current_date, datetime.time(12, 0))
        sign_name, element_type = get_moon_zodiac_sign(check_time)
        
        # Choose a clean emoji based on the plant part
        if "Root" in element_type:
            emoji = "🥕"
        elif "Leaf" in element_type:
            emoji = "🌿"
        elif "Flower" in element_type:
            emoji = "🌸"
        else:
            emoji = "🍓"
            
        event_name = f"{emoji} {element_type} (Moon in {sign_name})"
        
        e = Event(name=event_name, begin=current_date)
        e.make_all_day()
        cal.events.add(e)
        
    with open("biodynamic_zodiac.ics", "w") as f:
        f.writelines(cal.serialize_iter())

if __name__ == "__main__":
    generate_biodynamic_calendar()

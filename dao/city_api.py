import requests
response = requests.get("https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-1000/records?limit=20")
print(response.status_code)
print(response.json())
json_data=response.json()

import pandas as pd
pd.D(json_data)
pd.DataFrame.from_dict(json_data)




import requests

def search_cities(city_name=None, country_name=None, department_code=None, rows=10):
    base_url = "https://public.opendatasoft.com/api/records/1.0/search/"
    dataset = "geonames-all-cities-with-a-population-1000"

    # Parameters for the API request
    params = {
        'dataset': dataset,
        'rows': rows,  # Number of results to return
    }

    # Add filters based on the input parameters
   
    if country_name:
        params['refine.cou_name_en'] = country_name
    if city_name:
        params['refine.name'] = city_name
    # if department_code:
    #     params['refine.admin1_code'] = department_code
    
    # Make the API request
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        records = data.get('records', [])

        # Process and return city information
        results = []
        for record in records:
            city_info = record.get('fields', {})
            results.append({
                'city_name': city_info.get('name'),
                'country_name': city_info.get('cou_name_en'),
                'departement': city_info.get('admin2_code') 
            })
        return results
    else:
        return f"Error: Unable to retrieve data (Status Code: {response.status_code})"


# Example usage:
cities = search_cities(city_name="Madrid", country_name="Spain", department_code="29", rows=10)
cities = search_cities(city_name="Paris", country_name="France", department_code="75", rows=10)

for city in cities:
    print(city)

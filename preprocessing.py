import pandas as pd
import json

def get_cams_by_place(data):
    plot_cams = {}
    country_list = ["AU", "FR",
                    "AT", "DK", "GB",
                    "CZ", "CH", "IT",
                    "DE", "CA", "NZ",
                    "HK", "ES", "HR"]
    for country in country_list:   
        plot_cams[country] = list(set(data.loc[data['country'] == country, 'cam_id']))

    state_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "FL", "GA", 
            "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
            "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
            "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
            "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "PR"]
    for state in state_list:
        plot_cams[state] = list(set(data.loc[data['state'] == state, 'cam_id']))
    return plot_cams

if __name__ == "__main__":
    cars_file = "combined_csv_vehicles_4-1_8-1.csv"
    cars = pd.read_csv(cars_file)
    cars = cars.fillna(0)
    plot_cams = get_cams_by_place(cars)
    json.dump(plot_cams, open( "car_cams.json", 'w' ) )

    people_file = "combined_csv_pedestrians_4-1_8-1.csv"
    people = pd.read_csv(people_file)
    people = people.fillna(0)
    plot_cams = get_cams_by_place(people)
    json.dump(plot_cams, open( "people_cams.json", 'w' ) )

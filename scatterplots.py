""" This file plots scatterplots of a specified country or US state with optional color
    coding for date ranges.
"""


from plotting_tools import *
from matplotlib.patches import Patch
import pycountry
from matplotlib.lines import Line2D
from us_states import us_state_abbrev
import argparse
import mpld3
import math
import datetime

def color_list(plot_dates, date1=None, date2=None, date3=None, date4=None):
    if (date1):
        point1 = plot_dates.index(date1)
    if (date2):
        point2 = plot_dates.index(date2)
    if (date3):
        point3 = plot_dates.index(date3)
    if (date4):
        point4 = plot_dates.index(date4)
    
    if date4:
        return ["r"]*(point1) + ["g"]*(point2 - point1) + ["b"]*(point3-point2) + ["black"]*(point4-point3) + ["darkorchid"]*(len(plot_dates)-point4),  ['x']*(point1)+['o']*((point2) - point1) + ['*']*(point3 - point2) + ['+']*(point4 - point3) + ['D']*(len(plot_dates)-point4)

    elif date2:
        return ["r"]*(point1) + ["g"]*(((point2)) - point1) + ["blue"]*(len(plot_dates)-point2),  ['x']*(point1)+['o']*(point2 - point1) + ['*']*(len(plot_dates) - point2)

    elif date1:
        return ["r"]*(point1) + ["g"]*(len(plot_dates) - point1),  ['x']*(point1)+['o']*(len(plot_dates) - point1)

    else:
        return ["r"]*len(plot_dates), ['x']*len(plot_dates)


def generate_plot(country=None, state=None, date1=None, date2=None, date3=None, date4=None):
    fig, ax = plt.subplots()


    countries = {}
    for countryname in pycountry.countries:
        countries[countryname.name] = countryname.alpha_2


    if country:
        short_form = countries.get(country, 'Unknown code')
        place_to_use = country
    elif state:
        #short_form = us_state_abbrev[state]
        short_form = state
        place_to_use = state


    """vehicle counts ----------------------------------------------------------
    """

    col = "vehicle_count"
    cars = "combined_csv_vehicles_4-1_8-1.csv"
    colap = pd.read_csv('processed_vehicles.csv')
    data = pd.read_csv(cars)
    data = data.fillna(0)
    # select range of date
    data = data.loc[(data['date'] >= date1) & (data['date'] <= date2)]

    # remove the data of March 31
    useful_data = colap[1:]
    # select range of date
    useful_data['date_keys'] = '2020-' + useful_data['date_keys'].astype(str)
    useful_data['date_keys'] = pd.to_datetime(useful_data['date_keys'])
    useful_data = useful_data.loc[(useful_data['date_keys'] >= date1) & (useful_data['date_keys'] <= date2)]
    data_points = len(useful_data)

    start_samples = []
    end_samples = []
    plot_dates = []

    for i in range(data_points):
        start_samples.append(1*i)
        end_samples.append(min(1*(i+1), data_points))

    for i in range(data_points):
        plot_dates.append(np.array(useful_data[start_samples[i]:start_samples[i]+1]["date_keys"])[0])



    daily_counts = np.zeros((data_points))

    if country:
        plot_cams = get_plot_cams_list(data, country=short_form)
    elif state:
        plot_cams = get_plot_cams_list(data, state=short_form)


    for i in range(data_points): 
        data_to_use = useful_data[start_samples[i]:end_samples[i]][plot_cams] 
        daily_counts[i] = np.max(np.sum(data_to_use[plot_cams], axis=1))


    """people counts -----------------------------------------------------------------
    """

    col = "pedestrian_count"
    people = "combined_csv_pedestrians_4-1_8-1.csv"
    colap = pd.read_csv('processed_people.csv')
    data = pd.read_csv(people)
    data = data.fillna(0)
    # select range of date
    data = data.loc[(data['date'] >= date1) & (data['date'] <= date2)]

    # remove the data of March 31
    useful_data = colap[1:]
    # select range of date
    useful_data['date_keys'] = '2020-' + useful_data['date_keys'].astype(str)
    useful_data['date_keys'] = pd.to_datetime(useful_data['date_keys'])
    useful_data = useful_data.loc[(useful_data['date_keys'] >= date1) & (useful_data['date_keys'] <= date2)]
    data_points = len(useful_data)

    start_samples = []
    end_samples = []
    plot_dates = []

    for i in range(data_points):
        start_samples.append(1*i)
        end_samples.append(min(1*(i+1), data_points))


    for i in range(data_points):
       plot_dates.append(np.array(useful_data[start_samples[i]:start_samples[i]+1]["date_keys"])[0])
    

    daily_counts_people = np.zeros((data_points))

    if country:
        plot_cams = get_plot_cams_list(data, country=short_form)
    elif state:
        plot_cams = get_plot_cams_list(data, state=short_form)

    for i in range(data_points): 
        data_to_use = useful_data[start_samples[i]:end_samples[i]][plot_cams] 
        daily_counts_people[i] = np.max(np.sum(data_to_use[plot_cams], axis=1))


    ax.set(title="Scatterplot of People Count vs Vehicle Count in " + place_to_use)

    # colors, markers=color_list(plot_dates[1:-1], date1=date1, date2=date2, date3=date3, date4=date4)


    ax.set_xlabel('Vehicle count')
    ax.set_ylabel('People count')


    # Add legends
    dates = []
    dates_str = []
    for date in ['2020-05-01', '2020-06-01', '2020-07-01']:
        if len(useful_data.loc[(useful_data['date_keys'] == date)]) > 0:
            dates.append(np.datetime64(date))
            dates_str.append(date)
    if len(dates) == 3:
        colors, markers=color_list(plot_dates[1:-1], date1=dates[0], date2=dates[1], date3=dates[2])
    elif len(dates) == 2:
        colors, markers=color_list(plot_dates[1:-1], date1=dates[0], date2=dates[1])
    elif len(dates) == 1:
        colors, markers=color_list(plot_dates[1:-1], date1=dates[0])
    else:
        colors, markers=color_list(plot_dates[1:-1])


    for i in range(len(colors)):
        ax.scatter(daily_counts[i], daily_counts_people[i], color= colors[i], marker= markers[i], s=3)

    if len(dates) != 0:
        legend_elements = [Line2D([0], [0], marker='o', color='w', label='Scatter',
                            markerfacecolor='r', markersize=9),
                        Line2D([0], [0], marker='o', color='w', label='Scatter',
                            markerfacecolor='g', markersize=9),
                        Line2D([0], [0], marker='o', color='w', label='Scatter',
                            markerfacecolor='b', markersize=9),
                        Line2D([0], [0], marker='o', color='w', label='Scatter',
                            markerfacecolor='black', markersize=9),
                        Line2D([0], [0], marker='o', color='w', label='Scatter',
                            markerfacecolor='darkorchid', markersize=9),
                        ]

        legend = []
        prevdate = date1.replace("2020-", "")
        for each in dates_str:
            if each!=None:
                each = each.replace("2020-", "")
                legend+=[str(prevdate + '-- ' + each)]
                prevdate=each

        legend+=[str(prevdate + '-- ' + date2.replace("2020-", ""))]

        ax.legend(legend_elements, legend)

    fig.set_size_inches(5, 5)

    bins = math.floor(len(daily_counts)/7)
    vehicle_by_week = [sum(daily_counts[i:i+7]) for i in range(bins)]
    people_by_week = [sum(daily_counts_people[i:i+7]) for i in range(bins)]
    fig1, ax1 = plt.subplots()

    bar_width = 0.35
    ax1.bar(np.arange(bins), vehicle_by_week, bar_width, align='center', alpha=0.5, color='b', label='vehicle')
        
    ax1.bar(np.arange(bins) + bar_width, people_by_week, bar_width, align='center', alpha=0.5, color='g', label='people')

    """
    ticks = []
    for i in range(bins):
        week = datetime.datetime.strptime(date1, '%Y-%m-%d') + datetime.timedelta(days=i*7)
        ticks.append(week.strptime(date, '%Y-%m-%d'))
    """

    plt.xticks(np.arange(bins), range(bins))
    plt.ylabel('Counts')
    plt.xlabel('Week')
    plt.legend(loc='upper left')
    ax1.set(title="Time Series Histogram of People and Vehicle Count in " + place_to_use)
    fig1.set_size_inches(5, 5)

    return mpld3.fig_to_html(fig), mpld3.fig_to_html(fig1)


























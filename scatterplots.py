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
import time
from numba import njit, jit 
import json

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
    elif date3:
        return ["r"]*(point1) + ["g"]*(point2 - point1) + ["b"]*(point3-point2) + ["black"]*(len(plot_dates)-point3), ['x']*(point1)+['o']*(point2 - point1) + ['*']*(point3 - point2) + ['+']*(len(plot_dates) - point3)
    elif date2:
        return ["r"]*(point1) + ["g"]*(point2 - point1) + ["blue"]*(len(plot_dates)-point2),  ['x']*(point1)+['o']*(point2 - point1) + ['*']*(len(plot_dates) - point2)

    elif date1:
        return ["r"]*(point1) + ["g"]*(len(plot_dates) - point1),  ['x']*(point1)+['o']*(len(plot_dates) - point1)

    else:
        return ["r"]*len(plot_dates), ['x']*len(plot_dates)


def generate_plot(country=None, state=None, date1=None, date2=None, mobile=False):
    # start
    print(country)
    start_time = time.time()

    if mobile:
        fig, ax = plt.subplots(2, 1, figsize=(4, 8.5))
    else:
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))


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

    # start reading csv
    start_read_csv = time.time()
    print("program start: " + str(start_read_csv - start_time))

    col = "vehicle_count"
    colap = pd.read_csv('processed_vehicles.csv')

    # some preprocessing
    start_preprocessing = time.time()
    print("read vehicle csv: " + str(start_preprocessing - start_read_csv))


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

    cams = json.load(open("car_cams.json"))
    plot_cams = cams[short_form]

    for i in range(data_points): 
        data_to_use = useful_data[start_samples[i]:end_samples[i]][plot_cams] 
        daily_counts[i] = np.max(np.sum(data_to_use[plot_cams], axis=1))


    # end vehicle 
    vehicle_processing_end = time.time()
    print("vehicle preprocessing: " + str(vehicle_processing_end - start_preprocessing))

    """people counts -----------------------------------------------------------------
    """

    col = "pedestrian_count"
    colap = pd.read_csv('processed_people.csv')

    # people preprocessing
    people_preprocessing = time.time()
    print("read people csv: " + str(people_preprocessing-vehicle_processing_end))


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

    cams = json.load(open("people_cams.json"))
    plot_cams = cams[short_form]

    for i in range(data_points): 
        data_to_use = useful_data[start_samples[i]:end_samples[i]][plot_cams] 
        daily_counts_people[i] = np.max(np.sum(data_to_use[plot_cams], axis=1))


    ax[0].set(title="Scatterplot of People Count vs Vehicle Count in " + place_to_use)

    # colors, markers=color_list(plot_dates[1:-1], date1=date1, date2=date2, date3=date3, date4=date4)

    # people preprocessing end
    people_preprocessing_end = time.time()
    print("people preprocessing: " + str(people_preprocessing_end - people_preprocessing))

    ax[0].set_xlabel('Vehicle count')
    ax[0].set_ylabel('People count')


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
        ax[0].scatter(daily_counts[i], daily_counts_people[i], color= colors[i], marker= markers[i], s=5)

    if len(dates) != 0:
        legend_elements = [Line2D([0], [0], marker='x', color='r', ls='',
                            markerfacecolor='r', markersize=9),
                        Line2D([0], [0], marker='o', color='g', ls='',
                            markerfacecolor='g', markersize=9),
                        Line2D([0], [0], marker='*', color='b', ls='',
                            markerfacecolor='b', markersize=9),
                        Line2D([0], [0], marker='+', color='black', ls='',
                            markerfacecolor='black', markersize=9),
                        Line2D([0], [0], marker='o', color='w', ls='',
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

        ax[0].legend(legend_elements, legend)


    # code for barplot
    bins = math.floor(len(daily_counts)/7)
    vehicle_by_week = [sum(daily_counts[i:i+7]) for i in range(bins)]
    people_by_week = [sum(daily_counts_people[i:i+7]) for i in range(bins)]
    # fig1, ax1 = plt.subplots()

    bar_width = 0.35
    ax[1].bar(np.arange(bins), vehicle_by_week, bar_width, align='center', alpha=0.5, color='b', label='vehicle')
        
    ax[1].bar(np.arange(bins) + bar_width, people_by_week, bar_width, align='center', alpha=0.5, color='g', label='people')

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
    ax[1].set(title="Time Series of People and Vehicle Count in " + place_to_use)

    #fig.set_size_inches(4, 4)

    # plot end
    print("generate plot: " + str(time.time() - people_preprocessing_end))
    return mpld3.fig_to_html(fig)




if __name__ == '__main__':
    plot = generate_plot(country="Germany", date1="2020-06-10", date2="2020-07-02")





















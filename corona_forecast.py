from datetime import datetime
import matplotlib.pyplot as plt
import numpy
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

def init_dict():
    dict_corona = {}
    dict_corona['20/02/24'] = 16
    dict_corona['20/02/25'] = 16
    dict_corona['20/02/26'] = 19
    dict_corona['20/02/27'] = 24
    dict_corona['20/02/28'] = 53
    dict_corona['20/02/29'] = 66
    dict_corona['20/03/01'] = 117
    dict_corona['20/03/02'] = 150
    dict_corona['20/03/03'] = 188
    dict_corona['20/03/04'] = 240
    dict_corona['20/03/05'] = 349
    dict_corona['20/03/06'] = 534
    dict_corona['20/03/07'] = 684
    dict_corona['20/03/08'] = 847   #  Calculated Data
    dict_corona['20/03/09'] = 1112  #  1188
    dict_corona['20/03/10'] = 1565  #  1513
    dict_corona['20/03/11'] = 1966  #  2076
    dict_corona['20/03/12'] = 2745  #  2655
    dict_corona['20/03/13'] = 3675  #  3627
    dict_corona['20/03/14'] = 4585  #  4899
    dict_corona['20/03/15'] = 5813  #  6197
    dict_corona['20/03/16'] = 7272  #  7775
    dict_corona['20/03/17'] = 9360  #  9645
    dict_corona['20/03/18'] = 12327  # 12194
    dict_corona['20/03/19'] = 15320  # 15844
    #dict_corona['20/03/20'] = 15320  # 19917

    return dict_corona

def convert_x_to_datetime(x_list):
    new_x_list = []
    for date in x_list:
        datetime_object = datetime.strptime(date, '%y/%m/%d')
        new_x_list.append(datetime_object)
    return new_x_list

def func(x, parameter):
    y = []
    for data in x:
        y.append(parameter[0] * numpy.exp(parameter[1]*data))
    return numpy.array(y)

def print_forecast(x, popt):
    print('Forecast Germany:')
    x_forecast = list(range(len(x), len(x) + 10))
    y_forecast = func(x_forecast, popt)
    for i, value in enumerate(y_forecast):
        if i == 0:
            print(' Today: %d' %(int(value)))
        elif i == 1:
            print('%d Day : %d' %(i, int(value)))
        else:
            print('%d Days: %d' %(i, int(value)))

def plot_figure(x, y, y_c, popt, dict_corona):
    start_date = list(dict_corona.keys())[0]
    end_date = list(dict_corona.keys())[-1]
    r2_s = r2_score(y, y_c)
    annotate = 'R² = %f\n'  %r2_s
    annotate += 'f(t) = %.3f * exp(%.3f*t)' %(popt[0],popt[1])
    x = convert_x_to_datetime(dict_corona.keys())
    plt.figure()
    plt.title('COVID-19 Cases in Germany [' +
              start_date + '-' + end_date + ']')
    plt.annotate(annotate, xy=(0.03, 0.76), xycoords='axes fraction')
    plt.grid(True)
    plt.xticks(rotation=20)
    plt.plot(x, y_c, label='Fitted Model', color='#FF8000')
    plt.scatter(x, y, label='Data Points')
    plt.legend()
    plt.show()

def calc_curves(dict_corona):
    x = list(range(len(dict_corona.keys())))
    y = numpy.array(list(dict_corona.values()))
    popt, _ = curve_fit(lambda t,a,b: a*numpy.exp(b*t), x, y)
    y_c = func(x, popt)
    return x, y, popt, y_c


if __name__ == "__main__":
    dict_corona = init_dict()
    x, y, popt, y_c = calc_curves(dict_corona)
    print_forecast(x, popt)
    plot_figure(x, y, y_c, popt, dict_corona)
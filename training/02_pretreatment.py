import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # load data from csv file
    data = pd.read_csv('data.csv', index_col='date', parse_dates=['date'])

    # resample data to per day
    data = data['price'].resample('D').mean()

    # fill NaN with next valid value
    data = data.fillna(data.bfill())

    # show data after pretrearment
    # data.plot(figsize=(15, 6))
    # plt.show()

    # save data to csv file
    data.to_csv('data.csv', header=1)

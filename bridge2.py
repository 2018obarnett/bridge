import generateAndHandleData

import argparse
import sys

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import sklearn.model_selection as sm
import pandas as pd



# no clue how this works: https://stackoverflow.com/a/34482761
def progressbar(it, max, prefix="", size=60, out=sys.stdout): 
    def show(j):
        x = int(size*j/max)
        print(f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{max}",
              end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)


# Reads data in from csv, and splits into train and test data
def getData(csv_path):
    df = pd.read_csv(csv_path)
    df = df.drop('Index', axis=1)
    # TODO: make this a stratified shuffle split
    train, test = sm.train_test_split(df, test_size=0.2) 
    train = train.reset_index().drop('index', axis=1)
    test = test.reset_index().drop('index', axis=1)
    return train, test

# Returns the N/S HC point total
def calculateHCPoints(weight, series):
    np, sp, ep, wp = 0, 0, 0, 0
    for k in weight.keys():
        np += ''.join(list(series[1:5])).count(k) * weight.get(k)
        sp += ''.join(list(series[5:9])).count(k) * weight.get(k)
        ep += ''.join(list(series[9:13])).count(k) * weight.get(k)
        wp += ''.join(list(series[13:17])).count(k) * weight.get(k)
    return np + sp

# Returns the N/S distribution point total
def calculateDISTPoints(weight, series):
    return 0
    

# weight = dict of metrics, such as a dict of card and its point value
# i.e. {"HCP": {"A": 4, "K": 3, "Q": 2, "J": 1}, "DIST": {5:1, 6:2, 7:3, 8:4, 9:5} }
def getPointsTricksDataFrame(weight, df):
    new_df = pd.DataFrame(columns=["pts", "trx"], dtype="string")
    df_size = len(df)

    # for index, row in df.iterrows():
    for index, row in progressbar(df.iterrows(), df_size, "Processing: ", 40):
        pts = calculateHCPoints(weight["HCP"], row)
        pts += calculateDISTPoints(weight["DIST"], row)
        new_df.loc[len(new_df)] = [pts, row["trx"]]
    return new_df

def prepData(df):
    pass

def visualize(train_data, test_data):
    # values converts it into a numpy array
    train_x = train_data.iloc[:, 0].values.reshape(-1, 1)
    # -1 means that calculate the dimension of rows, but have 1 column
    train_y = train_data.iloc[:, 1].values.reshape(-1, 1)
    # values converts it into a numpy array
    test_x = test_data.iloc[:, 0].values.reshape(-1, 1)
    # -1 means that calculate the dimension of rows, but have 1 column
    test_y = test_data.iloc[:, 1].values.reshape(-1, 1)


    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(train_x, train_y)  # perform linear regression
    train_predictor = linear_regressor.predict(train_x)  # make predictions

    train_fit_score = linear_regressor.score(train_x, train_y)
    test_fit_score = linear_regressor.score(test_x, test_y)
    print(f"Train Score: {round(train_fit_score, 5)}")
    print(f"Test Score: {round(test_fit_score, 5)}")


    fig, axs = plt.subplots(1, 2, sharey=True)
    axs[0].scatter(train_x, train_y)
    axs[0].plot(train_x, train_predictor, color='red')
    axs[0].set_title("Training Data")

    axs[1].scatter(test_x, test_y)
    axs[1].plot(train_x, train_predictor, color='red')
    axs[1].set_title("Testing Data")

    plt.show()


def addNoiseToWeights(weights):
    # TODO: implement this
    return weights

def prepareDataFromCSV(csv_path):
    train, test = getData(csv_path)

    print(train.head())
    print(test.head())

    weights = {"HCP": {"A": 4.1, "K": 3.1, "Q": 2.1, "J": 1.1}, "DIST": {} }
    weights = addNoiseToWeights(weights)
    train_prepped = getPointsTricksDataFrame(weights, train)
    test_prepped = getPointsTricksDataFrame(weights, test)
    return train_prepped, test_prepped


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a description")
    parser.add_argument('-hp', '--hand-path', default=None,
                        help="file path to a .csv file containing hand records and tricks taken")
    parser.add_argument('-bsp', '--bridge-solver-path', default=None,
                        help="path to \`bridge-solver\` executable")
    parser.add_argument('-n', '--num-hands', default=1000,
                        help="number of hands to generate and solve")
    args = parser.parse_args()
    argsdict = vars(args)
    print(argsdict['hand_path'])
    print(argsdict['bridge_solver_path'])
    print(argsdict['num_hands'])

    if args.hand_path:
        print(f"Using hand file found at {args.hand_path}")
    else:
        if not args.bridge_solver_path:
            parser.error("-hp or -bsp and -n option should be filled")
        else:
            print(f"Using bridge-solver found at {args.bridge_solver_path}")
            if not args.num_hands:
                parser.error("-n optional required when using -bsp")

    if not args.hand_path:
        # TODO: update that file so it's not this way
        csv_path = generateAndHandleData.main(['fp', args.bridge_solver_path, args.num_hands, 32])
    else:
        csv_path = args.hand_path

    # csv_path = 'HandRecords/100000Deals-0.csv'
    # csv_path = 'HandRecords/1000Deals-0.csv' # comment out to use the larger set, this is faster

    print(csv_path)
    train, test = prepareDataFromCSV(csv_path)

    print(train)
    print(test)
    visualize(train, test)

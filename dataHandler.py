import os.path
import time
import pandas as pd

def makeOutputFilePath():
    return os.path.join('HandRecords', 'hands' + str(time.time().__trunc__()) + '.csv')

def handToSeries(hand_directory, deal):
    path = os.path.join(hand_directory, deal)
    with open(path, 'r') as file:
        [ns, nh, nd, nc] = file.readline().strip().split(' ')
        [es, eh, ed, ec, x, x, x, x, x, ws, wh, wd, wc] = file.readline().strip().split(' ')
        [ss, sh, sd, sc] = file.readline().strip().split(' ')
    return [ns, nh, nd, nc, es, eh, ed, ec, ws, wh, wd, wc, ss, sh, sd, sc]

def makeDataFrameFromHands(hand_directory):
    df = pd.DataFrame(columns=['ns', 'nh', 'nd', 'nc', 'es', 'eh', 'ed', 'ec', 'ws', 'wh', 'wd', 'wc', 'ss', 'sh', 'sd', 'sc'], dtype="string")

    for deal in os.listdir(hand_directory):
        if not deal == 'RESULTS':
            result =  handToSeries(hand_directory, deal)
            df.loc[len(df)] = result
    return df

def convert_to_csv(hand_directory, output_file_path=makeOutputFilePath()):
    df = makeDataFrameFromHands(hand_directory)
    df.to_csv(output_file_path, index_label = "Index", header  = ['ns', 'nh', 'nd', 'nc', 'es', 'eh', 'ed', 'ec', 'ws', 'wh', 'wd', 'wc', 'ss', 'sh', 'sd', 'sc'])    

    print(f"Wrote csv to {output_file_path}")
    return output_file_path

if __name__ == "__main__":
    convert_to_csv('HandRecords/1k_deals')

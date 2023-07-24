import os.path
import time
import pandas as pd

header = ['trx', 'ns', 'nh', 'nd', 'nc', 'ss', 'sh', 'sd', 'sc', 'es', 'eh', 'ed', 'ec', 'ws', 'wh', 'wd', 'wc']
def makeOutputFilePath():
    return os.path.join('HandRecords', 'hands' + str(time.time().__trunc__()) + '.csv')

def handToList(hand_directory, deal, trx = -1):
    path = os.path.join(hand_directory, deal)
    with open(path, 'r') as file:
        [ns, nh, nd, nc] = file.readline().strip().split(' ')
        [es, eh, ed, ec, x, x, x, x, x, ws, wh, wd, wc] = file.readline().strip().split(' ')
        [ss, sh, sd, sc] = file.readline().strip().split(' ')
    return [trx, ns, nh, nd, nc, ss, sh, sd, sc, es, eh, ed, ec, ws, wh, wd, wc,]

def convert_to_csv(hand_directory, output_file_path=makeOutputFilePath()):
    df = pd.DataFrame(columns=header, dtype="string")

    with open(os.path.join(hand_directory, 'RESULTS'), 'r') as results_file:
        while True:
            file = results_file.readline().strip()
            if len(file) == 0: break
            tricks = results_file.readline().split()[1]
            for _ in range(4):
                next(results_file)
            df.loc[len(df)] = handToList(hand_directory, file, trx = tricks)

    df.to_csv(output_file_path, index_label = "Index", header  = header)    

    print(f"Wrote csv to {output_file_path}")
    return output_file_path

if __name__ == "__main__":
    convert_to_csv('HandRecords/1k_deals')

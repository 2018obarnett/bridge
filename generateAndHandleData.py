import sys, os, time, subprocess, re
import pandas as pd
import threading
import queue
from utility import Seat

header = ['trx', 'ns', 'nh', 'nd', 'nc', 'ss', 'sh', 'sd',
          'sc', 'es', 'eh', 'ed', 'ec', 'ws', 'wh', 'wd', 'wc']
nsPattern = re.compile("^[nNsS].$")
ewPattern = re.compile("^[eEwW].$")


def makeOutputFilePath(num):
    return os.path.join('HandRecords', str(num) + 'Deals' + str(time.time().__trunc__()) + '.csv')

def dealToList(deal):
    tricksArray = []
    for seat in Seat:
        # for each person it will make a list of the tricks taken when they declare in the order No, spades, hearts, diamonds, clubs ex 10 10 4 3 5 meaning 4 tricks if they declare in hearts 
        tricksArray.append(" ".join((deal.split()[33+seat.value:-1:9])))
        
    tricks = " ".join(tricksArray)

    [ns, nh, nd, nc, es, eh, ed, ec, ws, wh, wd, wc, ss, sh, sd, sc] = deal.split()[1:32:2]
    return [tricks, ns, nh, nd, nc, ss, sh, sd, sc, es, eh, ed, ec, ws, wh, wd, wc]

def makeAndFillDataframe(path, num_deals, result_queue):
    start_time = time.time()

    df = pd.DataFrame(columns=header, dtype="string")
    for _ in range(num_deals):
        result = subprocess.run(
            [f"./{path}", "-r", "-m 2"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        lst = dealToList(result)
        df.loc[len(df)] = lst    
    result_queue.put(df)

    end_time = time.time()
    elapsed_time = end_time - start_time

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()


# Generate dataframe with num_hands rows with format [trx, ns, nh, nd, nc, ss, sh, sd, sc, es, eh, ed, ec, ws, wh, wd, wc]
def generateData(num_hands:int, solver_path:str, num_threads:int=1) -> pd.DataFrame:
    result_queue = queue.Queue()
    hands_per_thread = int(num_hands/num_threads)
    remainder = num_hands - hands_per_thread * num_threads

    start_t = time.time()
    thread_pool = []
    for i in range(num_threads):
        count = hands_per_thread + (i < remainder)
        thread_pool.append(threading.Thread(target=makeAndFillDataframe,
                                          args=(solver_path, count, result_queue)))
    for t in thread_pool:
        t.start()
    
    for t in thread_pool:
        t.join()

    result = []
    while not result_queue.empty():
        result.append(result_queue.get())

    print(f"Generated {num_hands} hands in {time.time()-start_t:.2f}s")
    return pd.concat(result, ignore_index=True)

# Read data from a provided csv into a dataframe with format [trx, ns, nh, nd, nc, ss, sh, sd, sc, es, eh, ed, ec, ws, wh, wd, wc]
def getData(file_name) -> pd.DataFrame:
    return pd.read_csv(file_name) # probably doesn't work lol

def saveData(df:pd.DataFrame, file_name) -> None:
    df.to_csv(file_name, index_label="Index", header=header)
    print(f"Wrote csv to {file_name}")
    
def attachPoints(df:pd.DataFrame, weights:list[float]) -> None:
    # todo: distribution points
    df['NSPoints'] = df.apply(lambda row: getNSPoints(row, weights), axis=1)
    df['EWPoints'] = df.apply(lambda row: getEWPoints(row, weights), axis=1)

def getNSPoints(row:pd.Series, weights) -> int:
    hands = ''.join([row.get(k) for k in row.keys() if nsPattern.match(k)])
    return sum([hands.count(k) * weights['HCP'][k] for k in weights['HCP']])

def getEWPoints(row:pd.Series, weights) -> int:
    hands = ''.join([row.get(k) for k in row.keys() if ewPattern.match(k)])
    return sum([hands.count(k) * weights['HCP'][k] for k in weights['HCP']])

def main(args):
    if len(args) < 3:
        raise "Not enough arguments"
    repo = args[1]
    num_hands = int(args[2])
    if len(args) > 3:
        output_path = args[3]
        output_path = makeOutputFilePath(num_hands)
    else:
        output_path = makeOutputFilePath(num_hands)
    if len(args) > 4:
        thread_count = int(args[4])
    else: 
        thread_count = 1
    path = os.path.join(repo, 'solver')

    result_queue = queue.Queue()
    hands_per_thread = int(num_hands/thread_count)
    remainder = num_hands - hands_per_thread * thread_count

    thread_pool = []
    for i in range(thread_count):
        count = hands_per_thread + (i < remainder)
        thread_pool.append(threading.Thread(target=makeAndFillDataframe,
                                          args=(path, count, result_queue)))
    for t in thread_pool:
        t.start()
    
    for t in thread_pool:
        t.join()


    print(result_queue.qsize())

    out = []
    while not result_queue.empty():
        out.append(result_queue.get())
    output_df = pd.concat(out, ignore_index=True)
    
    print(output_df)




    output_df.to_csv(output_path, index_label="Index", header=header)

    print(f"Wrote csv to {output_path}")
    return output_path


if __name__ == "__main__":
    start_time = time.time()

    main(sys.argv)

    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)

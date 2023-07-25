import sys, os, time, subprocess
import pandas as pd
import threading
import queue

header = ['trx', 'ns', 'nh', 'nd', 'nc', 'ss', 'sh', 'sd',
          'sc', 'es', 'eh', 'ed', 'ec', 'ws', 'wh', 'wd', 'wc']


def makeOutputFilePath(num):
    return os.path.join('HandRecords', str(num) + 'Deals' + str(time.time().__trunc__()) + '.csv')

def dealToList(deal):
    [ns, nh, nd, nc, es, eh, ed, ec, ws, wh, wd, wc, ss, sh, sd, sc, trx] = deal.split()[1:34:2]
    return [trx, ns, nh, nd, nc, ss, sh, sd, sc, es, eh, ed, ec, ws, wh, wd, wc]

def makeAndFillDataframe(path, num_deals, result_queue):
    df = pd.DataFrame(columns=header, dtype="string")

    for _ in range(num_deals):
        result = subprocess.run(
            [f"./{path}", "-r", "-m 2", "-t", "N"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        lst = dealToList(result)
        df.loc[len(df)] = lst    
    result_queue.put(df)


def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()

def main():
    args = sys.argv
    if len(args) < 3:
        raise "Not enough arguments"
    repo = args[1]
    num_hands = int(args[2])
    if len(args) > 3:
        output_path = args[3]
    else:
        output_path = makeOutputFilePath(num_hands)
    path = os.path.join(repo, 'solver')

    result_queue = queue.Queue()
    hands_per_thread = int(num_hands/4)
    t1 = threading.Thread(target=makeAndFillDataframe,
                          args=(path, hands_per_thread, result_queue))
    t2 = threading.Thread(target=makeAndFillDataframe,
                          args=(path, hands_per_thread, result_queue))
    t3 = threading.Thread(target=makeAndFillDataframe,
                          args=(path, hands_per_thread, result_queue))
    t4 = threading.Thread(target=makeAndFillDataframe,
                          args=(path, hands_per_thread, result_queue))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()

    print(result_queue.qsize())

    output_df = pd.concat(
        [result_queue.get(), result_queue.get(), result_queue.get(), result_queue.get()], ignore_index=True)
    
    print(output_df)



    # df.to_csv(output_path, index_label="Index", header=header)

    print(f"Wrote csv to {output_path}")
    return output_path


if __name__ == "__main__":
    start_time = time.time()

    main()

    end_time = time.time()

    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)

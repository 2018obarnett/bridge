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
    start_time = time.time()

    df = pd.DataFrame(columns=header, dtype="string")

    for _ in range(num_deals):
        result = subprocess.run(
            [f"./{path}", "-r", "-m 2", "-t", "N"], stdout=subprocess.PIPE).stdout.decode('utf-8')
        lst = dealToList(result)
        df.loc[len(df)] = lst    
    result_queue.put(df)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("thread duration: ", elapsed_time)


def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()

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

import matplotlib.pyplot as plt
import math
import statistics
import numpy as np

def five_m(data_pool):
    avg = statistics.mean(data_pool)
    print("Mean Value is %f." % avg)

    mid = statistics.median(data_pool)
    print("Median Value is %f." % mid)

    min_v = min(data_pool)
    print("Minumum Value is %f" % min_v)

    max_v = max(data_pool)
    print("Maximum Value is %f" % max_v)

    std = statistics.stdev(data_pool)
    print("Standard Deviation is %f" % std)

if __name__ == '__main__':
    filepath = "../data/sampleDepartLarge.log"
    data_pool = []
    chosen = 100000
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            line_list = line.split("\t")
            if line_list[8] == "-" or line_list[11]=="REJ":
                continue
            data_pool.append(float(line_list[8]))
    # data_pool.sort()
    data_pool_log = [math.log(duration,10) for duration in data_pool]
    data_pool_log.sort()
    print(data_pool_log)

    total = len(data_pool_log)
    step = 0.01
    start = min(data_pool_log)
    end = max(data_pool_log)
    print(start, end)
    bins = {}
    cur = -2
    while cur < end:
        count = 0
        data_pool_log.sort()
        for duration in data_pool_log:
            if duration < cur:
                count += 1
                # data_pool.remove(duration)
            else:
                bins[cur] = count/total
                break
        cur += step
    print(bins)

    # for i in range(1, int(end)+1):
    #     y_data.append(y_data[i-1]+bins[i])
    #     # print(y_data)

    #plt.plot(bins.keys(),bins.values(), color="black", label="Campus NAT")
    plt.legend(loc="best")
    plt.ylabel("CDF")
    plt.xticks([-2, -1, 0, 1, 2, 3], [0.01, 0.1, 1, 10, 100, 1000])
    plt.xlabel("Session Duration (In Second).")
    # plt.show()


    five_m(data_pool)
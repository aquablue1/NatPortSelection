import matplotlib.pyplot as plt
from src.LogInfo import Output_Filename


def draw_simulation():
    x_data = []
    y_data = []
    Output_Filename = "../results_to_show/random/large/output.log"
    with open(Output_Filename) as f:
        for line in f:
            line = line.strip()
            line_list = line.split("\t")
            x_data.append(float(line_list[0]))
            y_data.append(int(line_list[1]))

    plt.scatter(x_data, y_data, marker="+", s=60, color="black", label="random")
    # plt.xlim()
    plt.ylim([52000, 57000])
    plt.xlim([650, 950])
    plt.xticks([650, 710, 770, 830, 890, 950], [0, 60, 120, 180, 240, 300])
    plt.xlabel("Time (in second).")
    plt.ylabel("Port Number.")
    plt.legend(loc="upper left")
    plt.show()


def draw_real():
    x_data = []
    y_data = []
    low_count = 0
    high_count = 0
    with open("../data/sampleResid.log") as f:
        for line in f:
            line = line.strip()
            line_list = line.split("\t")
            # if line_list[11]=="REJ":
                # continue
            x_data.append(float(line_list[0]))
            y_data.append(int(line_list[3]))
            if int(line_list[3]) < 49152:
                low_count += 1
            else:
                high_count += 1

    print("low_count %d." % low_count)
    print("high_count %d" % high_count)
    plt.scatter(x_data, y_data, marker="+", color="black",  s=60, label="Rejected Session Type I")
    # plt.ylim([0, 66500])
    plt.ylim([52000, 57000])
    plt.xlim([1518628700, 1518629000])    # For Large DataSet
    # plt.xlim([1518628000, 1518630000])    # For Medium DataSet
    # plt.legend(loc="upper left")
    plt.xlabel("Time (in second).")
    plt.ylabel("Port Number.")
    plt.legend(loc="upper left")
    plt.show()



if __name__ == '__main__':
    # draw_simulation()
    draw_real()

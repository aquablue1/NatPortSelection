import matplotlib.pyplot as plt
from src.LogInfo import Output_Filename


def draw_simulation():
    x_data = []
    y_data = []
    Output_Filename = "../results_to_show/sticky_random/large/output.log"
    with open(Output_Filename) as f:
        for line in f:
            line = line.strip()
            line_list = line.split("\t")
            x_data.append(float(line_list[0]))
            y_data.append(int(line_list[1]))

    plt.scatter(x_data, y_data, marker="+", s = 20, color="black", label="random")
    # plt.xlim()
    plt.ylim([48500, 66500])
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
    plt.scatter(x_data, y_data, marker="x", color="black",  s = 20, label="sticky-random")
    plt.ylim([0, 66500])
    # plt.legend(loc="upper left")
    plt.xlabel("Time (in second).")
    plt.ylabel("Port Number.")
    plt.legend(loc="upper left")
    plt.show()



if __name__ == '__main__':
    # draw_simulation()
    draw_real()

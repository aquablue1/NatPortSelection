import matplotlib.pyplot as plt
from src.LogInfo import Output_Filename

if __name__ == '__main__':
    x_data = []
    y_data = []
    with open(Output_Filename) as f:
        for line in f:
            line = line.strip()
            line_list = line.split("\t")
            x_data.append(float(line_list[0]))
            y_data.append(int(line_list[1]))

    plt.scatter(x_data, y_data, marker="+", color="black", label="Simulation")
    plt.legend(loc="upper left")
    plt.show()
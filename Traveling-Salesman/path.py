import matplotlib.pyplot as plt
import copy

# Return coordinates (x, y) of 48 US Capitals
def us_capitals():
    """
    https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html
    ATT48 is a set of 48 cities (US state capitals) from TSPLIB. The minimal tour has length 33523.
    """
    cities = []
    with open("./att48_xy.txt") as fp:
        for cnt, line in enumerate(fp):
            x, y = line.strip().split(" ")[0], line.strip().split(" ")[-1]
            cities.append((int(x), int(y)))
    return cities

# Returns the distance of the path across the points
def distance(points, path):
    total_distance = 0
    path_copy = copy.deepcopy(path)
    path_copy.append(path[0])
    for i in range(1, len(path_copy)):
        x_1 = points[path_copy[i-1]][0]
        y_1 = points[path_copy[i-1]][1]
        x_2 = points[path_copy[i]][0]
        y_2 = points[path_copy[i]][1]
        total_distance += pow((x_1 - x_2)**2 + (y_1 - y_2)**2, 0.5)
    return round(total_distance, 4)

# Plots the given path across the points
def plot_path(points, path):

    path_plt = copy.deepcopy(path)
    path_plt.append(path[0])

    x_points = [p[0] for p in points]
    y_points = [p[1] for p in points]
    plt.scatter(x_points, y_points, color = 'black')

    x_path = [x_points[p] for p in path_plt]
    y_path = [y_points[p] for p in path_plt]
    plt.plot(x_path, y_path, linestyle = '-', color = 'red')

    ax = plt.gca()
    ax.set_xlabel("x coordinate")
    ax.set_ylabel("y coordinate")
    plt.title(f"US Capitals ({distance(points, path)} miles)")

    plt.show()

if __name__ == "__main__":
    cities = us_capitals()
    path = [i for i in range(len(cities))]

    plot_path(cities, path)
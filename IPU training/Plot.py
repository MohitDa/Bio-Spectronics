import matplotlib.pyplot as plt
from time import sleep

class plot:
    def plot_graph(self, x = [],y = [], color_input = "red", title_input = ""):
        plt.title(title_input)
#         plt.ylim(0.5,1.3)
        plt.plot(x,y, color = color_input)
        plt.pause(0.01)

    def close_graph(self, time = 0):
        sleep(time)
        plt.close()

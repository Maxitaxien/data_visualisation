import os

import matplotlib.pyplot as plt
def test_plot():
    labels = [1, 2, 1, 1, 2]
    plt.plot(labels, range(len(labels)))

    save_path = 'static/plots/plot1.png'
    plt.savefig(save_path)
    plt.close()
    return save_path
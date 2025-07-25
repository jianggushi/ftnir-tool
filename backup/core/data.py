import matplotlib.pyplot as plt

def save_data_to_txt(data: list, filename: str):
    with open(filename, 'w') as f:
        for line in data:
            f.write(line + '\n')

def plot_data(x: list, y: list, title: str = '', xlabel: str = '', ylabel: str = ''):
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.show()
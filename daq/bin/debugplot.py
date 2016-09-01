import argparse
import numpy as np
import matplotlib.pyplot as plt

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str)
    return parser.parse_args()

def main():
    args = get_args()
    data = np.loadtxt(args.file, usecols=(1,3))
    tim, chan = [], []

    for pt in data:
        tim.append(pt[1])
        chan.append(int(pt[0]))

    plt.plot(tim, chan, '.')
    plt.show()

if __name__ == '__main__':
    main()

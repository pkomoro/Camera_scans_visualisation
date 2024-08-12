import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import pathlib

if __name__ == "__main__":

    # path to the folder containing .npy files
    path ="C:/Users/komor/OneDrive - Wojskowa Akademia Techniczna/Pomiary/NN-wideband_lens"

    name = "ref_"

    paths = [f for f in Path(path).glob(name + "*.npy")]

    print(paths)

    
    data = paths.copy()

    for i in range(len(paths)):
        data[i] = np.load(Path(paths[i]))

    for i in range(len(paths)):
        paths[i] = paths[i].absolute().as_posix()[:-4]

        
    focal_length = [0]*len(paths)
    focusing = [0]*len(paths)

    for i in range(len(paths)):
        
        max_values = np.max(data[i], axis=(1,2))
        focusing[i] = max_values / np.max(max_values)

        max_positions = np.argwhere(max_values==np.max(max_values)).flatten()

        focal_length[i] = 360 - (max_positions[0] + max_positions[-1])/2


    freqs = [150,160,170,180,190,200,210,220]

    fit = np.polyfit(freqs, focal_length, 1)
    line = np.poly1d(fit)

    print(fit)

    plt.xlabel('Frequency [GHz]')
    plt.ylabel('Focal length [mm]')
    plt.ylim(120,300)
    plt.scatter(freqs, focal_length, c = 'red')
    plt.plot(freqs, line(freqs))
    plt.savefig(path + '/' + name + 'focal_length.jpg', dpi = 1000)
    plt.savefig(path + '/' + name + 'focal_length.svg')

    z_range = [360 - number for number in range(len(focusing[0]))]    

    plt.clf()
    plt.xlabel('z [mm]')
    plt.ylabel('Maximal signal [a.u.]')
    for i in focusing:
        plt.plot(z_range, i)
    plt.legend(freqs)
    plt.savefig(path + '/' + name + 'focusing.jpg', dpi = 1000)
    plt.savefig(path + '/' + name + 'focusing.svg')
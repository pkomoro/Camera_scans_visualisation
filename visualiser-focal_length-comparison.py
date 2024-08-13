import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import pathlib

if __name__ == "__main__":

    # path to the folder containing .npy files
    path =""

    name = "NN"

    # list files

    paths = [f for f in Path(path).glob(name + "*.npy")]

    print(paths)
    
    data = paths.copy()

    # import files

    for i in range(len(paths)):
        data[i] = np.load(Path(paths[i]))

    # prepare file names

    for i in range(len(paths)):
        paths[i] = paths[i].absolute().as_posix()[:-4]

    
    # extract focal lengths from positions of maximal signal

    focal_length = [0]*len(paths)
    focusing = [0]*len(paths)

    for i in range(len(paths)):
        
        max_values = np.max(data[i], axis=(1,2))
        focusing[i] = max_values / np.max(max_values)

        max_positions = np.argwhere(max_values==np.max(max_values)).flatten()

        focal_length[i] = 360 - (max_positions[0] + max_positions[-1])/2


    # extract focal lengths from positions of number of bright pixels

  
    for i in range(len(paths)):
        bright_pixels = [0]*len(data[i])
        for j in range(len(data[i])):
            max_value = np.max(data[i][j])
            
            bright_pixels[j] = (data[i][j]>max_value/4).sum()

        min_positions = np.argwhere(bright_pixels==np.min(bright_pixels)).flatten()

        focal_length[i] = 360 - (min_positions[0] + min_positions[-1])/2

 

    freqs = [150,160,170,180,190,200,210,220]

    
    fit1 = np.polyfit(freqs, focal_length[:8], 1)
    line1 = np.poly1d(fit1)
    print(fit1)
    
    fit2 = np.polyfit(freqs, focal_length[8:], 1)
    line2 = np.poly1d(fit2)
    print(fit2)

    plt.xlabel('Frequency [GHz]')
    plt.ylabel('Focal length [mm]')
    plt.ylim(120,220)
    plt.scatter(freqs, focal_length[:8], c = 'red')
    plt.scatter(freqs, focal_length[8:], c = 'green')
    plt.plot(freqs, line1(freqs))
    plt.plot(freqs, line2(freqs))
    # plt.savefig(path + '/' + name + 'focal_length.jpg', dpi = 1000)
    # plt.savefig(path + '/' + name + 'focal_length.svg')

    plt.show()

    
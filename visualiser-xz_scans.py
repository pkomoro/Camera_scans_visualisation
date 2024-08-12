import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import pathlib

if __name__ == "__main__":

    # path to the folder containing .npy files
    path ="C:/Users/komor/OneDrive - Wojskowa Akademia Techniczna/Pomiary/NN-wideband_lens"

    
    paths = [f for f in Path(path).glob("*.npy")]

    
    data = paths.copy()

    for i in range(len(paths)):
        data[i] = np.load(Path(paths[i]))

    for i in range(len(paths)):
        paths[i] = paths[i].absolute().as_posix()[:-4]

        

    for i in range(len(paths)):
        image = np.swapaxes(data[i], 0, 2)

        y = 15

        plt.xlabel('z [mm]')
        plt.ylabel('x [mm]')
        plt.imshow(image[y,:,:], cmap='inferno')
        plt.savefig(paths[i] + '_xz_y' + str(y) + 'px.jpg', dpi = 1000)
        plt.savefig(paths[i] + '_xz_y' + str(y) + 'px.svg')

    
    
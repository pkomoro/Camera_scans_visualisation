import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import pathlib

if __name__ == "__main__":

    # path to the folder containing .npy files
    path ="C:/Users/komor/OneDrive - Wojskowa Akademia Techniczna/Pomiary/Łącze THz/Ogniska soczewek - kamera"

    
    paths = [f for f in Path(path).glob("*.npy")]

    print(paths)

    paths_meta = [f for f in Path(path).glob("*.meta")]
    
    data = paths.copy()

    data_meta = paths_meta.copy()

    for i in range(len(paths)):
        data[i] = np.load(Path(paths[i]))

        file = open(Path(paths_meta[i]), "r")
        data_meta[i] = file.read()
        file.close()

    for i in range(len(paths)):
        paths[i] = paths[i].absolute().as_posix()[:-4]

        

    for i in range(len(paths)):
        
        
        index = data_meta[i].find("Start Y")
        data_meta[i] = data_meta[i][(index+9):]

        index = data_meta[i].find("mm")
        y_start = float(data_meta[i][:(index-1)])

        index = data_meta[i].find("Stop Y")
        data_meta[i] = data_meta[i][(index+8):]

        index = data_meta[i].find("mm")
        y_stop = float(data_meta[i][:(index-1)])
        
        index = data_meta[i].find("Step Z")
        data_meta[i] = data_meta[i][(index+8):]

        index = data_meta[i].find("mm")
        z_step = float(data_meta[i][:(index-1)])

        index = data_meta[i].find("Start Z")
        data_meta[i] = data_meta[i][(index+9):]

        index = data_meta[i].find("mm")
        z_start = float(data_meta[i][:(index-1)])

        index = data_meta[i].find("Stop Z")
        data_meta[i] = data_meta[i][(index+8):]

        index = data_meta[i].find("mm")
        z_stop = float(data_meta[i][:(index-1)])



        image = np.swapaxes(data[i], 0, 2)
        image = np.flip(image,2)

        y = 0

        plt.xlabel('z [mm]')
        plt.ylabel('x [mm]')
        plt.imshow(image[int((y_stop-y_start)/1.5/2) + y,:,:], cmap='inferno', aspect = 'auto',extent=[301 - z_stop, 301 - z_start, y_start - (y_start + y_stop)/2, y_stop - (y_start + y_stop)/2])
        plt.savefig(paths[i] + '_xz_y' + str(y) + 'px.jpg', dpi = 300)
        plt.savefig(paths[i] + '_xz_y' + str(y) + 'px.svg')
        plt.close()

    
    
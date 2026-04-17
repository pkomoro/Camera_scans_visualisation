import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

if __name__ == "__main__":
    # path to the folder containing .npy files
    path ="C:/Users/komor/OneDrive - Wojskowa Akademia Techniczna/Pomiary/Łącze THz/Terasense 90 mW"

    # closest distance from the structure to the camera in [mm]
    distance = 10
    
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
        print(data[i].shape)

    data_copy = data[0].copy()

    

    
    data_copy[15] = data[2][0]
    data_copy[14] = data[1][2]
    data_copy[11] = data[1][1]
    data_copy[8] = data[1][0]
    

    np.save(paths[0] + '_merged.npy', data_copy)


    # for i in range(len(paths)):
    #     index = data_meta[i].find("Step Z")
    #     data_meta[i] = data_meta[i][(index+8):]

    #     index = data_meta[i].find("mm")
    #     z_step = float(data_meta[i][:(index-1)])

    #     index = data_meta[i].find("Start Z")
    #     data_meta[i] = data_meta[i][(index+9):]

    #     index = data_meta[i].find("mm")
    #     z_start = float(data_meta[i][:(index-1)])

    #     index = data_meta[i].find("Stop Z")
    #     data_meta[i] = data_meta[i][(index+8):]

    #     index = data_meta[i].find("mm")
    #     z_stop = float(data_meta[i][:(index-1)])

    #     # print(f"Step Z: {z_step}\n Start Z: {z_start}\n Stop Z: {z_stop}\n")

    #     for j in range(len(data[i])):
    #         z = 300 + distance - (z_start + j*z_step)

    #         plt.xlabel('x [mm]')
    #         plt.ylabel('y [mm]')
    #         plt.imshow(data[i][j,:,:], cmap='inferno')
    #         plt.savefig(paths[i] + '_xy_z' + str(z) + 'mm.jpg', dpi = 1000)
    #         plt.savefig(paths[i] + '_xy_z' + str(z) + 'mm.svg')


        
        


   
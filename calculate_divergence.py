import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import time
import multiprocessing
import itertools


if __name__ == "__main__":
    # path to the folder containing .npy files
    path ="C:/Users/komor/OneDrive - Wojskowa Akademia Techniczna/Pomiary/Łącze THz/Terasense 90 mW"

    # closest distance from the structure to the camera in [mm]
    distance = 175
    
    paths = [f for f in Path(path).glob("*.npy")]

    print(*paths, sep='\n')

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


    start_time = time.time()

                     
    radii = [np.zeros(len(data[i])) for i in range(len(data))]
    distances = [np.zeros(len(data[i])) for i in range(len(data))]

    

    for i in range(len(paths)):

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

        distances[i] = distance + 300 - z_start - np.arange(len(data[i]))*z_step

        for j in range(len(data[i])):           
            threshold = 1/np.e**2 * np.max(data[i][j])
            radii[i][j] = np.sqrt(np.sum(data[i][j] > threshold) * 2.25 / np.pi)

            

        
    radii = np.concatenate(radii)
    distances = np.concatenate(distances)

    # Fit a line to the data
    coefficients = np.polyfit(distances, radii, 1)
    fit_line = np.poly1d(coefficients)
    fitted_radii = fit_line(distances)
    angle_deg = np.degrees(np.arctan(coefficients[0]))

    print(f"Fitted line coefficients: {coefficients}")
    print(f"Divergence angle: {angle_deg:.2f} degrees")

    plt.figure()
    plt.plot(distances, radii, 'o-')
    plt.plot(distances, fitted_radii, 'r--', label=f'Fit: {angle_deg:.2f}°')
    plt.legend()
    plt.xlabel('Distance (mm)')
    plt.ylabel('Radius (mm)')
    plt.title('Divergence of the beam')
    
    plt.savefig(path + '/divergence_plot.jpg', dpi=1000, bbox_inches='tight')
    plt.savefig(path + '/divergence_plot.svg', bbox_inches='tight')

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds\n")
    

import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import pathlib

if __name__ == "__main__":

    # path to the folder containing .npy files
    path ="C:/Users/komor/OneDrive - Wojskowa Akademia Techniczna/Pomiary/Łącze THz/Ogniska soczewek - kamera"

    paths = [f for f in Path(path).glob("f300*.npy")]

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

    exposure_table = [1, 2.8, 6.3, 13, 28, 113, 226, 453, 906, 1813]
    y = 0

    fig, ax = plt.subplots()

    plt.xlabel('z [mm]')
    plt.ylabel('x [mm]')

    z0 = 1240
    
    ax.set_xlim(z0-300, z0)
    ax.set_ylim(-24, 24)

    ax.set_facecolor('black')

    radii = [np.zeros(len(data[i])) for i in range(len(data))]
    distances = [np.zeros(len(data[i])) for i in range(len(data))]

    for j in range(int(len(paths)/2)):

        for i in range(2):
            
            index = data_meta[2*j+i].find("Camera exposure setting:")
            data_meta[2*j+i] = data_meta[2*j+i][(index+25):]

            index = data_meta[2*j+i].find("Pixel size")
            exposure = int(data_meta[2*j+i][:(index-1)])

            index = data_meta[2*j+i].find("Start Y")
            data_meta[2*j+i] = data_meta[2*j+i][(index+9):]

            index = data_meta[2*j+i].find("mm")
            y_start = float(data_meta[2*j+i][:(index-1)])

            index = data_meta[2*j+i].find("Stop Y")
            data_meta[2*j+i] = data_meta[2*j+i][(index+8):]

            index = data_meta[2*j+i].find("mm")
            y_stop = float(data_meta[2*j+i][:(index-1)])

            index = data_meta[2*j+i].find("Step Z")
            data_meta[2*j+i] = data_meta[2*j+i][(index+8):]

            index = data_meta[2*j+i].find("mm")
            z_step = float(data_meta[2*j+i][:(index-1)])

            index = data_meta[2*j+i].find("Start Z")
            data_meta[2*j+i] = data_meta[2*j+i][(index+9):]

            index = data_meta[2*j+i].find("mm")
            z_start = float(data_meta[2*j+i][:(index-1)])

            index = data_meta[2*j+i].find("Stop Z")
            data_meta[2*j+i] = data_meta[2*j+i][(index+8):]

            index = data_meta[2*j+i].find("mm")
            z_stop = float(data_meta[2*j+i][:(index-1)])

            if "1710mm" in paths[2*j+i]:
                z_start += 300
                z_stop += 300


            image = np.swapaxes(data[2*j+i], 0, 2)
            image = np.flip(image,2)

            vmax = exposure_table[exposure]
            vmax = np.max(data)

        
            plt.imshow(image[int((y_stop-y_start)/1.5/2) + y,:,:], cmap='inferno', aspect = 'auto',
                    extent=[z0 + 300 - z_stop, z0 + 300 - z_start, y_start - (y_start + y_stop)/2, y_stop - (y_start + y_stop)/2], vmin = 0, vmax = vmax)

            distances[2*j+i] = z0 + 300 - z_start - np.arange(len(data[i]))*z_step

        

            for k in range(len(data[2*j+i])):           
                threshold = 1/np.e**2 * np.max(data[2*j+i][k])
                radii[2*j+i][k] = np.sqrt(np.sum(data[2*j+i][k] > threshold) * 2.25 / np.pi)
            
        plt.savefig(paths[2*j] + '_xz_y' + str(y) + 'px_merged.jpg', dpi = 300, bbox_inches='tight')
        # plt.savefig(paths[2*j] + '_xz_y' + str(y) + 'px_merged.svg')
        plt.close()

        radii_plot = np.concatenate(radii[2*j:2*j+1])
        distances_plot = np.concatenate(distances[2*j:2*j+1])

        # print(radii_plot)
        # print(distances_plot)

        # Fit a line to the data
        coefficients = np.polyfit(distances_plot, radii_plot, 2)
        fit_line = np.poly1d(coefficients)
        fitted_radii = fit_line(distances_plot)
        # angle_deg = np.degrees(np.arctan(coefficients[0]))

        plt.figure()
        plt.plot(distances_plot, radii_plot, 'o-')
        # plt.plot(distances_plot, fitted_radii, 'r--', label=f'Fit: {angle_deg:.2f}°')
        plt.plot(distances_plot, fitted_radii, 'r--')
        plt.legend()
        plt.xlabel('Distance (mm)')
        plt.ylabel('Radius (mm)')
        plt.title('Divergence of the beam')
    
        plt.savefig(paths[2*j] + '_divergence_plot.jpg', dpi=300, bbox_inches='tight')
        # plt.savefig(paths[2*j] + '_divergence_plot.svg', bbox_inches='tight')
        plt.close()

        
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
import pathlib
import re

if __name__ == "__main__":

    # path to the folder containing .npy files
    path ="C:/Users/komor/OneDrive - Wojskowa Akademia Techniczna/Pomiary/Łącze THz/Ogniska soczewek - kamera"

    paths = [f for f in Path(path).glob("f180*.npy")]

    # print(*paths, sep='\n')

    ploting = False

    l = 3.14  # mm, wavelength of the beam
    w0 = 6.84  # mm, beam waist radius
    

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

    

    ax.set_facecolor('black')

    radii = [np.zeros(len(data[i])) for i in range(len(data))]
    distances = [np.zeros(len(data[i])) for i in range(len(data))]

    image_positions = [0 for i in range(len(data))]
    object_positions = [0 for i in range(len(data))]

    for j in range(len(paths)):
            
        match = re.search(r"lens_d(\d{3})", Path(paths[j]).name)
        lens_d = int(match.group(1)) if match else None

        print(f"Processing {paths[j]} with lens diameter {lens_d} mm")

        z0 = 450 - lens_d + 210
        
        index = data_meta[j].find("Camera exposure setting:")
        data_meta[j] = data_meta[j][(index+25):]

        index = data_meta[j].find("Pixel size")
        exposure = int(data_meta[j][:(index-1)])

        index = data_meta[j].find("Start Y")
        data_meta[j] = data_meta[j][(index+9):]

        index = data_meta[j].find("mm")
        y_start = float(data_meta[j][:(index-1)])

        index = data_meta[j].find("Stop Y")
        data_meta[j] = data_meta[j][(index+8):]

        index = data_meta[j].find("mm")
        y_stop = float(data_meta[j][:(index-1)])

        index = data_meta[j].find("Step Z")
        data_meta[j] = data_meta[j][(index+8):]

        index = data_meta[j].find("mm")
        z_step = float(data_meta[j][:(index-1)])

        index = data_meta[j].find("Start Z")
        data_meta[j] = data_meta[j][(index+9):]

        index = data_meta[j].find("mm")
        z_start = float(data_meta[j][:(index-1)])

        index = data_meta[j].find("Stop Z")
        data_meta[j] = data_meta[j][(index+8):]

        index = data_meta[j].find("mm")
        z_stop = float(data_meta[j][:(index-1)])

        

        image = np.swapaxes(data[j], 0, 2)
        image = np.flip(image,2)

        vmax = exposure_table[exposure]
        vmax = np.max(data)

        if ploting:
            plt.imshow(image[int((y_stop-y_start)/1.5/2) + y,:,:], cmap='inferno', aspect = 'auto',
                    extent=[z0 + 300 - z_stop, z0 + 300 - z_start, y_start - (y_start + y_stop)/2, y_stop - (y_start + y_stop)/2], vmin = 0, vmax = vmax)

        distances[j] = z0 + 300 - z_start - np.arange(len(data[j]))*z_step

        ax.set_xlim(z0, z0+300)
        ax.set_ylim(-24, 24)

        for k in range(len(data[j])):           
            threshold = 1/np.e**2 * np.max(data[j][k])
            radii[j][k] = np.sqrt(np.sum(data[j][k] > threshold) * 2.25 / np.pi)
            
        
        if ploting:
            plt.savefig(paths[j] + '_xz_y' + str(y) + 'px_merged.jpg', dpi = 300, bbox_inches='tight')
            # plt.savefig(paths[2*j] + '_xz_y' + str(y) + 'px_merged.svg')
            plt.close()

        

        # Fit a line to the data
        coefficients = np.polyfit(distances[j], radii[j], 5)
        fit_line = np.poly1d(coefficients)
        fitted_radii = fit_line(distances[j])
        # angle_deg = np.degrees(np.arctan(coefficients[0]))

        image_positions[j] = distances[j][np.argmin(fitted_radii)]
        object_positions[j] = 570 - z0

        
        if ploting:
            plt.figure()
            plt.plot(distances[j], radii[j], 'o-')
            # plt.plot(distances[j], fitted_radii, 'r--', label=f'Fit: {angle_deg:.2f}°')
            plt.plot(distances[j], fitted_radii, 'r--')
            # plt.legend()
            plt.xlabel('Distance (mm)')
            plt.ylabel('Radius (mm)')
            plt.title('Divergence of the beam')
    
            plt.savefig(paths[j] + '_divergence_plot.jpg', dpi=300, bbox_inches='tight')
            # plt.savefig(paths[2*j] + '_divergence_plot.svg', bbox_inches='tight')
            plt.close()

   


    # Calculate theoretical object positions using lens equation: 1/f = 1/u + 1/v
    # where u is object distance, v is image distance, f is focal length
    focal_length = 180  # mm, adjust based on your lens

    def thin_lens_equation(u, f):
        return 1 / (1 / f - 1 / u)
    
    def gaussian_lens_equation(s, f, w0, l):
        return 1 / (1 / f - 1 / (s + (np.pi * w0**2 / l)**2 / (s + f)))
    
    
    object_distances = np.linspace(np.min(object_positions), np.max(object_positions), 100)  # mm, range of object distances to consider
    theoretical_image_positions = thin_lens_equation(object_distances, focal_length)
    theoretical_image_positions_gaussian = gaussian_lens_equation(object_distances, focal_length, w0, l)
        
    # Plot comparison
    plt.figure(figsize=(10, 6))
    plt.plot(object_positions, image_positions, 'o-', label='Experimental', linewidth=2, markersize=8)
    plt.plot(object_distances, theoretical_image_positions, 'r--', label='Thin lens equation', linewidth=2)
    plt.plot(object_distances, theoretical_image_positions_gaussian, 'g--', label='Gaussian beam', linewidth=2)
    plt.xlabel('Object Distance (mm)')
    plt.ylabel('Image Distance (mm)')
    plt.title('Object Positions: Experimental vs Theoretical')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(Path(path) / 'object_positions_comparison.jpg', dpi=300, bbox_inches='tight')
    plt.close()
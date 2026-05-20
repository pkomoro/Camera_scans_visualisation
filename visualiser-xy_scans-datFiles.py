import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path

if __name__ == "__main__":
    # path to the folder containing .npy files
    path ="C:/Users/komor/OneDrive - Wojskowa Akademia Techniczna/Pomiary/Światłowody terahercowe UW/seria 2"
    
    
    
    paths = [f for f in Path(path).glob('**/*.dat')]    
    data = []

    for file_path in paths:
        with open(file_path, "r") as f:
            lines = f.readlines()[2:]  # skip first two lines
            matrix = np.array([list(map(float, line.strip().split(','))) for line in lines])
            data.append(matrix)


    for i in range(len(paths)):
        paths[i] = paths[i].absolute().as_posix()[:-4]

    
    for i in range(len(paths)):
        
        plt.xlabel('x [mm]')
        plt.ylabel('y [mm]')
        plt.imshow(data[i], cmap='inferno')
        plt.savefig(paths[i] + '_xy.jpg', dpi = 1000)
        plt.savefig(paths[i] + '_xy.svg')

    with open(path + "summary.txt", "w") as summary_file:
        for i in range(len(paths)):
            total_value = np.sum(data[i])
            summary_file.write(f"{paths[i]}: {total_value}\n")
    

   
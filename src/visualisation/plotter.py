import matplotlib
matplotlib.use('Agg')  # Use the Agg backend
import os
import math
import numpy as np
import subprocess
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from multiprocessing import Pool

from calculations.orbital_mechanics import distance

def blackout(fig, ax, grid=True):

    fig.set_facecolor('black')
    ax.set_facecolor('black')

    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')

    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.set_ticklabels([])

    if grid:
        ax.grid(True)

        # hide the axes themselves
        ax.xaxis.set_visible(True)
        ax.yaxis.set_visible(True)
        ax.zaxis.set_visible(True)

    else:
        ax.grid(False)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.zaxis.set_visible(False)

    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.zaxis.pane.set_edgecolor('black')

    return fig, ax

def get_fig_ax(trail, object_1, object_2):

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')

    fig, ax = blackout(fig, ax)

    # Calculate min and max values for x, y, and z from both objects' trajectories
    x_vals = [x for x, _, _ in object_1.trajectory] + [x for x, _, _ in object_2.trajectory]
    y_vals = [y for _, y, _ in object_1.trajectory] + [y for _, y, _ in object_2.trajectory]
    z_vals = [z for _, _, z in object_1.trajectory] + [z for _, _, z in object_2.trajectory]

    xmin, xmax = min(x_vals), max(x_vals)
    ymin, ymax = min(y_vals), max(y_vals)
    zmin, zmax = min(z_vals), max(z_vals)

    padding = 0
    ax.set_xlim([xmin - padding, xmax + padding])
    ax.set_ylim([ymin - padding, ymax + padding])
    ax.set_zlim([zmin - padding, zmax + padding])

    return fig, ax

def plot_3d_scatter(object1, object2):

    fig, ax = get_fig_ax()
    fig, ax = blackout(fig, ax)

    # Unpack positions from trajectories
    x1, y1, z1 = zip(*object1.trajectory)
    x2, y2, z2 = zip(*object2.trajectory)

    # Number of points in each trajectory
    num_points1 = len(object1.trajectory)
    num_points2 = len(object2.trajectory)

    # Create a color range based on the index of each point in the trajectory
    colors1 = cm.magma(range(num_points1))
    colors2 = cm.viridis(range(num_points2))

    # Plotting with sizes based on the radius of the objects and color map for time progression
    ax.scatter(x1, y1, z1, s=object1.radius * 0.01, c=colors1, label=f'{object1.object_type} 1')
    ax.scatter(x2, y2, z2, s=object2.radius * 0.01, c=colors2, label=f'{object2.object_type} 2')

    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')
    plt.title("3D Trajectories of Black Holes")
    plt.legend()

    plt.show()

    plt.savefig('../figures/cbc_merger.png', dpi=50)

def plot_3d_scatter_animation(object_1, object_2, trail=False):

    trajectory_length = len(object_1.trajectory)
    colours_1 = cm.magma(range(trajectory_length))
    colours_2 = cm.viridis(range(trajectory_length))

    frames_dir = 'animation_frames'
    os.makedirs(frames_dir, exist_ok=True)

    # Determine number of workers and divide work
    num_workers = (os.cpu_count() - 1)  # or os.cpu_count() to use all available CPU cores
    frame_ranges = np.array_split(range(trajectory_length), num_workers)

    if trail:
        with Pool(num_workers) as pool:
            tasks = [(frame_range, object_1, object_2, trail, frames_dir) for frame_range in frame_ranges]
            list(tqdm(pool.imap_unordered(worker_with_trail, tasks), total=len(tasks), desc='Generating frame'))
    else:
        with Pool(num_workers) as pool:
            tasks = [(frame_range, object_1, object_2, trail, frames_dir) for frame_range in frame_ranges]
            list(tqdm(pool.imap_unordered(worker, tasks), total=len(tasks), desc="Generating frames"))

    # Use FFmpeg to combine frames into a video with GPU acceleration
    ffmpeg_command = [
        'ffmpeg',
        '-r', str(30),  # frame rate
        '-i', f'{frames_dir}/frame_%04d.png',
        '-c:v', 'h264_nvenc',  # for NVIDIA GPU
        '-preset', 'fast',
        '../figures/cbc_merger_animation.mp4'
    ]
    subprocess.run(ffmpeg_command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    # Clean up frames
    for file in os.listdir(frames_dir):
        os.remove(os.path.join(frames_dir, file))
    os.rmdir(frames_dir)

def worker(args):
    
    # Unpack args passed to worker function
    frame_range, object_1, object_2, trail, frames_dir = args
    for frame in frame_range:
        # Create new figure and axis for frame
        fig, ax = get_fig_ax(trail, object_1, object_2)

        # Get coorindates corresponding to the frame
        x1, y1, z1 = object_1.trajectory[frame]
        x2, y2, z2 = object_2.trajectory[frame]

        # Plot 3d scatter for both objects
        ax.scatter(x1, y1, z1, s=object_1.radius * 0.1, c='blue')
        ax.scatter(x2, y2, z2, s=object_2.radius * 0.1, c='red')

        # Save fig and free up memory
        plt.savefig(f'{frames_dir}/frame_{frame:04d}.png', dpi=200)
        plt.close(fig)

def worker_with_trail(args):

    # Unpacking arguments passed to the worker function
    frame_range, object_1, object_2, trail, frames_dir = args

    # Setting the maximum number of points to be plotted in the trail
    max_points = 20  

    # Generating colour maps for the maximum number of points in the trail
    colours_1 = cm.magma(np.linspace(0, 1, max_points))
    colours_2 = cm.viridis(np.linspace(0, 1, max_points))

    for frame in frame_range:
        # Create a new figure and axis for each frame
        fig, ax = get_fig_ax(trail, object_1, object_2)
        plt.title(f'CBC Merger', color='white', fontsize=12)

        # Calculate the start index for slicing the trajectory. It ensures that only the last 'max_points' are considered
        start_idx_1 = max(0, frame + 1 - max_points)
        start_idx_2 = max(0, frame + 1 - max_points)

        # Extracting the coordinates for the specified range from the trajectories of both objects
        x1, y1, z1 = zip(*object_1.trajectory[start_idx_1:frame+1])
        x2, y2, z2 = zip(*object_2.trajectory[start_idx_2:frame+1])

        # Determining the number of points currently being plotted
        num_points_1 = len(x1)
        num_points_2 = len(x2)

        # Slicing the colour maps to match the number of points being plotted
        colour_1 = colours_1[:num_points_1]
        colour_2 = colours_2[:num_points_2]

        # Plotting the points for each object with their respective colours and sizes
        ax.scatter(x1, y1, z1, s=object_1.radius * 0.01, c=colour_1, alpha=1, label=(f'{object_1.object_type} Mass: {object_1.mass}'))
        ax.scatter(x2, y2, z2, s=object_2.radius * 0.01, c=colour_2, alpha=1, label=(f'{object_2.object_type} Mass: {object_2.mass}'))

        legend = ax.legend(facecolor='darkgrey', loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, fontsize='small')
        plt.setp(legend.get_texts(), color='black')

        # Saving the figure to a file and then closing it to free up memory
        plt.savefig(f'{frames_dir}/frame_{frame:04d}.png', dpi=200)
        plt.close(fig)

def mp4_to_gif(mp4_path, gif_path):
    try:
        command = [
            'ffmpeg',
            '-i', mp4_path,  # Input file
            '-filter_complex', '[0:v] fps=10,scale=w=480:h=-1,split [a][b];[a] palettegen [p];[b][p] paletteuse',
            '-loop', str(0),  # Loop count
            '-f', 'gif',  # Output format
            gif_path  # Output file
        ]

        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(f"Conversion completed: '{mp4_path}' to '{gif_path}'")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}")



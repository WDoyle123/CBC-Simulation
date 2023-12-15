import os
import subprocess
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

def blackout(fig, ax):

    fig.set_facecolor('black')
    ax.set_facecolor('black')

    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_zlabel('')

    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.set_ticklabels([])

    ax.grid(False)

    # hide tick labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # hide the axes themselves
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

def get_fig_ax():

    fig = plt.figure(figsize=(4, 4))
    ax = fig.add_subplot(111, projection='3d')

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

def plot_3d_scatter_animation(object_1, object_2):

    fig, ax = get_fig_ax()
    #fig, ax = blackout(fig, ax)

    trajectory_length = len(object_1.trajectory)

    # Initialise scatter plots
    scatter_1 = ax.scatter([], [], [], s=object_1.radius * 0.1, c='blue', label=f'{object_1.object_type} 1')
    scatter_2 = ax.scatter([], [], [], s=object_2.radius * 0.1, c='red', label=f'{object_2.object_type} 2')

    def update(frame):
        x1, y1, z1 = zip(*object_1.trajectory[:frame+1])
        x2, y2, z2 = zip(*object_2.trajectory[:frame+1])

        ax.clear()  # Clear previous data
        ax.scatter(x1, y1, z1, s=object_1.radius * 0.1, c='blue', label=f'{object_1.object_type} 1')
        ax.scatter(x2, y2, z2, s=object_2.radius * 0.1, c='red', label=f'{object_2.object_type} 2')

        # Re-apply labels and other formatting if needed
        plt.title('CBC Merger')
        plt.legend()

    # Directory for saving frames
    frames_dir = 'animation_frames'
    os.makedirs(frames_dir, exist_ok=True)

    # Function to update and save each frame
    def update_and_save(frame):
        update(frame)
        plt.savefig(f'{frames_dir}/frame_{frame:04d}.png')

    # Generate and save frames
    for frame in tqdm(range(trajectory_length), desc="Generating frames"):
        update_and_save(frame)

    # Use FFmpeg to combine frames into a video with GPU acceleration
    ffmpeg_command = [
        'ffmpeg',
        '-r', str(60),  # Example frame rate
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

def update_frame(frame):

    x1, y1, z1 = zip(*object_1.trajectory[i])
    x2, y2, z2 = zip(*object_2.trajectory[i])

    ax.scatter(x1, y1, z1, s=object_1.radius * 0.1, c='blue', label=f'{object_1.object_type} 1')
    ax.scatter(x2, y2, z2, s=object_2.radius * 0.1, c='red', label=f'{object_2.object_type} 2')

    plt.title('CBC Meger')
    plt.legend()


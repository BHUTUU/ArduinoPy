import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import pyfirmata

# Arduino board settings
board_port = 'COM2'  # Replace with your Arduino serial port
baud_rate = 9600

# Initialize empty lists to store data
x_data = []
y_data = []

# Create a figure for the plot
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(1, 1, 1)

# Set the axis labels and title
ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_title('Serial Plotter')

# Create an empty line object with markers for the plot
line, = ax.plot(x_data, y_data, marker='o')

# Function to update the graph with new data
def update_graph():
    # Initialize the Arduino board
    board = pyfirmata.Arduino(board_port)

    # Set up an iterator to read analog input
    it = pyfirmata.util.Iterator(board)
    it.start()

    # Define the analog input pin
    analog_input_pin = board.analog[0]

    # Read and process the analog data
    while True:
        try:
            value = analog_input_pin.read()

            # Skip None values
            if value is None:
                continue

            # Update the data
            x_data.append(len(x_data) + 1)
            y_data.append(value)

            # Update the line object
            line.set_data(x_data, y_data)

            # Adjust the plot limits if needed
            ax.relim()
            ax.autoscale_view()

        except ValueError:
            # Skip lines that don't contain valid data
            continue

        # Redraw the plot
        fig.canvas.draw()

    # Close the Arduino board connection
    board.exit()

# Function to start the serial plotter
def start_serial_plotter():
    # Start a separate thread to read serial data and update the plot
    threading.Thread(target=update_graph).start()

# Create the main window
window = tk.Tk()
window.title('Serial Plotter')

# Create a canvas to display the plot
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Create a button to start the serial plotter
start_button = tk.Button(window, text='Start', command=start_serial_plotter)
start_button.pack()

# Start the Tkinter event loop
window.mainloop()

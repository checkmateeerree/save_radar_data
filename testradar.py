
import serial
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import time
import serial.tools.list_ports
import os.path
import argparse
import json

def find_arduino_com_port(ports):
    #finds COM port that the Arduino is on (assumes only one Arduino is connected)
    for port in ports:
        # port.Name, port.DeviceID, port.Name properties
        if "COM" in port.description:
            comPort = port.name
    
    try:      
        if comPort:      
            return comPort
    except:
        return None

def connect(ser):
    connected = False
    
    while not connected:
        serin = ser.read()
        connected = True

    print("connected!")
    return

def collect_data(length, ser):
    
    x = []    #speed
    y = []    #Doppler level
    z = []    # Doppler Frequency

    while len(x) <= length:     #while you are taking data
        data = ser.readline()    #reads until it gets a carriage return. MAKE SURE THERE IS A CARRIAGE RETURN OR IT READS FOREVER
        sep = data.split()
        sep = [i.decode() for i in sep]
        
        if len(sep) == 0:
            continue
        
        x.append(float(sep[0])) 
        y.append(float(sep[1]))
        z.append(float(sep[2]))
        
        time.sleep(0.1)
    
    return x, y, z

def graph_data(x, y, z, type_of_data):

    gs = gridspec.GridSpec(2, 2)
    fig = plt.figure()
    
    ax1 = fig.add_subplot(gs[0, 0]) # row 0, col 0
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :]) 

    ax1_x_ticks = np.arange(0, len(x))
    ax1_y_ticks = np.arange(0, max(x) + 1, 1)
    ax2_x_ticks = np.arange(0, len(y))
    ax2_y_ticks = np.arange(0, max(y) + 200, 200)
    ax3_x_ticks = np.arange(0, len(z))
    ax3_y_ticks = np.arange(0, max(z) + 10, 50)
    
    plot_graph(ax1, x, "Speed (m/s)", f"Speed of {type_of_data}", ax1_x_ticks, ax1_y_ticks)
    plot_graph(ax2, y, "Doppler Level", f"Doppler Level of {type_of_data}", ax2_x_ticks, ax2_y_ticks)
    plot_graph(ax3, z, "Doppler Frequency", f"Doppler Frequency of {type_of_data}", ax3_x_ticks, ax3_y_ticks)
    
    fig.tight_layout()

    return fig

def plot_graph(ax, data, ylabel, title, xticks, yticks):
    ax.plot(data)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)

def make_directory_to_save_data(type_of_data):
    base_dir = "./" + type_of_data + "Testing/"
    prefix_new_dir = "Test_"

    with open(f"{base_dir}test_num.json", "r+") as test_num_file:
        test_num_dict = json.load(test_num_file)
        test_num = test_num_dict["test_num"] + 1
        
        test_num_dict["test_num"] = test_num
        print(test_num_dict)
        json_dump_data = json.dumps(test_num_dict)
        
        test_num_file.seek(0)
        test_num_file.truncate()
        test_num_file.write(json_dump_data)

    test_num = str(test_num)
    
    new_dir = base_dir + prefix_new_dir + test_num

    os.mkdir(new_dir)
    
    return new_dir
    
def save_graph_data(fig, new_dir):
    fig.savefig(new_dir + "/graph.png")
    print(f"saved graph data to {new_dir}/graph.png")
    return
    
def save_num_data(x, y, z, new_dir):
    rows = list(zip(x, y, z))
    
    with open(new_dir + "/data.txt", "w") as data_file:
        data_file.write("Speed \t Doppler Level \t Doppler Frequency \n")
        for line in rows:
            for i in line:
                data_file.write(str(i) + " ")
            data_file.write("\n")   
            
        
    print(f"saved num data to {new_dir}/data.txt")
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Capture Arduino Serial data and graph it, and store the data.')
    parser.add_argument('--length', type=int,
                    help='number of data points you want to collect')
    parser.add_argument('--type', choices=['car', 'biker', 'walker'],
                        help='three options: car, biker, or walker')
    parser.add_argument('--delete_last', action="store_true",
                        help='''delete last testing data stored, 
                                if there's something wrong with it.
                            ''')

    args = parser.parse_args()
    
    if not (args.length and args.type):
        parser.error('Error, please provide --length and --type arguments')
    elif args.delete_last and args.type:
        #add functionality so u delete last
        #experiment of type specified
        exit()
    elif args.delete_last and (not args.type):
        parser.error("Error, please provide --type of testing data you want to delete")
    length = args.length
    type_of_data = args.type
        
    ports = serial.tools.list_ports.comports()
    arduino_com_port = find_arduino_com_port(ports)

    ser = serial.Serial(arduino_com_port, 115200, timeout=0.05) #sets up serial connection (make sure baud rate is correct - matches Arduino)

    connect(ser)
    
    new_dir = make_directory_to_save_data(type_of_data)
        
    speed_measurements, dop_lvl_measurements, dop_freq_measurements = collect_data(length, ser)

    fig = graph_data(speed_measurements,dop_lvl_measurements,dop_freq_measurements, type_of_data)
        
    save_graph_data(fig, new_dir)
    save_num_data(speed_measurements, dop_lvl_measurements, dop_freq_measurements, new_dir)

    ser.close() #closes serial connection (very important to do this! if you have an error partway through the code, type this into the cmd line to close the connection)
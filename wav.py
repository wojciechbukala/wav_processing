import struct
import matplotlib.pyplot as plt
import numpy as np
def load_audio(file_path):
    with open(file_path,'rb') as audio_file:
        # Getting the audio file parameters
        # Read the header to get audio file information
        
        header = audio_file.read(44) # In WAV files, first 44 bytes are reserved for the header
        print(f"The header is {header}")        
        if header[:4] != b'RIFF' or header[8:12] != b'WAVE' or header[12:16] != b'fmt ':
            raise ValueError("Invalid WAV file")
            
        # Extract relevant information from the header
        header_chunk_id = struct.unpack('4s', header[0:4])[0]
        header_chunk_size = struct.unpack('<I', header[4:8])[0]
        header_chunk_format = struct.unpack('4s', header[8:12])[0]
        format_chunk_id = struct.unpack('4s', header[12:16])[0]
        format_chunk_size = struct.unpack('<I', header[16:20])[0]
        format_code = struct.unpack('<H', header[20:22])[0]
        channels = struct.unpack('<H', header[22:24])[0]
        sample_rate = struct.unpack('<I', header[24:28])[0]
        byte_rate = struct.unpack('<I', header[28:32])[0]
        block_align = struct.unpack('<H', header[32:34])[0]
        sample_width = struct.unpack('<H', header[34:36])[0]
        data_chunk_id = struct.unpack('4s', header[36:40])[0]
        data_chunk_size = struct.unpack('<I', header[40:44])[0]
        
        # Read the data from the file
        audio_file.seek(44)
        data = audio_file.read(data_chunk_size)
    
    # Converting the raw binary data to a list of integers : 
    typ = { 1: np.int8, 2: np.int16, 4: np.int32 }.get(sample_width/8)
    print(typ)
    data_array = np.frombuffer(data, dtype=typ)
    # Convert to float32
    data_array = data_array.astype(np.float32)
    
    return header_chunk_id, header_chunk_size, header_chunk_format, format_chunk_id, format_chunk_size, data_array, format_code, channels, sample_width, sample_rate, byte_rate, block_align, data_chunk_id, data_chunk_size

file_name = "./M1F1-int32-AFsp.wav"
header_chunk_id , header_chunk_size, header_chunk_format, format_chunk_id, format_chunk_size, audio_data, format_code, channels, sample_width, sample_rate, byte_rate, block_align, data_chunk_id, data_chunk_size = load_audio(file_name)

print("HEADER CHUNK :----- \n")
print(f"Header Chunk ID : {header_chunk_id}")
print(f"Header Chunk Size : {header_chunk_size}")
print(f"Header Chunk Format : {header_chunk_format}")
print("FORMAT CHUNK :----- \n")
print(f"Format Chunk ID : {format_chunk_id}")
print(f"Format Chunk Size : {format_chunk_size}")
print(f"Format Code: {format_code}")
print(f"Number of Channels: {channels}")
print(f"Sample Rate: {sample_rate}")
print(f"Byte Rate : {byte_rate}")
print(f"Block align : {block_align}")
print(f"Sample Width: {sample_width}")
print(f"Number of Samples: {len(audio_data)}")
print("DATA CHUNK :----- \n")
print(f"Data Chunk ID : {data_chunk_id}")
print(f"Data Size : {data_chunk_size}")
print(f"Data : {audio_data}")
print(f"Type of data array : {type(audio_data[0])}")

t = np.arange(len(audio_data)/channels)/(sample_rate)

if channels == 1: 
    plt.figure(figsize=(12,2))

# plt.subplot(2,1)
    plt.plot(t,audio_data,color=[0,0,0],linewidth=0.5)
    plt.xlim(0, len(audio_data)/sample_rate)
    plt.ylabel('Left chh')
    plt.grid()

    plt.show()

if channels == 2:
    data_chan = [audio_data[offset::channels] for offset in range(channels)]
    for i in range(channels):
        if len(data_chan[i])!= len(t):
            data_chan[i] = np.append( data_chan[i], np.empty(len(t) - len(data_chan[i])))

    plt.figure(figsize=(12,4))

    plt.subplot(2,1,1)
    plt.plot(t,data_chan[0],color=[0,0,0],linewidth=0.5)
    plt.xlim(0, len(audio_data)/(channels*sample_rate))
    plt.xticks(ticks=[])
    plt.ylabel('Left ch')
    plt.grid()

    plt.subplot(2,1,2)
    plt.plot(t,data_chan[1],color=[0,0,0],linewidth=0.5)
    plt.xlim(0, len(audio_data)/(channels*sample_rate))
    plt.ylabel('Rigth ch')
    plt.grid()

    plt.show()
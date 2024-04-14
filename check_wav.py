import struct
import matplotlib.pyplot as plt
import numpy as np

class Check_wav:
    def __init__(self, file_path):
        self.file_path = file_path
        self.load_audio()

    def load_audio(self):
        with open(self.file_path,'rb') as audio_file:
            # Getting the audio file parameters
            # Read the header to get audio file information
            
            self.header = audio_file.read(44) # In WAV files, first 44 bytes are reserved for the header
            #print(f"The header is {self.header}\n")        
            if self.header[:4] != b'RIFF' or self.header[8:12] != b'WAVE' or self.header[12:16] != b'fmt ':
                raise ValueError("Invalid WAV file")
                
            # Extract relevant information from the header
            self.header_chunk_id = struct.unpack('4s', self.header[0:4])[0]
            self.file_size = struct.unpack('<I', self.header[4:8])[0]
            self.header_chunk_format = struct.unpack('4s', self.header[8:12])[0]
            self.format_chunk_id = struct.unpack('4s', self.header[12:16])[0]
            self.format_chunk_size = struct.unpack('<I', self.header[16:20])[0]
            self.format_code = struct.unpack('<H', self.header[20:22])[0]
            self.channels = struct.unpack('<H', self.header[22:24])[0]
            self.sample_rate = struct.unpack('<I', self.header[24:28])[0]
            self.byte_rate = struct.unpack('<I', self.header[28:32])[0]
            self.block_align = struct.unpack('<H', self.header[32:34])[0]
            self.sample_width = struct.unpack('<H', self.header[34:36])[0]
            self.data_chunk_id = struct.unpack('4s', self.header[36:40])[0]
            self.data_chunk_size = struct.unpack('<I', self.header[40:44])[0]            
            
            # Read the data from the file
            audio_file.seek(44)
            data = audio_file.read(self.data_chunk_size)

            # Check for additional chunks
            self.add_chunks = b''
            add_chunk_id = 0
            add_data_id = self.data_chunk_size + 44
            audio_file.seek(add_data_id)
            add_data = audio_file.read()
            print(add_data)

            while add_data_id + add_chunk_id + 8 <= len(add_data):  # Ensure enough bytes left for 8-byte chunk header
                chunk_id = struct.unpack('4s', add_data[0 + add_chunk_id:4 + add_chunk_id])[0]
                self.add_chunks += chunk_id + b' '
                
                chunk_size = struct.unpack('<I', add_data[4 + add_chunk_id:8 + add_chunk_id])[0]
                
                print(add_data[8 + add_chunk_id:8 + chunk_size + add_chunk_id])
                
                add_chunk_id += 8 + chunk_size

        
        # Converting the raw binary data to a list of integers : 
        typ = { 1: np.int8, 2: np.int16, 4: np.int32 }.get(self.sample_width/8)
        self.data_array = np.frombuffer(data, dtype=typ)
        # Convert to float32
        self.data_array = self.data_array.astype(np.float32)
        
        #return header_chunk_id, file_size, header_chunk_format, format_chunk_id, format_chunk_size, data_array, format_code, channels, sample_width, sample_rate, byte_rate, block_align, data_chunk_id, data_chunk_size, add_chunks
    
    def header_to_string(self):
        return f"The header is {self.header}"

    def header_chunk_to_string(self):
        return f"""Header Chunk ID : {self.header_chunk_id}
File Size : {self.file_size}
Header Chunk Format : {self.header_chunk_format}"""
    
    def format_to_string(self):
        return f"""Format Chunk ID : {self.format_chunk_id}
Format Chunk Size : {self.format_chunk_size}
Format Code: {self.format_code}
Number of Channels: {self.channels}
Sample Rate: {self.sample_rate}
Byte Rate : {self.byte_rate}
Block align : {self.block_align}
Sample Width: {self.sample_width}
Number of Samples: {len(self.data_array)}"""
    
    def data_to_string(self):
        return f"""Data Chunk ID : {self.data_chunk_id}
Data Size : {self.data_chunk_size}
Data : {self.data_array}
Type of data array : {type(self.data_array[0])}"""
    
    def meta_to_string(self):
        return f"""Additional chunks: {self.add_chunks}"""
    
    def plots(self):
        t = np.arange(len(self.data_array)/self.channels)/(self.sample_rate)

        if self.channels == 1: 
            plt.figure(figsize=(12,2))

            plt.subplot(2,1,1)
            plt.plot(t,self.data_array,color=[0,0,0],linewidth=0.5)
            plt.xlim(0, len(self.data_array)/self.sample_rate)
            plt.ylabel('Left chh')
            plt.grid()

            #plt.show()

        if self.channels == 2:
            data_chan = [self.data_array[offset::self.channels] for offset in range(self.channels)]
            for i in range(self.channels):
                if len(data_chan[i])!= len(t):
                    data_chan[i] = np.append( data_chan[i], np.empty(len(t) - len(data_chan[i])))

            plt.figure(figsize=(12,4))

            plt.subplot(2,1,1)
            plt.plot(t,data_chan[0],color=[0,0,0],linewidth=0.5)
            plt.xlim(0, len(self.data_array)/(self.channels*self.sample_rate))
            plt.xticks(ticks=[])
            plt.ylabel('Left ch')
            plt.grid()

            plt.subplot(2,1,2)
            plt.plot(t,data_chan[1],color=[0,0,0],linewidth=0.5)
            plt.xlim(0, len(self.data_array)/(self.channels*self.sample_rate))
            plt.ylabel('Rigth ch')
            plt.grid()

            #plt.show()
            
        plt.tight_layout()
        return plt.gcf()
    
    def save_anonimous_wav(self, output_file_path):
        with open(output_file_path, 'wb') as output_file:
            output_file.write(self.header)
            
            if self.sample_width == 8:
                data_type = np.int8
            elif self.sample_width == 16:
                data_type = np.int16
            elif self.sample_width == 32:
                data_type = np.int32
            else:
                raise ValueError("Unsupported sample width")
            
            # Zapisz dane do pliku
            data_bytes = self.data_array.astype(data_type).tobytes()
            output_file.write(data_bytes)

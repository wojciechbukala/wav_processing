import struct
import matplotlib.pyplot as plt
import numpy as np
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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
            self.data = audio_file.read(self.data_chunk_size)

            # Check for additional chunks
            self.add_chunks = b''
            add_chunk_id = 0
            add_data_id = self.data_chunk_size + 44
            audio_file.seek(add_data_id)
            add_data = audio_file.read()
            print(f"Additional data: {add_data}")

            self.add_chunks_list = self.split_additional_chunks(add_data)

        # Converting the raw binary data to a list of integers : 
        typ = { 1: np.int8, 2: np.int16, 4: np.int32 }.get(self.sample_width/8)
        self.data_array = np.frombuffer(self.data, dtype=typ)
        # Convert to float32
        self.data_array = self.data_array.astype(np.float32)
        
        #return header_chunk_id, file_size, header_chunk_format, format_chunk_id, format_chunk_size, data_array, format_code, channels, sample_width, sample_rate, byte_rate, block_align, data_chunk_id, data_chunk_size, add_chunks
    
    def split_additional_chunks(self, add_data):
        add_chunks_list = []
        add_chunk_id = 0

        while add_chunk_id + 8 <= len(add_data):  # Ensure enough bytes left for 8-byte chunk header
            chunk_id = struct.unpack('4s', add_data[0 + add_chunk_id:4 + add_chunk_id])[0]
            chunk_size = struct.unpack('<I', add_data[4 + add_chunk_id:8 + add_chunk_id])[0]

            # Extract chunk data
            chunk_data = add_data[8 + add_chunk_id:8 + chunk_size + add_chunk_id]

            # Add chunk to list
            add_chunks_list.append({
                'chunk_id': chunk_id.decode(),
                'chunk_size': chunk_size,
                'chunk_data': chunk_data
            })

            add_chunk_id += 8 + chunk_size

        return add_chunks_list


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
        result = f"""Additional chunks: {self.add_chunks}\n"""
        for chunk in self.add_chunks_list:
            result += f"Chunk ID: {chunk['chunk_id']}, Size: {chunk['chunk_size'],}\n Chunk data: {chunk['chunk_data']}"
        return result
        
    
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

    def spectrogram(self, fs, window_size=256, overlap=0.5):
        x = self.data_array
        hop_size = int(window_size * (1 - overlap))
        num_samples = len(x)
        num_windows = int(np.ceil((num_samples - window_size) / hop_size)) + 1
        frequencies = np.fft.rfftfreq(window_size, 1 / fs)
        
        spectrogram = np.zeros((len(frequencies), num_windows))
        
        for i in range(num_windows):
            start = i * hop_size
            end = start + window_size
            if end > num_samples:
                window = np.hamming(num_samples - start)
                padded_window = np.pad(window, (0, window_size - len(window)), 'constant')
                segment = x[start:num_samples]
                segment = np.pad(segment, (0, len(padded_window)-len(segment)), mode='constant')
            else:
                segment = x[start:end]
                padded_window = np.hamming(window_size)
            windowed_segment = segment * padded_window
            spectrum = np.abs(np.fft.rfft(windowed_segment, window_size))
            spectrogram[:, i] = spectrum
            times = np.arange(0, num_samples-1, hop_size)[1:]/fs
            
        return frequencies, times, spectrogram
    
    def plot_spectrogram(self, fs):
        frequencies, times, Sxx = self.spectrogram(fs)
        scale = 10 * np.log10(Sxx)
        plt.pcolormesh(times, frequencies, scale)  
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.title('Spectrogram')
        plt.colorbar(label='Intensity [dB]')
        #plt.show()

        plt.tight_layout()
        return plt.gcf()

############################ Electronic CodeBook section ############################
    def ecb_encrypt(self, public_key, block_size):
        e, N = public_key
        self.encrypted_blocks_base64 = []

        # data = self.data_array.tobytes()
        data = self.data
        for i in range(0, len(data), block_size):
            block = int.from_bytes(data[i:i+block_size-1], byteorder='big', signed=False)
            encrypted_block = pow(block, e, N)
            encrypted_block_bytes = encrypted_block.to_bytes((encrypted_block.bit_length() + 7) // 8, byteorder='big')
            encrypted_block_bytes += b'\0'*((block_size*8-encrypted_block.bit_length())//8)
            encrypted_block_base64 = base64.b64encode(encrypted_block_bytes).decode('utf-8')
            self.encrypted_blocks_base64.append(encrypted_block_base64)

        self.encrypted_data = '\n'.join(self.encrypted_blocks_base64).encode('utf-8')

    def save_encrypted_wav(self, output_file_path):
        with open(output_file_path, 'wb') as output_file:
            output_file.write(self.header)
            output_file.write(self.encrypted_data)

    def ecb_decrypt(self, private_key, block_size):
        d, N = private_key
        decrypted_data = bytearray()
        for encrypted_block_base64 in self.encrypted_blocks_base64:
            encrypted_block_bytes = base64.b64decode(encrypted_block_base64)
            encrypted_block = int.from_bytes(encrypted_block_bytes, byteorder='big', signed=False)
            decrypted_block = pow(encrypted_block, d, N)
            decrypted_block_bytes = decrypted_block.to_bytes((decrypted_block.bit_length()+7)//8, byteorder='big')
            decrypted_block_bytes += b'\0'*((block_size*8-decrypted_block.bit_length())//8)
            decrypted_data.extend(decrypted_block_bytes)

        decrypted_data = decrypted_data[:len(self.data_array.tobytes())]

        typ = {1: np.int8, 2: np.int16, 4: np.int32}.get(self.sample_width // 8)
        if not typ:
            raise ValueError("Unsupported sample width")
        self.data_array = np.frombuffer(decrypted_data, dtype=typ)

    def save_decrypted_wav(self, output_file_path):
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

            data_bytes = self.data_array.astype(data_type).tobytes()
            output_file.write(data_bytes)

############################ Cipher block chaining section ############################

    def xor_mask(self, data, mask):
        return bytes(a ^ b for a, b in zip(data, mask))
    def cbc_encryption(self, public_key, block_size, IV):
        e, N = public_key
        self.encrypted_blocks_base64 = []
        data = self.data 
        for i in range(0, len(data), block_size):
            block_bytes = data[i:i+block_size-1]
            if(i==0): 
                prev_block = IV
                i += 1
            print("type of prev block: ", type(prev_block))
            print("type of block: ", type(block_bytes))
            block_bytes = self.xor_mask(block_bytes, prev_block)
            block = int.from_bytes(block_bytes, byteorder='big', signed=False)
            encrypted_block = pow(block, e, N)
            encrypted_block_bytes = encrypted_block.to_bytes((encrypted_block.bit_length() + 7) // 8, byteorder='big')
            encrypted_block_bytes += b'\0'*((block_size*8-encrypted_block.bit_length())//8)
            prev_block = encrypted_block_bytes
            encrypted_block_base64 = base64.b64encode(encrypted_block_bytes).decode('utf-8')
            self.encrypted_blocks_base64.append(encrypted_block_base64)
        
        self.encrypted_data = '\n'.join(self.encrypted_blocks_base64).encode('utf-8')

    def cbc_decryption(self, private_key, block_size, IV):
        d, N = private_key
        decrypted_data = bytearray()
        i=0
        for encrypted_block_base64 in self.encrypted_blocks_base64:
            encrypted_block_bytes = base64.b64decode(encrypted_block_base64)
            encrypted_block = int.from_bytes(encrypted_block_bytes, byteorder='big', signed=False)
            decrypted_block = pow(encrypted_block, d, N)
            decrypted_block_bytes = decrypted_block.to_bytes((decrypted_block.bit_length()+7)//8, byteorder='big')
            decrypted_block_bytes += b'\0'*((block_size*8-decrypted_block.bit_length())//8)
            if(i==0): 
                prev_block = IV
                i += 1
            decrypted_block_bytes = self.xor_mask(decrypted_block_bytes, prev_block)
            decrypted_data.extend(decrypted_block_bytes)
            prev_block = encrypted_block_bytes
            
    def library_encrypt(self, public_key_pem, block_size):
        self.encrypted_blocks = []

        public_key = RSA.import_key(public_key_pem)
        cipher_rsa = PKCS1_OAEP.new(public_key)

        data = self.data
        for i in range(0, len(data), block_size):
            block = data[i:i+block_size]
            encrypted_block = cipher_rsa.encrypt(block)
            self.encrypted_blocks.append(encrypted_block)

        self.encrypted_data = b''.join(self.encrypted_blocks)

    def library_decrypt(self, private_key_pem):
        decrypted_data = bytearray()

        private_key = RSA.import_key(private_key_pem)
        cipher_rsa = PKCS1_OAEP.new(private_key)

        for encrypted_block in self.encrypted_blocks:
            decrypted_block = cipher_rsa.decrypt(encrypted_block)
            decrypted_data.extend(decrypted_block)

        decrypted_data = decrypted_data[:len(self.data_array.tobytes())]

        typ = {1: np.int8, 2: np.int16, 4: np.int32}.get(self.sample_width // 8)
        if not typ:
            raise ValueError("Unsupported sample width")
        self.data_array = np.frombuffer(decrypted_data, dtype=typ)

        

def add_bytes(input_file, output_file, bytes_to_add):
    with open(input_file, 'rb') as input_f:
        with open(output_file, 'wb') as output_f:
            header = input_f.read(44)
            output_f.write(header)
            
            data = input_f.read()
            output_f.write(data)
            
            output_f.write(bytes_to_add)


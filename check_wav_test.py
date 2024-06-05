import check_wav

cwav = check_wav.Check_wav("test_files/sample-file-4.wav")

print("\n -----HEADER CHUNK----- \n")
print(cwav.header_chunk_to_string())

print("\n -----FORMAT CHUNK----- \n")
print(cwav.format_to_string())

print("\n -----DATA CHUNK----- \n")
print(cwav.data_to_string())

print("\n -----METADATA CHUNK----- \n")
print(cwav.meta_to_string())

#cwav.plots()

cwav.plot_spectrogram(1000)

cwav.save_anonimous_wav("test_files/sample-file-4_result.wav")
additional_bytes = b"Additional bytes" * 1000
check_wav.add_bytes("test_files/sample-file-4_result.wav", "test_files/sample-file-4_additional.wav", additional_bytes)
import check_wav

cwav = check_wav.Check_wav("file_example_WAV_5MG.wav")

print("\n -----HEADER CHUNK----- \n")
print(cwav.header_chunk_to_string())

print("\n -----FORMAT CHUNK----- \n")
print(cwav.format_to_string())

print("\n -----DATA CHUNK----- \n")
print(cwav.data_to_string())

print("\n -----METADATA CHUNK----- \n")
print(cwav.meta_to_string())

cwav.plots()
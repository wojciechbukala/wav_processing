import check_wav

cwav = check_wav.Check_wav("test_files/Bontempi-B3-C5.wav")

print("\n -----HEADER CHUNK----- \n")
print(cwav.header_chunk_to_string())

print("\n -----FORMAT CHUNK----- \n")
print(cwav.format_to_string())

print("\n -----DATA CHUNK----- \n")
print(cwav.data_to_string())

print("\n -----METADATA CHUNK----- \n")
print(cwav.meta_to_string())

#cwav.plots()

cwav.save_anonimous_wav("test_files/Bontempi_result.wav")
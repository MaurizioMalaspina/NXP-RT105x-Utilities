import os
import sys

# Definitions for the C struct conversion
memConfig = { 'reserved0':4, 'readSampleClkSrc':1,
             'csHoldTime':1, 'csSetupTime':1, 'columnAddressWidth':1, 'deviceModeCfgEnable':1,
             'deviceModeType':1, 'waitTimeCfgCommands':2, 'deviceModeSeq':4, 'deviceModeArg':4,
             'configCmdEnable':1, 'configModeType':3, 'configCmdSeqs[0]':4, 'configCmdSeqs[1]':4,
             'configCmdSeqs[2]':4, 'reserved1':4, 'configCmdArgs[0]':4, 'configCmdArgs[1]':4,
             'configCmdArgs[2]':4, 'reserved2':4, 'controllerMiscOption':4, 'deviceType':1,
             'sflashPadType':1, 'serialClkFreq':1, 'lutCustomSeqEnable':1, 'reserved3':8,
             'sflashA1Size':4, 'sflashA2Size':4, 'sflashB1Size':4, 'sflashB2Size':4,
             'csPadSettingOverride':4, 'sclkPadSettingOverride':4, 'dataPadSettingOverride':4,
             'dqsPadSettingOverride':4, 'timeoutInMs':4, 'commandInterval':4, 'dataValidTime[0]':2,
             'dataValidTime[1]':2, 'busyOffset':2, 'busyBitPolarity':2
             }
flexspi_nor_cfg = {'pageSize':4, 'sectorSize':4, 'ipcmdSerialClkFreq':1, 'isUniformBlockSize':1,
                   'reserved0':2, 'serialNorType':1, 'needExitNoCmdMode':1, 'halfClkForNonReadCmd':1,
                   'needRestoreNoCmdMode':1, 'blockSize':4
                   }

lut_cmd = { 'CMD_SDR':        0x01,
            'CMD_DDR':        0x21,
            'RADDR_SDR':      0x02,
            'RADDR_DDR':      0x22,
            'CADDR_SDR':      0x03,
            'CADDR_DDR':      0x23,
            'MODE1_SDR':      0x04,
            'MODE1_DDR':      0x24,
            'MODE2_SDR':      0x05,
            'MODE2_DDR':      0x25,
            'MODE4_SDR':      0x06,
            'MODE4_DDR':      0x26,
            'MODE8_SDR':      0x07,
            'MODE8_DDR':      0x27,
            'WRITE_SDR':      0x08,
            'WRITE_DDR':      0x28,
            'READ_SDR':       0x09,
            'READ_DDR':       0x29,
            'LEARN_SDR':      0x0A,
            'LEARN_DDR':      0x2A,
            'DATSZ_SDR':      0x0B,
            'DATSZ_DDR':      0x2B,
            'DUMMY_SDR':      0x0C,
            'DUMMY_DDR':      0x2C,
            'DUMMY_RWDS_SDR': 0x0D,
            'DUMMY_RWDS_DDR': 0x2D,
            'JMP_ON_CS':      0x1F,
          }

lut_pad = { 'FLEXSPI_1PAD': 0,
            'FLEXSPI_2PAD': 1,
            'FLEXSPI_4PAD': 2,
            'FLEXSPI_8PAD': 3
          }

def split_LUT_item(lut_item, config):
    config.write("            FLEXSPI_LUT_SEQ(")
    data1 = lut_item[1] >> 2
    for k, v in lut_cmd.items():
        if v == data1:
            config.write(f"{k}, ")
            break
    else:
        config.write("0, ")
    
    data2 = lut_item[1] & 3
    for k, v in lut_pad.items():
        if v == data2:
            config.write(f"{k}, ")
            break
    else:
        config.write("0, ")
    
    data3 = lut_item[0]
    if data3 != 0:
        config.write(f"0x{data3:02X}, ")
    else:
        config.write(f"{data3}, ")
                 
    data1 = lut_item[3] >> 2
    for k, v in lut_cmd.items():
        if v == data1:
            config.write(f"{k}, ")
            break
    else:
        config.write("0, ")
    
    data2 = lut_item[3] & 0x3
    for k, v in lut_pad.items():
        if v == data2:
            config.write(f"{k}, ")
            break
    else:
        config.write("0, ")
    
    data3 = lut_item[2]
    config.write(f"{data3}")      

    config.write("),\n")
    return

def fillFCB(config, fd, rdpt, **dic_argv):
    max_key_length = max(len(k) for k in dic_argv.keys())
    for k, v in dic_argv.items():
        padding = max_key_length - len(k) + 8  # Align to the longest key with extra space
        config.write(f"        .{k}{' ' * padding}=")
        dl = 0
        data = 0
        while dl < v:
            data += (fd[rdpt] << (8 * dl))
            dl += 1
            rdpt += 1

        if data != 0:
            hex_data = f"0x{data:X}"
            spaces = ' ' * (9 - len(hex_data))
            config.write(f" {hex_data}{spaces}// dec = {data}")
        else:
            config.write(f" {data}")
        config.write(",\n")
    return rdpt

def parse_s19_file(input_file, output_file, text_output_file):
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        first_4_bytes_checked = False
        for line in infile:
            if line.startswith('S3'):
                address = int(line[4:12], 16)             # Extract address and convert in hexadecimal integer
                if 0x60000000 <= address <= 0x600001FF:   # The serial NOR configuration block start @ address 0x60000000
                    data_length = int(line[2:4], 16) - 5  # Subtract address and checksum lengths
                    data_start = 12
                    data_end = data_start + (data_length * 2)
                    data = bytes.fromhex(line[data_start:data_end]) # Create a bytes object from a string of hexadecimal numbers
                    
                    if not first_4_bytes_checked:
                        if data[:4] != b'FCFB':
                            print("Error: First 4 bytes are not 0x46434642 (FCFB).")
                            
                            # force files closure 
                            outfile.close()
                            
                            sys.exit(1)
                        first_4_bytes_checked = True
                    
                    outfile.write(data) # write on .bin

        # force files writing  and closing 
        outfile.flush()
        outfile.close()

        return first_4_bytes_checked

def bin_to_c_struct(binary_file):
    c_file = binary_file.rsplit('.', 1)[0] + '.c'
    text_file = binary_file.rsplit('.', 1)[0] + '.txt'

    try:
        with open(binary_file, 'rb') as f:
            fcb = f.read()
    except FileNotFoundError:
        print(f"File {binary_file} not found")
        sys.exit(1)

    with open(c_file, 'w') as config, open(text_file, 'w') as txtfile:
        config.write("const flexspi_nor_config_t qspiflash_config = {\n")
        config.write("    .memConfig =\n")
        config.write("    {\n")
        config.write("        .tag              = FLEXSPI_CFG_BLK_TAG,     // 0x42464346UL\n")
        config.write("        .version          = FLEXSPI_CFG_BLK_VERSION, // 0x56010400UL\n")

        pt = 8
        pt = fillFCB(config, fcb, pt, **memConfig) #fill the first 128 bytes

        config.write("        .lookupTable =\n")   #fill the LUT 256 bytes
        config.write("        {\n")
        loop = 0
        while loop < 64:
            item = fcb[pt:(pt + 4)]
            split_LUT_item(item, config)
            pt += 4
            loop += 1
            if loop % 4 == 0:
                config.write("\n")
        config.write("        },\n")

        config.write("        .lutCustomSeq={") #fill the custom LUT 48 bytes
        loop = 0
        while loop < 12:
            config.write(f"{fcb[pt] + (fcb[pt + 1] << 8) + (fcb[pt + 2] << 16) + (fcb[pt + 3] << 24)},")
            pt += 4
            loop += 1
        config.write("},\n")

        pt += 16 # skip reserved bytes
        config.write("    },\n")

        pt = fillFCB(config, fcb, pt, **flexspi_nor_cfg) #fill the last 64 bytes (only the first  3 fields are documented in  the RM)
        config.write("};\n")

        for i in range(0, len(fcb), 16): # generate txt file with the binary data
            line = ', '.join(f'0x{byte:02X}' for byte in fcb[i:i+16])
            txtfile.write(line + '\n')

    print(f"Generated files: {text_file}")
    print(f"Generated files: {c_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python FcbExtractor.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    file_extension = os.path.splitext(input_file)[1].lower()

    if file_extension == '.s19':
        output_file = input_file.rsplit('.', 1)[0] + '.bin'
        text_output_file = input_file.rsplit('.', 1)[0] + '.txt'
        first_4_bytes_checked = parse_s19_file(input_file, output_file, text_output_file)
        if first_4_bytes_checked:
            print(f"Generated files: {output_file}")
            bin_to_c_struct(output_file)
    elif file_extension == '.bin':
        bin_to_c_struct(input_file)
    else:
        print("Unsupported file format. Please provide a .s19 or .bin file.")
        sys.exit(1)
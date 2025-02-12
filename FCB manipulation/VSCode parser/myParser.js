registerFileType((fileExt, filePath, fileData) => {
	// Check for bin extension
	if (fileExt == 'bin'){
		return true;
	}
	return false;
});

registerParser(() => {
    // Tag
    read(4);
    addRow('TAG', getStringValue(), 'FlexSPI Configuration Block');

    // Version
    read(4);
    const version = getNumberValue();
    const bugfix = version & 0xFF;
    const minor = (version >> 8) & 0xFF;
    const major = (version >> 16) & 0xFF;
    const asciiV = String.fromCharCode((version >> 24) & 0xFF);
    addRow('Version', getHex0xValue(), `${asciiV}.${major}.${minor}.${bugfix} --> ASCII: '${asciiV}', Major: ${major},  Minor: ${minor}, BugFix: ${bugfix}`);

    // Reserved
    read(4);
    addRow('Reserved', getHex0xValue(), 'Reserved field');

    // Read Sample Clock Source
    read(1);
    addRow('readSampleClkSrc', getHex0xValue(), '0  internal loopback, 1  loopback from DQS pad, 3  Flash provided DQS');

    // csHoldTime
    read(1);
    addRow('csHoldTime', getHex0xValue(), 'Serial Flash CS Hold Time');

    // csSetupTime
    read(1);
    addRow('csSetupTime', getHex0xValue(), 'Serial Flash CS Setup Time');

    // columnAdressWidth
    read(1);
    addRow('columnAdressWidth', getHex0xValue(), 'Column Address Width: 3  HyperFlash, 12/13  Serial NAND, 0  Others');

    // Device Mode Configuration Enable
    read(1);
    addRow('deviceModeCfgEnable', getHex0xValue(), '0  Disabled, 1  Enabled');

    // Reserved
    read(1);
    addRow('Reserved', getHex0xValue(), 'Reserved field');

    // Wait Time Configuration Commands
    read(2);
    addRow('waitTimeCfgCommands', getHex0xValue(), 'Wait time for all configuration commands, unit 100us');

    // Device Mode Sequence
    read(4);
    addRow('deviceModeSeq', getHex0xValue(), 'Sequence for device mode configuration');

    // Device Mode Argument
    read(4);
    addRow('deviceModeArg', getHex0xValue(), 'Device Mode argument, effective only when deviceModeCfgEnable = 1');

    // Config Command Enable
    read(1);
    addRow('configCmdEnable', getHex0xValue(), '0  Disabled, 1  Enabled');

    // Reserved
    read(3);
    addRow('Reserved', getHex0xValue(), 'Reserved field');

    // Config Command Sequences
    read(12);
    addRow('configCmdSeqs', getHexValue(), 'Sequences for Config Command, allow 3 separate configuration commands');

    // Reserved
    read(4);
    addRow('Reserved', getHex0xValue(), 'Reserved field');

    // Config Command Arguments
    read(12);
    addRow('cfgCmdArgs', getHexValue(), 'Arguments for each separate configuration command sequence');

    // Reserved
    read(4);
    addRow('Reserved', getHex0xValue(), 'Reserved field');

    // Controller Misc Options
    read(4);
    addRow('controllerMiscOption', getHex0xValue(), `Miscellaneous options for controller:
    Bit0  differential clock enable
    Bit1  CK2 enable, must set to 0 in this silicon
    Bit2  ParallelModeEnable, must set to 0 for this silicon
    Bit3  wordAddressableEnable
    Bit4  Safe Configuration Frequency enable set to 1 for the devices that support DDR Read instructions
    Bit5  Pad Setting Override Enable
    Bit6  DDR Mode Enable, set to 1 for device supports DDR read command
    `);

    // Device Type
    read(1);
    addRow('deviceType', getHex0xValue(), '1  Serial NOR, 2  Serial NAND');

    // SFlash Pad Type
    read(1);
    addRow('sflashPadType', getHex0xValue(), '1  Single pad, 2  Dual pads, 4  Quad pads, 8  Octal pads');

    // Serial Clock Frequency
    read(1);
    addRow('serialClkFreq', getHex0xValue(), '1  30 MHz, 2  50 MHz, 3  60 MHz, 4  75 MHz, 5  80 MHz, 6  100 MHz, 7  133 MHz, 8  166 MHz, Other values - 30 MHz');

    // LUT Custom Sequence Enable
    read(1);
    addRow('lutCustomSeqEnable', getHex0xValue(), '0  Use pre-defined LUT sequence index and number, 1  Use LUT sequence parameters provided in this block');

    // Reserved
    read(8);
    addRow('Reserved', getHexValue(), 'Reserved field');

    // SFlash Sizes
    read(4);
    addRow('sflashA1Size', getHex0xValue(), 'Actual size for SPI NOR / Size * 2 for SPI NAND');
    read(4);
    addRow('sflashA2Size', getHex0xValue(), 'Same as above');
    read(4);
    addRow('sflashB1Size', getHex0xValue(), 'Same as above');
    read(4);
    addRow('sflashB2Size', getHex0xValue(), 'Same as above');

    // Pad Setting Overrides
    read(4);
    addRow('csPadSettingOverride', getHex0xValue(), 'Set to 0 if not supported');
    read(4);
    addRow('sclkPadSettingOverride', getHex0xValue(), 'Set to 0 if not supported');
    read(4);
    addRow('dataPadSettingOverride', getHex0xValue(), 'Set to 0 if not supported');
    read(4);
    addRow('dqsPadSettingOverride', getHex0xValue(), 'Set to 0 if not supported');

    // Timeout in ms
    read(4);
    addRow('timeoutInMs', getHex0xValue(), 'Maximum wait time during read busy status');

    // Command Interval
    read(4);
    addRow('commandInterval', getHex0xValue(), 'Unit: ns, used for SPI NAND only at high frequency');

    // Data Valid Time
    read(4);
    addRow('dataValidTime', getHex0xValue(), 'Time from clock edge to data valid edge, unit ns');

    // Busy Offset and Polarity
    read(2);
    addRow('busyOffset', getHex0xValue(), 'Busy bit offset, range: 0-31');
    read(2);
    addRow('busyBitPolarity', getHex0xValue(), '0  busy bit is 1 if device is busy, 1  busy bit is 0 if device is busy');

    // Lookup Table
    read(256);
    addRow('lookupTable', getHexValue(), 'Lookup table');

    // LUT Custom Sequence
    read(48);
    addRow('lutCustomSeq', getHexValue(), 'Customized LUT sequence');

    // Reserved, not documented in the RM, extracted from the SDK
    read(16);
    addRow('Reserved', getHexValue(), 'Reserved for future use');

    read(4);
    addRow('pageSize', getHexValue(), 'Page size of Serial NOR Flash');

    read(4);
    addRow('sectorSize', getHexValue(), 'Sector size of Serial NOR Flash');

    read(1);
    addRow('ipcmdSerialClkFreq', getHexValue(), 'IP command serial clock frequency');
    
    read(1);
    addRow('isUniformBlockSize', getHexValue(), 'Uniform block size (Sector/Block size is the same)');

    read(2);
    addRow('reserved0', getHexValue(), 'Reserved for future use');

    read(1);
    addRow('serialNorType', getHexValue(), 'Serial NOR Flash type: 0/1/2/3');

    read(1);
    addRow('needExitNoCmdMode', getHexValue(), 'Need to exit NoCmd mode before other IP command');

    read(1);
    addRow('halfClkForNonReadCmd', getHexValue(), 'Half the Serial Clock for non-read command: true/false');

    read(1);
    addRow('needRestoreNoCmdMode', getHexValue(), 'Need to Restore NoCmd mode after IP commmand execution');

    read(4);
    addRow('blockSize', getHexValue(), 'Block size of Serial NOR Flash');

    read(11);
    addRow('Reserved1', getHexValue(), 'Reserved for future use');
});

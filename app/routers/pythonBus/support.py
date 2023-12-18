def getFreeAppChannel(canChannel: dict) -> int:
    """this function iterate all over the canChannel and get the 
    first available channel number (application ch num)

    Args:
        canChannel (_type_): dict[VectorCanChannel]

    Returns:
        int: first available app channel number
    """
    try:
        # Get a sorted list of existing ch_num values
        existing_ch_nums = sorted(bus.channelNum for bus in canChannel.values())

        # Find the smallest missing number in the sequence
        new_ch_num = 0
        for num in existing_ch_nums:
            if num != new_ch_num:
                break
            new_ch_num += 1

        return new_ch_num
    except:
        return 0
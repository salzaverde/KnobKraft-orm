import roland
from Roland_XV3080 import _xv3080_patch_data, xv_3080, xv_3080_main, _xv3080_edit_buffer_addresses
import knobkraft
from roland import DataBlock


def test_edit_buffers():
    edit_buffer1 = knobkraft.stringToSyx(
        "f0 41 10 00 10 12 1f 00 00 00 50 69 61 6e 6f 6d 6f 6e 69 63 73 20 01 00 74 40 01 40 40 40 00 00 01 00 00 00 01 00 00 12 00 06 04 00 40 40 40 40 40 0d 00 02 02 64 02 45 00 40 00 40 00 40 62 09 48 00 40 00 40 00 40 65 04 4a 00 40 00 40 00 40 00 00 40 00 40 00 40 00 40 0b f7"
        "f0 41 10 00 10 12 1f 00 02 00 01 7f 7f 7f 00 00 40 00 40 00 40 00 40 00 00 00 00 08 00 00 00 08 00 01 06 08 00 00 01 08 00 01 03 08 00 00 07 08 00 00 00 08 00 01 01 08 00 01 00 08 00 00 00 08 00 01 00 08 00 07 0f 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 34 f7"
        "f0 41 10 00 10 12 1f 00 04 00 01 00 00 00 08 00 00 01 08 00 00 0d 08 00 00 01 08 00 00 00 08 00 00 00 08 00 00 07 08 00 05 0a 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 57 f7"
        "f0 41 10 00 10 12 1f 00 06 00 03 32 00 08 00 05 0a 08 00 06 02 08 00 00 07 08 00 01 04 08 00 07 0f 08 00 07 0f 08 00 00 0d 08 00 02 04 08 00 00 02 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 22 f7"
        "f0 41 10 00 10 12 1f 00 10 00 00 00 00 00 01 00 00 7f 00 00 01 7f 00 00 01 00 7f 00 00 01 7f 00 00 01 00 7f 00 00 01 7f 00 00 00 00 7f 00 00 01 7f 00 00 52 f7"
        "f0 41 10 00 10 12 1f 00 20 00 7f 40 40 00 40 40 00 40 01 00 00 00 7f 7f 7f 00 00 01 01 01 01 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 01 0f 40 00 40 00 40 70 03 65 40 40 44 00 40 5c 7f 00 7f 58 02 7f 40 3c 00 02 58 40 40 47 00 3b 4e 14 7f 61 00 01 05 0f 02 00 00 40 00 00 00 40 40 40 40 01 05 00 02 00 00 40 00 00 00 40 40 40 40 1b f7"
        "f0 41 10 00 10 12 1f 00 22 00 7f 40 40 00 40 40 00 40 01 00 00 00 7f 7f 7f 00 5b 01 01 01 01 00 01 01 00 00 00 01 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 01 00 00 00 02 03 00 00 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 06 3f 40 00 40 00 40 61 03 5e 40 40 42 00 45 65 7f 00 7f 58 13 7f 40 3c 00 02 59 40 40 45 00 43 5d 2b 7f 64 00 01 05 0e 02 00 00 40 00 00 00 40 40 40 40 01 05 00 02 00 00 40 00 00 00 40 40 40 40 4a f7"
        "f0 41 10 00 10 12 1f 00 24 00 7f 40 40 00 40 40 00 40 01 00 00 00 7f 7f 7f 00 25 01 01 01 01 00 01 01 00 00 00 01 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 01 00 00 09 00 00 00 09 02 03 00 00 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 06 44 40 00 40 00 40 55 03 5e 40 40 42 00 45 65 7f 00 7f 58 13 7f 40 3c 00 02 58 40 40 45 00 43 5d 2b 7f 64 00 01 05 0e 02 00 00 40 00 00 00 40 40 40 40 01 05 00 02 00 00 40 00 00 00 40 40 40 40 75 f7"
        "f0 41 10 00 10 12 1f 00 26 00 7f 40 40 00 40 40 08 40 01 00 00 00 7f 7f 7f 7f 7f 00 01 01 01 00 00 01 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 01 3a 40 00 40 00 40 7f 03 5e 40 40 42 00 45 65 7f 00 7f 58 13 7f 40 3c 00 02 54 40 40 45 00 43 5d 2b 7f 64 00 01 05 0f 02 00 00 40 00 00 00 40 40 40 40 01 05 00 02 00 00 40 00 00 00 40 40 40 40 13 f7")
    edit_buffer2 = knobkraft.stringToSyx(
        "f0 41 10 00 10 12 1f 00 00 00 50 69 6c 67 72 69 6d 61 67 65 20 20 1f 00 7f 40 00 40 40 40 00 01 01 00 00 00 01 01 01 48 00 07 08 00 40 40 40 40 40 0d 00 02 02 62 11 4a 00 40 00 40 00 40 63 11 4a 04 47 00 40 00 40 64 02 4d 04 4a 00 40 00 40 00 00 40 00 40 00 40 00 40 4e f7"
        "f0 41 10 00 10 12 1f 00 02 00 13 7f 7f 7f 00 00 40 00 40 00 40 00 40 00 00 00 00 08 00 07 09 08 00 07 07 08 00 07 0a 08 00 04 01 08 00 01 01 08 00 07 0f 08 00 07 0f 08 00 07 0f 08 00 00 0f 08 00 00 06 08 00 03 02 08 00 07 0f 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 27 f7"
        "f0 41 10 00 10 12 1f 00 04 00 01 7f 00 00 08 00 01 09 08 00 02 04 08 00 01 04 08 00 00 03 08 00 00 00 08 00 00 07 08 00 05 0a 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 4f f7"
        "f0 41 10 00 10 12 1f 00 06 00 01 2e 00 08 00 00 03 08 00 04 03 08 00 00 0d 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 75 f7"
        "f0 41 10 00 10 12 1f 00 10 00 00 00 00 00 01 01 00 7f 00 00 01 7f 00 00 01 00 7f 00 00 01 7f 00 00 01 00 7f 00 00 01 7f 00 00 01 00 7f 00 00 01 7f 00 00 50 f7"
        "f0 41 10 00 10 12 1f 00 20 00 7f 40 40 00 00 40 00 40 01 00 00 00 7f 3c 52 7f 7f 00 01 01 01 00 00 01 00 00 00 01 01 00 00 01 01 00 00 00 00 00 00 00 00 00 00 01 00 01 0e 01 00 00 00 00 01 00 01 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 01 46 3d 00 40 00 40 54 02 54 40 40 42 00 0d 3d 58 00 7f 52 05 00 41 3c 03 01 5c 40 40 40 00 2c 48 32 7f 71 00 00 05 02 02 00 05 40 00 05 00 40 34 77 7f 01 04 08 02 00 00 40 00 00 01 40 40 40 40 28 f7"
        "f0 41 10 00 10 12 1f 00 22 00 3b 40 40 00 7f 40 00 40 01 00 08 00 7f 7f 6d 7f 7f 00 01 01 01 00 00 01 00 00 00 01 01 00 00 01 01 00 00 00 00 00 00 00 00 00 00 01 00 01 0b 0f 00 00 00 00 01 00 01 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 01 59 3d 00 40 00 40 54 02 54 40 40 42 00 0d 3d 58 00 7f 52 05 00 41 3c 03 01 5c 40 40 40 00 2c 48 32 7f 71 00 00 05 02 02 00 05 40 00 05 00 3a 34 77 7f 01 04 08 02 00 00 40 00 00 01 40 40 40 40 6d f7"
        "f0 41 10 00 10 12 1f 00 24 00 7f 40 40 00 00 40 00 40 01 00 00 00 7f 3c 52 7f 7f 00 01 01 01 00 00 01 00 00 00 01 01 00 00 01 01 00 00 00 00 00 00 00 00 00 00 01 00 02 00 05 00 00 00 00 01 00 01 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 01 3e 3d 00 40 00 40 54 02 54 40 40 42 00 0d 3d 58 00 7f 52 05 00 41 3c 03 01 5c 40 40 40 00 2c 48 32 7f 71 00 00 05 02 02 00 05 40 00 05 00 40 34 77 7f 01 04 08 02 00 00 40 00 00 01 40 40 40 40 35 f7"
        "f0 41 10 00 10 12 1f 00 26 00 3b 40 40 00 7f 40 00 40 01 00 08 00 7f 7f 6d 7f 7f 00 01 01 01 00 00 01 00 00 00 01 01 00 00 01 01 00 00 00 00 00 00 00 00 00 00 01 00 01 09 0a 00 00 00 00 01 00 01 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 01 59 3d 00 40 00 40 54 02 54 40 40 42 00 0d 3d 58 00 7f 52 05 00 41 3c 03 01 5c 40 40 40 00 2c 48 32 7f 71 00 00 05 02 02 00 05 40 00 05 00 3a 34 77 7f 01 04 08 02 00 00 40 00 00 01 40 40 40 40 70 f7")
    assert xv_3080.isEditBufferDump(edit_buffer1)
    assert xv_3080.isEditBufferDump(edit_buffer2)
    assert xv_3080.calculateFingerprint(edit_buffer1) != xv_3080.calculateFingerprint(edit_buffer2)


def test_address_calculation():
    value = (0x01, 0x02, 0x03, 0x04)
    as_int = DataBlock.size_to_number(value)
    as_list = tuple(DataBlock.size_as_7bit_list(as_int, 4))
    assert value == as_list

    base_block = _xv3080_patch_data[6]
    assert base_block.address == (0x00, 0x00, 0x22, 0x00)
    edit_buffer = _xv3080_edit_buffer_addresses
    assert edit_buffer.absolute_address(base_block.address) == (0x1f, 0x00, 0x22, 0x00)
    address, size = edit_buffer.address_and_size_for_sub_request(6, 17)
    assert address == [0x1f, 17, 0x22, 0x00]
    assert size == DataBlock.size_as_7bit_list(base_block.size, 4)

    # Test 7 bit overflow
    address, size = edit_buffer.address_and_size_for_sub_request(6, 128)
    assert address == [0x20, 0, 0x22, 0x00]

    # Test calculating the subaddress
    assert edit_buffer.subaddress_from_address([0x1f, 0x00, 0x22, 0x00]) == 0x00
    assert edit_buffer.subaddress_from_address([0x1f, 17, 0x22, 0x00]) == 17
    assert edit_buffer.subaddress_from_address([0x20, 0x00, 0x22, 0x00]) == 128

    # Test finding the block of an address
    assert edit_buffer.find_base_address([0x1f, 0x00, 0x22, 0x00]) == (0x1f, 0x00, 0x22 ,0x00)
    assert edit_buffer.find_base_address([0x1f, 0x7f, 0x22, 0x00]) == (0x1f, 0x00, 0x22 ,0x00)


def test_message_creation():
    # Example 1
    set_chorus_performance_common = [0xf0, 0x41, 0x10, 0x00, 0x10, 0x12, 0x10, 0x00, 0x04, 0x00, 0x02, 0x6a, 0xf7]
    assert (xv_3080.main_model.isOwnSysex(set_chorus_performance_common))
    command3, address4, data5 = xv_3080.main_model.parseRolandMessage(set_chorus_performance_common)
    assert (command3 == 0x12)
    assert (address4 == [0x10, 0x00, 0x04, 0x00])
    assert (data5 == [0x02])
    composed6 = xv_3080.main_model.buildRolandMessage(0x10, roland.command_dt1, [0x10, 0x00, 0x04, 0x00], [0x02])
    assert (composed6 == set_chorus_performance_common)

    # Test weird address arithmetic
    assert (roland.DataBlock.size_to_number((0x1, 0x1, 0x1)) == (16384 + 128 + 1))
    for i in range(1200):
        list_address = roland.DataBlock.size_as_7bit_list(i, 4)
        and_back = roland.DataBlock.size_to_number(tuple(list_address))
        assert (i == and_back)


def test_program_dump_request():
    edit_buffer1 = knobkraft.stringToSyx(
        "f0 41 10 00 10 12 1f 00 00 00 50 69 61 6e 6f 6d 6f 6e 69 63 73 20 01 00 74 40 01 40 40 40 00 00 01 00 00 00 01 00 00 12 00 06 04 00 40 40 40 40 40 0d 00 02 02 64 02 45 00 40 00 40 00 40 62 09 48 00 40 00 40 00 40 65 04 4a 00 40 00 40 00 40 00 00 40 00 40 00 40 00 40 0b f7"
        "f0 41 10 00 10 12 1f 00 02 00 01 7f 7f 7f 00 00 40 00 40 00 40 00 40 00 00 00 00 08 00 00 00 08 00 01 06 08 00 00 01 08 00 01 03 08 00 00 07 08 00 00 00 08 00 01 01 08 00 01 00 08 00 00 00 08 00 01 00 08 00 07 0f 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 34 f7"
        "f0 41 10 00 10 12 1f 00 04 00 01 00 00 00 08 00 00 01 08 00 00 0d 08 00 00 01 08 00 00 00 08 00 00 00 08 00 00 07 08 00 05 0a 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 57 f7"
        "f0 41 10 00 10 12 1f 00 06 00 03 32 00 08 00 05 0a 08 00 06 02 08 00 00 07 08 00 01 04 08 00 07 0f 08 00 07 0f 08 00 00 0d 08 00 02 04 08 00 00 02 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 08 00 00 00 22 f7"
        "f0 41 10 00 10 12 1f 00 10 00 00 00 00 00 01 00 00 7f 00 00 01 7f 00 00 01 00 7f 00 00 01 7f 00 00 01 00 7f 00 00 01 7f 00 00 00 00 7f 00 00 01 7f 00 00 52 f7"
        "f0 41 10 00 10 12 1f 00 20 00 7f 40 40 00 40 40 00 40 01 00 00 00 7f 7f 7f 00 00 01 01 01 01 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 01 0f 40 00 40 00 40 70 03 65 40 40 44 00 40 5c 7f 00 7f 58 02 7f 40 3c 00 02 58 40 40 47 00 3b 4e 14 7f 61 00 01 05 0f 02 00 00 40 00 00 00 40 40 40 40 01 05 00 02 00 00 40 00 00 00 40 40 40 40 1b f7"
        "f0 41 10 00 10 12 1f 00 22 00 7f 40 40 00 40 40 00 40 01 00 00 00 7f 7f 7f 00 5b 01 01 01 01 00 01 01 00 00 00 01 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 01 00 00 00 02 03 00 00 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 06 3f 40 00 40 00 40 61 03 5e 40 40 42 00 45 65 7f 00 7f 58 13 7f 40 3c 00 02 59 40 40 45 00 43 5d 2b 7f 64 00 01 05 0e 02 00 00 40 00 00 00 40 40 40 40 01 05 00 02 00 00 40 00 00 00 40 40 40 40 4a f7"
        "f0 41 10 00 10 12 1f 00 24 00 7f 40 40 00 40 40 00 40 01 00 00 00 7f 7f 7f 00 25 01 01 01 01 00 01 01 00 00 00 01 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 01 00 00 09 00 00 00 09 02 03 00 00 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 06 44 40 00 40 00 40 55 03 5e 40 40 42 00 45 65 7f 00 7f 58 13 7f 40 3c 00 02 58 40 40 45 00 43 5d 2b 7f 64 00 01 05 0e 02 00 00 40 00 00 00 40 40 40 40 01 05 00 02 00 00 40 00 00 00 40 40 40 40 75 f7"
        "f0 41 10 00 10 12 1f 00 26 00 7f 40 40 00 40 40 08 40 01 00 00 00 7f 7f 7f 7f 7f 00 01 01 01 00 00 01 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 00 01 00 4a 40 40 40 40 40 00 00 00 00 40 40 40 40 40 01 3a 40 00 40 00 40 7f 03 5e 40 40 42 00 45 65 7f 00 7f 58 13 7f 40 3c 00 02 54 40 40 45 00 43 5d 2b 7f 64 00 01 05 0f 02 00 00 40 00 00 00 40 40 40 40 01 05 00 02 00 00 40 00 00 00 40 40 40 40 13 f7")
    program_place = 33
    program_buffer = xv_3080_main.convertToProgramDump(0, edit_buffer1, program_place)
    program_messages = knobkraft.splitSysexMessage(program_buffer)
    sub_message = 0
    for message in program_messages:
        command, address = xv_3080_main.getCommandAndAddressFromRolandMessage(message)
        assert command == roland.command_dt1
        # Check that we can extract the program place correctly
        program_no = xv_3080_main.program_dump.subaddress_from_address(address)
        assert program_place == program_no
        # Check that we can normalize the address also correctly
        assert xv_3080_main.program_dump.absolute_address(xv_3080_main.program_dump.data_blocks[sub_message].address) == \
               xv_3080_main.program_dump.find_base_address(address)
        # Now check that we can calculate the next request package correctly
        is_part, reply = xv_3080_main.isPartOfSingleProgramDump(message)
        print(reply)
        assert is_part

        if len(reply) > 0:
            command, reply_address = xv_3080_main.getCommandAndAddressFromRolandMessage(reply)
            assert command == roland.command_rq1
            new_program_no = xv_3080_main.program_dump.subaddress_from_address(reply_address)
            assert program_place == new_program_no
            assert xv_3080_main.program_dump.absolute_address(xv_3080_main.program_dump.data_blocks[sub_message + 1].address) == \
                xv_3080_main.program_dump.find_base_address(reply_address)

        # Process next message
        sub_message += 1


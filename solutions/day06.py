PACKET_MARK_SIZE = 4
MESSAGE_MARK_SIZE = 14

def run(input_data: str):
    packet_start = None
    message_start = None
    for idx, _ in enumerate(input_data):
        if packet_start is None and len(set(input_data[idx:idx + PACKET_MARK_SIZE])) == PACKET_MARK_SIZE:
            packet_start = (idx + PACKET_MARK_SIZE)

        if message_start is None and len(set(input_data[idx:idx + MESSAGE_MARK_SIZE])) == MESSAGE_MARK_SIZE:
            message_start = (idx + MESSAGE_MARK_SIZE)

    print(f"Part one: {packet_start}")
    print(f"Part two: {message_start}")

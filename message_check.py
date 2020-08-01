import sys


def validate(message: str):
    print('BAF')
    print(message)
    if len(message) < 2:
        raise ValueError('Message is too short.')
    if message[0] == '#':
        message_without_pound = message[1:]
        splited_message = message_without_pound.split()
        print(splited_message[0])
        message_number = int(splited_message[0])

    else:
        raise ValueError('Message must start with # followed by a number!')


if __name__ == "__main__":
    validate(open(sys.argv[1], 'r').read())

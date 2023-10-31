from argparse import ArgumentParser

def config_argparse():
    a = ArgumentParser()
    a.add_argument('--input', '-i', type=str, required=True)
    a.add_argument('--output', '-o', type=str, required=True)
    a.add_argument('--password', '-p', type=str, required=True)
    return a.parse_args()

def xor_encrypt_decrypt(input_file, output_file, key):
    with open(input_file, 'rb') as file:
        data = file.read()

    key_bytes = key.encode('ascii')
    key_length = len(key_bytes)
    encrypted_data = bytearray()

    for i, byte in enumerate(data):
        encrypted_byte = byte ^ key_bytes[i % key_length]
        encrypted_data.append(encrypted_byte)

    with open(output_file, 'wb') as file:
        file.write(encrypted_data)

    print(f'File {input_file} XOR-ed with key "{key}" and saved to {output_file}')

if __name__ == '__main__':
    args = config_argparse()
    xor_encrypt_decrypt(args.input, args.output, args.password)

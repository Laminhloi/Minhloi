import base64
import binascii
import marshal
import lzma
import zlib
import sys

def encode_base64(content, reverse=False):
    content = base64.b64encode(content)
    if reverse:
        content = content[::-1]
    return content

def encode_base85(content, reverse=False):
    content = base64.b85encode(content)
    if reverse:
        content = content[::-1]
    return content

def encode_hex(content, reverse=False):
    content = binascii.hexlify(content)
    if reverse:
        content = content[::-1]
    return content

def encode_marshal(content, reverse=False):
    encoded_content = marshal.dumps(content)
    if reverse:
        encoded_content = encoded_content[::-1]
    return encoded_content

def encode_lzma(content, reverse=False):
    encoded_content = lzma.compress(content)
    if reverse:
        encoded_content = encoded_content[::-1]
    return encoded_content

def encode_zlib(content, reverse=False):
    encoded_content = zlib.compress(content)
    if reverse:
        encoded_content = encoded_content[::-1]
    return encoded_content


def process_command(content, command_name, reverse=False):
    """Process a single command to encode or compress content."""
    if command_name == "base":
        content = encode_base64(content, reverse=reverse)
    elif command_name == "85b":
        content = encode_base85(content, reverse=reverse)
    elif command_name == "hex":
        content = encode_hex(content, reverse=reverse)
    elif command_name == "mas":
        content = encode_marshal(content, reverse=reverse)
    elif command_name == "lm":
        content = encode_lzma(content, reverse=reverse)
    elif command_name == "zlib":
        content = encode_zlib(content, reverse=reverse)
    elif command_name == "ngc":
        content = content[::-1]
    
    return content

def encode_file(input_file_path, commands):
    with open(input_file_path, 'rb') as file:
        content = file.read()

    created_files = []
    step = 1

    for command in commands:
        command_name = command.rstrip("0123456789").replace("-1", "")
        times = int(command[len(command_name):]) if command[len(command_name):].isdigit() else 1
        reverse = command.startswith("-1")

        for _ in range(times):
            content = process_command(content, command_name, reverse=reverse)
            file_name = f"{step}_{command_name}.py"
            create_encoded_file(content, file_name, command_name)
            created_files.append(file_name)

            with open(file_name, 'rb') as file:
                content = file.read()

            step += 1

    return created_files

def create_encoded_file(encoded_content, file_name, command_name):
    python_code = f"""
\"\"\"
TOOL ENCODE BỞI LA MINH LỢI 
\"\"\"
import base64
import binascii
import marshal
import lzma
import zlib
import sys

def decode_content(encoded_content, command_name):
    reverse = command_name.startswith("-1")
    try:
        if command_name == "base":
            decoded_content = base64.b64decode(encoded_content)
        elif command_name == "85b":
            decoded_content = base64.b85decode(encoded_content)
        elif command_name == "hex":
            decoded_content = binascii.unhexlify(encoded_content)
        elif command_name == "mas":
            decoded_content = marshal.loads(encoded_content)
        elif command_name == "lm":
            decoded_content = lzma.decompress(encoded_content)
        elif command_name == "zlib":
            decoded_content = zlib.decompress(encoded_content)        
    except Exception as e:
        print(f"Đã xảy ra lỗi khi giải mã:")
        sys.exit(1)    
    return decoded_content

try:
    encoded_content = {repr(encoded_content)}
    command_name = {repr(command_name)}
    decoded_content = decode_content(encoded_content, command_name)
    exec(decoded_content.decode('utf-8'))
except Exception as e:
    print(f"Đã xảy ra lỗi khi thực thi:")
    sys.exit(1)
"""
    with open(file_name, 'w') as file:
        file.write(python_code)

# Main execution
input_file_path = input("Nhập Tên File : ")
commands = input("Nhập chuỗi lệnh mã hóa VD : base1 lm2 mas1 zlib1 85b2 hex1 : ").split()
created_files = encode_file(input_file_path, commands)

print("Đã tạo các tệp sau:")
for f in created_files:
    print(f)

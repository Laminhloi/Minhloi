import base64

def encode_shell_script(input_file, output_file):
    try:
        # Đọc nội dung từ file .sh gốc
        with open(input_file, 'r', encoding='utf-8') as file:
            script_content = file.read()
        
        # Mã hóa nội dung
        encoded_content = base64.b64encode(script_content.encode('utf-8')).decode('utf-8')
        
        # Tạo file mới chứa mã hóa và mã giải mã
        with open(output_file, 'w', encoding='utf-8') as encoded_file:
            encoded_file.write(f"""#!/bin/bash
# Script này tự giải mã và thực thi

encoded_script="{encoded_content}"

# Giải mã nội dung
decoded_script=$(echo "$encoded_script" | base64 --decode | tr -d '\\r')

# Lưu nội dung vào file tạm và thực thi
bash_code=$(mktemp /tmp/script.XXXXXX)
echo "$decoded_script" > "$bash_code"
chmod +x "$bash_code"
bash "$bash_code"
rm -f "$bash_code"
""")
        
        print(f"File mã hóa đã được tạo: {output_file}")
    except FileNotFoundError:
        print("Không tìm thấy file gốc!")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    input_file = input("Nhập tên file .sh gốc cần mã hóa: ").strip()
    output_file = input("Nhập tên file .sh mã hóa sẽ tạo: ").strip()
    
    encode_shell_script(input_file, output_file)

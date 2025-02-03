import base64

def encode_file(file_name, encoding_type, iterations, output_file_name):
    try:
        # Đọc nội dung từ file gốc
        with open(file_name, 'rb') as file:
            data = file.read()
        
        # Xử lý mã hóa theo số lần
        for _ in range(iterations):
            if encoding_type == "base64":
                data = base64.b64encode(data)
            else:
                raise ValueError("Loại mã hóa không được hỗ trợ!")
        
        # Lưu kết quả vào file mới
        with open(output_file_name, 'wb') as output_file:
            output_file.write(data)
        
        print(f"Đã mã hóa tệp {file_name} thành công và lưu vào {output_file_name}")
    
    except FileNotFoundError:
        print("Không tìm thấy tệp được chỉ định!")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    # Nhập tên tệp gốc
    file_name = input("Nhập tên tệp cần mã hóa (bao gồm phần mở rộng): ").strip()
    
    # Nhập loại mã hóa
    encoding_type = input("Nhập loại mã hóa (ví dụ: base64): ").strip().lower()
    
    # Nhập số lần mã hóa (1-100)
    while True:
        try:
            iterations = int(input("Nhập số lần mã hóa (1-100): ").strip())
            if 1 <= iterations <= 100:
                break
            else:
                print("Vui lòng nhập số trong khoảng từ 1 đến 100!")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ!")
    
    # Nhập tên file kết quả
    output_file_name = input("Nhập tên file kết quả (ví dụ: Loi.txt): ").strip()
    
    # Thực hiện mã hóa
    encode_file(file_name, encoding_type, iterations, output_file_name)

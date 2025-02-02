import time
import telebot
import threading

# Token bot Telegram
laminhloi = "8016938264:AAE9KA2fRFNCTBWyJio8p-CiZr6qaD93828"
bot = telebot.TeleBot(laminhloi)

# ID Admin
ADMIN_ID = 7779940330  

# Dictionary lưu trạng thái lệnh đang chạy theo nhóm
running_tasks = {}

# Tốc độ gửi tin nhắn cho mỗi lệnh
SEND_DELAY = {
    "treotru": 14,  
    "nhay": 3,      
    "reo": 3        
}

# Hàm gửi toàn bộ nội dung file & lặp lại vô hạn
def send_full_loop(chat_id, file_name, delay, command):
    while running_tasks.get(chat_id, {}).get(command, False):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.read()
            bot.send_message(chat_id, content)
            time.sleep(delay)
        except Exception as e:
            print(f"Lỗi: {e}")
            break

# Hàm gửi từng dòng & lặp lại
def send_line_loop(chat_id, file_name, delay, command, user_tag=None):
    while running_tasks.get(chat_id, {}).get(command, False):
        try:
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.readlines()
            for line in content:
                if not running_tasks.get(chat_id, {}).get(command, False):
                    return  
                message = f"{user_tag} {line.strip()}" if user_tag else line.strip()
                bot.send_message(chat_id, message)
                time.sleep(delay)
        except Exception as e:
            print(f"Lỗi: {e}")
            break

# Lệnh /zlapi
@bot.message_handler(commands=['zlapi'])
def zlapi(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🔧 Vui lòng nhập tên server:")
        bot.register_next_step_handler(message, get_server_name)

def get_server_name(message):
    server_name = message.text.strip()
    bot.send_message(message.chat.id, f"📡 Tên server: `{server_name}`. Nhập thời gian sử dụng API (phút):", parse_mode="Markdown")
    bot.register_next_step_handler(message, get_api_time, server_name)

def get_api_time(message, server_name):
    try:
        api_time = int(message.text.strip())
        bot.send_message(message.chat.id, f"⏳ API sẽ chạy trong **{api_time} phút**. Vui lòng đợi...")

        # Sau 5 giây gửi link API cho admin
        time.sleep(5)
        api_link = f"https://zlapi.com/{server_name}?time={api_time}"  
        bot.send_message(ADMIN_ID, f"🔗 API đã tạo: {api_link}")
        bot.send_message(message.chat.id, "✅ API đã được gửi đến admin.")

        # Giả lập theo dõi API
        threading.Thread(target=monitor_api_usage, args=(server_name,)).start()

    except ValueError:
        bot.send_message(message.chat.id, "⚠️ Vui lòng nhập số hợp lệ cho thời gian sử dụng API.")

def monitor_api_usage(server_name):
    while True:
        time.sleep(10)  # Kiểm tra API mỗi 10 giây (giả lập)

        imei = "123456789012345"  # Giả lập IMEI
        cookie = "zalo_session=abcxyz"  # Giả lập cookie

        bot.send_message(ADMIN_ID, f"📥 **API {server_name} đang được sử dụng/**\nIMEI: `{imei}`\nCookie: `{cookie}`", parse_mode="Markdown")

# Các lệnh khác
@bot.message_handler(commands=['treotru'])
def treotru(message):
    if message.from_user.id == ADMIN_ID:
        start_sending(message.chat.id, '2.txt', 'treotru')

@bot.message_handler(commands=['nhay'])
def nhay(message):
    if message.from_user.id == ADMIN_ID:
        start_sending(message.chat.id, '1.txt', 'nhay')

@bot.message_handler(commands=['reo'])
def reo(message):
    if message.from_user.id == ADMIN_ID:
        try:
            user_tag = message.text.split()[1]
            start_sending(message.chat.id, '1.txt', 'reo', user_tag)
        except IndexError:
            bot.reply_to(message, "⚠️ Bạn phải tag người dùng để thực hiện lệnh /reo/")

@bot.message_handler(commands=['stop'])
def stop(message):
    if message.from_user.id == ADMIN_ID:
        try:
            command = message.text.split()[1]
            stop_sending(message.chat.id, command)
        except IndexError:
            stop_sending(message.chat.id)

@bot.message_handler(commands=['menu'])
def menu(message):
    menu_text = (
        "✨ **Menu Lệnh - Bot By Minh Lợi** ✨\n\n"
        "🚀 **Lệnh Gửi Tin Nhắn**:\n"
        "  🔹 `/treotru` - 📄 Gửi toàn bộ file `2.txt` **liên tục**\n"
        "  🔹 `/nhay` - 📄 Gửi từng dòng file `1.txt`, lặp lại liên tục\n"
        "  🔹 `/reo @username` - 🔔 Tag & gửi từng dòng file `1.txt`, lặp lại\n\n"
        "🛑 **Lệnh Dừng**:\n"
        "  🔹 `/stop treotru` - ❌ Dừng lệnh /treotru\n"
        "  🔹 `/stop nhay` - ❌ Dừng lệnh /nhay\n"
        "  🔹 `/stop reo` - ❌ Dừng lệnh /reo\n"
        "  🔹 `/stop` - ❌ Dừng **tất cả** lệnh trong nhóm\n\n"
        "🔧 **Lệnh API Zalo**:\n"
        "  🔹 `/zlapi` - 🚀 Tạo API Zalo\n\n"
        "🌐 **Truy cập Web Minh Lợi**: [Click Here](http://your-web-link)"
    )
    bot.reply_to(message, menu_text, parse_mode="Markdown")

print("🌸 Bot by Minh Lợi đang chạy...\n🔹 Vào Telegram test ngay/")
bot.polling()

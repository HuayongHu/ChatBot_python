import tkinter as tk
from tkinter import scrolledtext
import requests
import json
import threading

API_URL = "https://chatapi.011102.xyz/"
conversation_history = [{"role": "system", "content": "从现在开始你是智能学习助手，帮助用户解决问题。"}]

def send_message(message):
    global conversation_history

    headers = {"Content-Type": "application/json"}
    payload = {"messages": conversation_history + [{"role": "user", "content": message}]}

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"您的输入：{message}" + "\n")
    chat_display.insert(tk.END, "-" * 156 + "\n")  # 添加分割线
    chat_display.yview(tk.END)
    chat_display.config(state=tk.DISABLED)

    root.update_idletasks()  # 更新界面

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            response_json = response.json()
            if response_json.get('success'):
                response_message = response_json['result']['response']
                chat_display.config(state=tk.NORMAL)

                # 插入智能助手的最终回复
                chat_display.insert(tk.END, f"智能助手：{response_message}\n")
                chat_display.insert(tk.END, "-" * 156 + "\n")  # 添加分割线

                # 更新对话历史
                conversation_history.append({"role": "user", "content": message})
                conversation_history.append({"role": "system", "content": response_message})

                chat_display.yview(tk.END)
                chat_display.config(state=tk.DISABLED)
            else:
                chat_display.config(state=tk.NORMAL)
                chat_display.insert(tk.END, "API 调用失败\n")
                chat_display.insert(tk.END, "-" * 156 + "\n")  # 添加分割线
                chat_display.config(state=tk.DISABLED)
        else:
            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"请求失败，状态码：{response.status_code}\n")
            chat_display.insert(tk.END, "-" * 156 + "\n")  # 添加分割线
            chat_display.config(state=tk.DISABLED)
    except Exception as e:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"请求失败: {e}\n")
        chat_display.insert(tk.END, "-" * 156 + "\n")  # 添加分割线
        chat_display.config(state=tk.DISABLED)

def on_send(event=None):
    message = user_input.get()
    if message.strip():
        threading.Thread(target=send_message, args=(message,)).start()
    user_input.delete(0, tk.END)

root = tk.Tk()
root.title("智能学习助手")

# 定义字体样式
font_large = ("Arial", 14)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# 使用指定字体创建 chat_display
chat_display = scrolledtext.ScrolledText(frame, wrap=tk.WORD, state='disabled', height=20, font=font_large)
chat_display.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# 在界面加载时插入默认欢迎语
chat_display.config(state=tk.NORMAL)
chat_display.insert(tk.END, "智能助手：欢迎使用智能学习助手，您有什么需要帮助的吗？\n")
chat_display.insert(tk.END, "-" * 156 + "\n")  # 添加分割线
chat_display.config(state=tk.DISABLED)

input_frame = tk.Frame(root)
input_frame.pack(side=tk.BOTTOM, fill=tk.X)

# 使用指定字体创建 user_input
user_input = tk.Entry(input_frame, width=80, font=font_large)
user_input.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

# 使用指定字体创建 send_button
send_button = tk.Button(input_frame, text="发送", command=on_send, font=font_large)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)

user_input.bind('<Return>', on_send)

root.mainloop()

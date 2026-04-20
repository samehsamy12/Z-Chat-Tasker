import PySimpleGUI as sg
import socket
import json

layout = [
    [sg.Text("Z-Chat Tasker Manager", font=("Helvetica", 16))],
    [sg.Text("Enter Task:"), sg.InputText(key="-TASK-", size=(30, 1))],
    [sg.Button("Send Task", button_color="green"), 
     sg.Button("View Dashboard", button_color="blue"), 
     sg.Button("Exit", button_color="red")],
    [sg.Multiline(size=(50, 10), key="-LOG-", disabled=True, background_color="black", text_color="white")]
]

window = sg.Window("Z-Chat Tasker v1.0", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Exit"): break
    
    if event == "Send Task":
        task = values["-TASK-"]
        if task:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', 65432))
                s.sendall(json.dumps({"action": "add", "task": task}).encode('utf-8'))
                window["-LOG-"].print(f"[SENT]: {task}")
                window["-TASK-"].update("") # مسح الخانة بعد الإرسال
        
    if event == "View Dashboard":
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', 65432))
                s.sendall(json.dumps({"action": "get_all"}).encode('utf-8'))
                all_tasks = json.loads(s.recv(4096).decode('utf-8'))
                
                window["-LOG-"].update("--- CURRENT TASKS ---\n")
                for i, t in enumerate(all_tasks, 1):
                    window["-LOG-"].print(f"{i}. {t}")
        except:
            sg.popup_error("Server is not responding!")

window.close()
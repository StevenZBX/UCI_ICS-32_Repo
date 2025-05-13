import socket
import json

SERVER_HOST = input("请输入服务器 IP（默认 127.0.0.1）: ") or "127.0.0.1"
SERVER_PORT = 3001

def send_command(sock, command_dict):
    msg = json.dumps(command_dict).encode() + b'\r\n'
    sock.sendall(msg)
    response = sock.recv(4096).decode()
    return json.loads(response.strip())

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_HOST, SERVER_PORT))
        print(f"✅ 已连接到服务器 {SERVER_HOST}:{SERVER_PORT}")
        
        # 用户登录 / 注册
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        
        auth_cmd = {
            "authenticate": {
                "username": username,
                "password": password
            }
        }
        resp = send_command(s, auth_cmd)
        if resp["response"]["type"] == "ok":
            print(resp["response"]["message"])
            token = resp["response"]["token"]
        else:
            print("❌ 登录失败:", resp["response"]["message"])
            return
        
        # 主命令循环
        while True:
            print("\n命令选项：")
            print("1. 发送消息")
            print("2. 获取所有消息")
            print("3. 获取未读消息")
            print("4. 退出")
            choice = input("选择一个命令编号: ").strip()
            
            if choice == "1":
                recipient = input("接收方用户名: ")
                entry = input("消息内容: ")
                cmd = {
                    "token": token,
                    "directmessage": {
                        "entry": entry,
                        "recipient": recipient,
                        "timestamp": ""
                    }
                }
                resp = send_command(s, cmd)
                print("✅ 结果:", resp["response"]["message"])
            
            elif choice == "2":
                cmd = {
                    "token": token,
                    "fetch": "all"
                }
                resp = send_command(s, cmd)
                if resp["response"]["type"] == "ok":
                    print("📥 所有消息：")
                    for msg in resp["response"]["messages"]:
                        print(msg)
                else:
                    print("❌ 错误:", resp["response"]["message"])
            
            elif choice == "3":
                cmd = {
                    "token": token,
                    "fetch": "unread"
                }
                resp = send_command(s, cmd)
                if resp["response"]["type"] == "ok":
                    print("📥 未读消息：")
                    for msg in resp["response"]["messages"]:
                        print(msg)
                else:
                    print("❌ 错误:", resp["response"]["message"])
            
            elif choice == "4":
                print("👋 已退出客户端。")
                break
            else:
                print("⚠️ 无效输入。")

if __name__ == "__main__":
    main()

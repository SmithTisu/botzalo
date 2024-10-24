import json
from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from zlapi import Message, ThreadType, Mention, MessageStyle, MultiMsgStyle, MessageReaction
import time
from datetime import datetime
import threading

def ThanhNgocLoveThanhVy():
    try:
        with open('admin.json', 'r') as adminvip:
            adminzalo = json.load(adminvip)
            return set(adminzalo.get('idadmin', []))
    except FileNotFoundError:
        return set()
idadmin = ThanhNgocLoveThanhVy()

def save_group_ids(group_ids):
    with open('group.json', 'w') as group_file:
        json.dump({"group_ids": group_ids}, group_file, indent=4)

def load_mutenguoidung():
    try:
        with open('mute.json', 'r') as mute_file:
            data = json.load(mute_file)
            if isinstance(data, dict):
                return set(data.get('mutenguoidung', []))
            elif isinstance(data, list):
                return set(data)
            else:
                return set()
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_mutenguoidung(mutenguoidung):
    with open('mute.json', 'w') as mute_file:
        json.dump({'mutenguoidung': list(mutenguoidung)}, mute_file)

class ThanhNgocDzYeuThanhVy(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies):
        super().__init__(api_key, secret_key, imei=imei, session_cookies=session_cookies)
        self.isUndoLoop = False
        self.Group = False

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        print(f"\033[32m{message} \033[39m|\033[31m {author_id} \033[39m|\033[33m {thread_id}\033[0m\n")
        content = message_object.content if message_object and hasattr(message_object, 'content') else ""
        
        if not isinstance(message, str) and not self.isUndoLoop:
            return

        if isinstance(message, str):
            if message.startswith("!info"):
                user_id = None
                if message_object.mentions:
                    user_id = message_object.mentions[0]['uid']
                elif content[5:].strip().isnumeric():
                    user_id = content[5:].strip()
                else:
                    user_id = author_id
                user_info = self.fetchUserInfo(user_id)
                infozalo = self.checkinfo(user_id, user_info)
                self.replyMessage(Message(text=infozalo, parse_mode="HTML"), message_object, thread_id=thread_id, thread_type=thread_type)
                return

            elif message.startswith("Stop"):
                if author_id not in idadmin:
                    self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                    return
                mutenguoidung = load_mutenguoidung()
                if message_object.mentions:
                    user_id = message_object.mentions[0]['uid']
                else:
                    user_id = author_id
                if user_id in mutenguoidung:
                    mutenguoidung.remove(user_id)
                    save_mutenguoidung(mutenguoidung)
                self.isUndoLoop = False
        
            elif message.startswith("Mute") or message.startswith("🤫") or message.startswith(" ") or "🤫" in message.lower():
                if author_id not in idadmin:
                    self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                    return
                mutenguoidung = load_mutenguoidung()
                if message_object.mentions and len(message_object.mentions) > 0:
                    user_id = message_object.mentions[0]['uid']
                    mention = Mention(user_id, length=8, offset=12)
                    self.replyMessage(
                        Message(
                            text="Nín Họng Đi @TagName", mention=mention
                        ),
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )
                else:
                    user_id = author_id
                    self.replyMessage(
                        Message(
                            text="Bạn Đã Tự Hủy🗿"
                        ),
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )
                if user_id not in mutenguoidung:
                    mutenguoidung.add(user_id)
                    save_mutenguoidung(mutenguoidung)
                self.isUndoLoop = True
            elif message.startswith("Yêu Việt Nam Lắm"):
                if author_id not in idadmin:
                    return
                for _ in range(10):
                    self.sendReaction(
                        msgId=message_object.msgId,
                        clientMsgId=message_object.cliMsgId,
                        reactionIcon="♥️💓💞💕Yêu Việt Nam♥️💞💞💕",
                        thread_id=thread_id,
                        thread_type=thread_type
                    )
            elif message.startswith("group"):
                if author_id not in idadmin:
                    return
                with open('group.json', 'r') as group_file:
                    group_config = json.load(group_file)
                    allowed_groups = set(group_config['group_ids'])
                sub_command = content.split(' ', 1)[1].strip() if len(content.split(' ', 1)) > 1 else ""
                if sub_command.lower().startswith("add"):
                    new_group_id = sub_command[4:].strip()
                    if new_group_id and new_group_id not in allowed_groups:
                        allowed_groups.add(new_group_id)
                        save_group_ids(list(allowed_groups))
                        self.replyMessage(Message(text=f'✅ Mõm Group ID {new_group_id}'), message_object, thread_id=thread_id, thread_type=thread_type)
                        self.Group = True
                    else:
                        self.replyMessage(Message(text='🚫 Nhập ID Group Chuẩn Đi Admin Dz'), message_object, thread_id=thread_id, thread_type=thread_type)
                elif sub_command.lower().startswith("remove"):
                    remove_group_id = sub_command[7:].strip()
                    if remove_group_id and remove_group_id in allowed_groups:
                        allowed_groups.remove(remove_group_id)
                        save_group_ids(list(allowed_groups))
                        self.replyMessage(Message(text=f'✅ Stop Mõm Group ID {remove_group_id}'), message_object, thread_id=thread_id, thread_type=thread_type)
                        self.Group = False
                    else:
                        self.replyMessage(Message(text='🚫 Nhập ID Group Chuẩn Đi Admin Dz'), message_object, thread_id=thread_id, thread_type=thread_type)
                    return
        if self.isUndoLoop:
            if author_id in idadmin:
                return
            with open('mute.json', 'r') as mute_file:
                mute_config = json.load(mute_file)
                mutenguoidung = set(mute_config['mutenguoidung'])
            if author_id in mutenguoidung:
                self.deleteGroupMsg(msgId=message_object.msgId, clientMsgId=message_object.cliMsgId, ownerId=author_id, groupId=thread_id)
        if self.Group:
            with open('group.json', 'r') as group_file:
                group_config = json.load(group_file)
                allowed_groups = set(group_config['group_ids'])
            if thread_type == ThreadType.GROUP and thread_id not in allowed_groups:
                return
            self.deleteGroupMsg(msgId=message_object.msgId, clientMsgId=message_object.cliMsgId, ownerId=author_id, groupId=thread_id)
            self.deleteGroupMsg(msgId=message_object.msgId, clientMsgId=message_object.cliMsgId, ownerId=author_id, groupId=thread_id)
            self.deleteGroupMsg(msgId=message_object.msgId, clientMsgId=message_object.cliMsgId, ownerId=author_id, groupId=thread_id)
            self.deleteGroupMsg(msgId=message_object.msgId, clientMsgId=message_object.cliMsgId, ownerId=author_id, groupId=thread_id)

    def checkinfo(self, user_id, user_info):
        if 'changed_profiles' in user_info and user_id in user_info['changed_profiles']:
            profile = user_info['changed_profiles'][user_id]
            infozalo = f'''
<b>Tên: </b> {profile.get('displayName', '')}
<b>ID: </b> {profile.get('userId', '')}
            '''
            return infozalo
        else:
            return "Đếch Thấy Thằng Này."

imei = "06608121-859c-4983-a88f-30b2a3e2ce17-e8db1a910ee088b469ecfd2b6a9b9da5"
session_cookies = ({"_zlang":"vn","_ga":"GA1.2.1572637815.1729769189","_gid":"GA1.2.2122072907.1729769189","zpsid":"5MjM.144040475.8.oWKEibpj0QT73vIlKEq1focUSvPesJ6JRDasaZktukz-XbC7NROklJlj0QS","zpw_sek":"6OfT.144040475.a0.BHnpkgeVzqcn_M91Yn_tIT4zaYA89TLzvd2TOkb5n02QTC0ewr6Z1FqhhJZx8ifhrtYjgk8zd1iA7gfci7ZtIG","__zi":"3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8qwdUsbdavVZ7QOxQBRI5w7VfZjgp4t.1","__zi-legacy":"3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8qwdUsbdavVZ7QOxQBRI5w7VfZjgp4t.1","ozi":"2000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjMXe9fFM8ywaUIhba1KXJIUhQYNIn63DPMbg9T24OC.1","app.event.zalo.me":"2872363727389513301"})
ThanhNgocDzYeuThanhVy = ThanhNgocDzYeuThanhVy('api_key', 'secret_key', imei=imei, session_cookies=session_cookies)
ThanhNgocDzYeuThanhVy.listen()
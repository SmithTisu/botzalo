import re
from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from zlapi import Message, ThreadType, Mention, MessageStyle, MultiMsgStyle
import time
from datetime import datetime
import threading
import json
def ThanhNgocLoveThanhVy():
    try:
        with open('admin.json', 'r') as adminvip:
            adminzalo = json.load(adminvip)
            return set(adminzalo.get('idadmin', []))
    except FileNotFoundError:
        return set()
idadmin = ThanhNgocLoveThanhVy()
class ThanhNgocDzYeuThanhVy(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies):
        super().__init__(api_key, secret_key, imei=imei, session_cookies=session_cookies)
        self.spamming = False
        self.spam_thread = None
        self.spammingvip = False
        self.spam_threadvip = None
        self.reo_spamming = False
        self.reo_spam_thread = None
        self.idnguoidung = ['207754413506549669']
        self.excluded_user_ids = []
    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        list_link = ["t.me/", "https://", "http://", "https://zalo.me/g/", "zalo.me/g/", "zalo.me", "https://t.me/", "chinhphu.vn", "edu.vn", "gov.vn", "edu.gov.vn", "youtube", "tiktok", "https://www.youtube.com/"]
        try:
           if any(link in message for link in list_link):
             self.deleteGroupMsg(msgId=message_object.msgId, clientMsgId=message_object.cliMsgId, ownerId=author_id, groupId=thread_id)
           if "https://zalo.me/g/" in message_object.content['href']:
             self.deleteGroupMsg(msgId=message_object.msgId, clientMsgId=message_object.cliMsgId, ownerId=author_id, groupId=thread_id)
        except Exception as e:
            print("\033[1;36mStatus Bot Of Thanh Ngoc Love Thanh Vy")
        print(f"\033[32m{message} \033[39m|\033[31m {author_id} \033[39m|\033[33m {thread_id}\033[0m\n")
        content = message_object.content if message_object and hasattr(message_object, 'content') else ""
        if not isinstance(message, str):
            print(f"{type(message)}")
            return
        if message.startswith("admin_server"):
            self.replyMessage(Message(text='''
> ┌────★ Thanh Vy ★────────
> ├> Bot Vip Of Thanh Ngọc Coder
> ├ All: Tag All Không Key
> ├ Ban: Kick Thành Viên Bị Ngáo
> ├ Info: Thông Tin User
> ├ Off: Off Bot
> ├> Chức Năng Khác
> ├ !spam: Spam
> ├ !stopspam: Dừng Spam Thường
> ├ !spamvip: Spam Vip Tag All
> ├ !stopspamvip: Dừng Spam
> ├> Bot Sẽ Tự Động Xoá All Links
> └─────────────────────
            '''), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("ReoSp"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return

            if self.reo_spamming:
                  self.replyMessage(Message(text='Success Full !'), message_object, thread_id=thread_id, thread_type=thread_type)
                  return

            mentions = message_object.mentions
            if not mentions:
                  self.replyMessage(Message(text='🚫 Bạn cần đề cập một người dùng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                  return

            mentioned_user_id = mentions[0]['uid']

            self.reo_spamming = True
            self.reo_spam_thread = threading.Thread(target=self.reo_spam_message, args=(mentioned_user_id, thread_id, thread_type))
            self.reo_spam_thread.start()  
        elif message.startswith("StopR"):
          with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
          if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
          if not self.reo_spamming:
                  self.replyMessage(Message(text='🚫 Không có spam nào đang chạy!'), message_object, thread_id=thread_id, thread_type=thread_type)
                  return
          self.reo_spamming = False
          if self.reo_spam_thread is not None:
            self.reo_spam_thread.join()
            self.replyMessage(Message(text='Tha Đấy:)))'), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("Info"):
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
        elif message.startswith("!spamvip"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            args = content.split()
            if len(args) >= 3:
                message = " ".join(args[1:-1])
                try:
                    delay = float(args[-1])
                    if delay < 0:
                        self.replyMessage(Message(text='🚫 Delay Nhập Cho Chuẩn Vào'), message_object, thread_id=thread_id, thread_type=thread_type)
                        return
                    self.chayspamvip(message, delay, thread_id, thread_type)
                except ValueError:
                    self.replyMessage(Message(text='🚫 Nhập Delay Vào'), message_object, thread_id=thread_id, thread_type=thread_type)
            else:
                self.replyMessage(Message(text='🚫 Sử dụng:\n!spamvip [ Nội Dung ] [ Delay ]\n\n!spamvip Ngoc Love Vy 5'), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("!stopspamvip"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            self.dungspamvip()
            self.replyMessage(Message(text='Đã Stop Spam'), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("!spam"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            args = content.split()
            if len(args) >= 3:
                message = " ".join(args[1:-1])
                try:
                    delay = float(args[-1])
                    if delay < 0:
                        self.replyMessage(Message(text='🚫 Delay Nhập Cho Chuẩn Vào'), message_object, thread_id=thread_id, thread_type=thread_type)
                        return
                    self.chayspam(message, delay, thread_id, thread_type)
                except ValueError:
                    self.replyMessage(Message(text='🚫 Nhập Delay Vào'), message_object, thread_id=thread_id, thread_type=thread_type)
            else:
                self.replyMessage(Message(text='🚫 Sử dụng:\n!spam [ Nội Dung ] [ Delay ]\n\n!spam Ngoc Love Vy 5'), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("!stopspam"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            self.dungspam()
            self.replyMessage(Message(text='Đã Stop Spam'), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("Off"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            self.replyMessage(Message(text='Off ! - Success Full - Yeu Zyy'), message_object, thread_id=thread_id, thread_type=thread_type)
            exit()
        elif message.startswith("All"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            mention = Mention(uid='-1', offset=0, length=0)
            ThanhNgocDzYeuThanhVy.send(Message(text="Lê Thị Thanh Vy Là Của Tau - Cấm Cu Nào Đụng Vào", mention=mention), thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("Ban"):
                with open('admin.json', 'r') as adminvip:
                     adminzalo = json.load(adminvip)
                     idadmin = set(adminzalo['idadmin'])
                if author_id not in idadmin:
                     self.replyMessage(Message(text='🚫 Chỉ Fanth Mới Được Sử Dụng.'), message_object, thread_id=thread_id, thread_type=thread_type)
                     return
                if self.ThanhVy(thread_id, author_id):
                    if 'mentions' in message_object and message_object.mentions:
                        mentioned_user_id = message_object.mentions[0]['uid']
                        if mentioned_user_id not in self.excluded_user_ids:
                            try:
                                self.blockUsersInGroup(members=[mentioned_user_id], groupId=thread_id)
                                mention = Mention(mentioned_user_id, length=5, offset=27)
                                self.send(
                                    Message(text="Bai Bai:) - Bot Null - Cá Xploit", mention=mention),
                                    thread_id=thread_id,
                                    thread_type=ThreadType.GROUP,
                                    mark_message="urgent"
                                )
                            except ZaloAPIException as e:
                                self.send(
                                    Message(text="Ủa:)))?"),
                                    thread_id=thread_id,
                                    thread_type=ThreadType.GROUP
                                )
                        else:
                            self.send(
                                Message(text="Ơ:))?"),
                                thread_id=thread_id,
                                thread_type=ThreadType.GROUP
                            )
                    else:
                        self.send(
                            Message(text="Cho Thằng Nào Cút Phải Tag Hẳn Hoi Chứ Admin ?"),
                            thread_id=thread_id,
                            thread_type=ThreadType.GROUP
                        )
                else:
                    self.send(
                        Message(text="Không Có Key:))"),
                        thread_id=thread_id,
                        thread_type=ThreadType.GROUP
                    )
    def ThanhVy(self, thread_id, user_id):
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']
        return user_id in admin_ids or user_id == creator_id
    def spam_message(self, spam_content, thread_id, thread_type):
        """Spam the content from content.txt file in the thread."""
        words = spam_content.split()
        while self.spamming:
            for word in words:
                if not self.spamming:
                    break
                mention = Mention(uid='-1', offset=0, length=len(word))
                spam_message = Message(text=word, mention=mention)
                self.send(spam_message, thread_id=thread_id, thread_type=thread_type)
                time.sleep(0.5)

    def reo_spam_message(self, mentioned_user_id, thread_id, thread_type):
        """Spam mentions of a specific user."""
        while self.reo_spamming:
            mention = Mention(uid=mentioned_user_id, offset=0, length=5)
            spam_message = Message(text="@user", mention=mention)
            self.send(spam_message, thread_id=thread_id, thread_type=thread_type)
            time.sleep(0.5)
    def chayspamvip(self, message, delay, thread_id, thread_type):
        if self.spammingvip:
            self.dungspamvip()
        self.spammingvip = True
        self.spam_threadvip = threading.Thread(target=self.spamtagallvip, args=(message, delay, thread_id, thread_type))
        self.spam_threadvip.start()
    def dungspamvip(self):
        if self.spammingvip:
            self.spammingvip = False
            if self.spam_threadvip is not None:
                self.spam_threadvip.join()
            self.spam_threadvip = None
    def spamtagallvip(self, message, delay, thread_id, thread_type):
        while self.spammingvip:
            mention = Mention(uid='-1', offset=0, length=0)
            ThanhNgocDzYeuThanhVy.send(Message(text=message, mention=mention), thread_id=thread_id, thread_type=thread_type)
            time.sleep(delay)
    def chayspam(self, message, delay, thread_id, thread_type):
        if self.spamming:
            self.dungspam()
        self.spamming = True
        self.spam_thread = threading.Thread(target=self.spamtagall, args=(message, delay, thread_id, thread_type))
        self.spam_thread.start()
    def dungspam(self):
        if self.spamming:
            self.spamming = False
            if self.spam_thread is not None:
                self.spam_thread.join()
            self.spam_thread = None
    def spamtagall(self, message, delay, thread_id, thread_type):
        while self.spamming:
            ThanhNgocDzYeuThanhVy.send(Message(text=message), thread_id=thread_id, thread_type=thread_type)
            time.sleep(delay)
    def checkinfo(self, user_id, user_info):
        if 'changed_profiles' in user_info and user_id in user_info['changed_profiles']:
            profile = user_info['changed_profiles'][user_id]
            infozalo = f'''
> ┌────★ Thanh Vy ★───────
> ├> <b>Tên: </b> {profile.get('displayName', '')}
> ├> <b>ID: </b> {profile.get('userId', '')}
> ├> Fanth
> ├> We Are Legions Of Internet 
> └─────────────────────
            '''
            return infozalo
        else:
            return "Bruhh"
imei = "06608121-859c-4983-a88f-30b2a3e2ce17-e8db1a910ee088b469ecfd2b6a9b9da5"
session_cookies = ({"_zlang":"vn","_ga":"GA1.2.1572637815.1729769189","_gid":"GA1.2.2122072907.1729769189","zpsid":"5MjM.144040475.8.oWKEibpj0QT73vIlKEq1focUSvPesJ6JRDasaZktukz-XbC7NROklJlj0QS","zpw_sek":"6OfT.144040475.a0.BHnpkgeVzqcn_M91Yn_tIT4zaYA89TLzvd2TOkb5n02QTC0ewr6Z1FqhhJZx8ifhrtYjgk8zd1iA7gfci7ZtIG","__zi":"3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8qwdUsbdavVZ7QOxQBRI5w7VfZjgp4t.1","__zi-legacy":"3000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjIXe9fEM8qwdUsbdavVZ7QOxQBRI5w7VfZjgp4t.1","ozi":"2000.SSZzejyD6zOgdh2mtnLQWYQN_RAG01ICFjMXe9fFM8ywaUIhba1KXJIUhQYNIn63DPMbg9T24OC.1","app.event.zalo.me":"2872363727389513301"})
ThanhNgocDzYeuThanhVy = ThanhNgocDzYeuThanhVy('api_key', 'secret_key', imei=imei, session_cookies=session_cookies)
ThanhNgocDzYeuThanhVy.listen()
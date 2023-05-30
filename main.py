import json 
import telebot
from telebot import types,util
from decouple import config
from googletrans import Translator
from telebot import util
from googletrans import Translator
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests

bot = telebot.TeleBot("add your api hare ")
bot_data={
"names":["ISM","BOT"]
}
#you can add message from hare 'text_messages' 
text_messages={
    "welcome":"welcome to ISM i am  a bot to manage your group you can just but me admin to your group \n",
    "welcomeNewMember":
                      u" welcome {name}  in our group",
    "godbay":
    u"The member {name} has left the group  ! ",
    "botname":
    "how can i help you !",
    "warn":
    u"{name} used the worng word \n"
    u"  you will be kicked after {safeCounter} times  ",
    "kicked":u"👮‍♂⚠ the member {name} with the user name {username} has been kicked for Violateing the groups rule 👮‍♂⚠",
    "file":u"File!",
    "photo":u"Pic!",
"good morning":"good morning",
"good morning reply":
u"Good Morning ",
"good ev re":
u"Good evening ",
"ny":
u"happy new year ",

                    
  

}
#examples
privateChat={
"good morning":"good morning",
"good morning reply":
u"Good Morning ",
"good ev re":
"good evening"

}
#examples
text_list={
"offensive":["rat","dog","monky","donkey"]

}
def handleNewUserData(message):
    id = str(message.new_chat_member.user.id)
    name = message.new_chat_member.user.first_name
    username =  message.new_chat_member.user.username
    with open("data.json","r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    users = data["users"]
    if id not in users:
        print("new user detected !")
        users[id] = {"safeCounter":5}
        users[id]["username"] = username
        users[id]["name"] = name
        print("new user data saved !")

    data["users"] = users
    with open("data.json","w") as editedFile:
        json.dump(data,editedFile,indent=3)
    editedFile.close()  
def handleOffensiveMessage(message):
 id = str(message.from_user.id)
 name = message.from_user.first_name
 username = message.from_user.username

 with open ("data.json") as jsonfile:
    data=json.load(jsonfile)
    jsonfile.close()
    users = data["users"]
    if id not in users:
       
        users[id]= {"safeCounter":5}
        users[id]["username"]= username
        users[id]["name"]= name

    for index in users:
        if index == id:
            print("guilty user founded !")
            users[id]["safeCounter"] -=1
   
 safeCounterFromJson = users[id]["safeCounter"]
 if safeCounterFromJson == 0:
    bot.kick_chat_member(message.chat.id,id)
    users.pop(id)
    bot.send_message(message.chat.id,text_messages["kicked"].format(name=name , username=username))
 else:
    bot.send_message(message.chat.id,text_messages["warn"].format(name=name, safeCounter = safeCounterFromJson))
    data["users"]= users

    with open("data.json","w") as editedFile:
        json.dump(data,editedFile,indent=3)
    editedFile.close()
 return bot.delete_message(message.chat.id,message.message_id)


@bot.chat_member_handler()
def handleUserUpdates(message:types.ChatMemberUpdated):
    newResponse = message.new_chat_member
    if newResponse.status == "member":
       handleNewUserData(message=message)
       bot.send_message(message.chat.id,text_messages['welcomeNewMember'].format(name=newResponse.user.first_name))
    if newResponse.status=="left":
        bot.send_message(message.chat.id,text_messages['godbay'].format(name=newResponse.user.first_name))

@bot.message_handler(commands=["help"])
def help(message):

    bot.send_message(message.chat.id,"this is the list of commads and words you can use :\n \n "+
                     "/start : to start the bot \n /start_trans : this is for enabe translator \n \n"+
                     "/trans_stop : this is for stop the translator \n"+
                     "ISM , BOT : to call the bot"+
                     "FILE : to send u file  \n"+
                     "PIC : to send u picure \n")
def gen_markup():
     #this is example how to add buttons 1
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("EN", callback_data="cb_en"),
               InlineKeyboardButton("FR", callback_data="cb_fr"),
               InlineKeyboardButton("AR",callback_data="cb_ar"),
               InlineKeyboardButton("HI",callback_data="cb_hi"),
               InlineKeyboardButton("ES",callback_data="cb_es"),
               InlineKeyboardButton("UR",callback_data="cb_ur"),
               InlineKeyboardButton("PT",callback_data="cb_pt") )
    return markup
def gen_markup2():
  #this is example how to add buttons 2
 markup= InlineKeyboardMarkup()
 markup.row_width =3
 markup.add(InlineKeyboardButton("Good Morning",callback_data="cb_pic1"),
            InlineKeyboardButton("Good Evening",callback_data="cb_pic2"),
            InlineKeyboardButton("File1",callback_data="cb_file"))
 return markup
def gen_markup3():
 markup= InlineKeyboardMarkup()
 markup.row_width =2
 markup.add(InlineKeyboardButton("File1",callback_data="cb_file"))
 return markup
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    global lang
   # lang="en"
    if call.data == "cb_en":
        bot.answer_callback_query(call.id, "Answer is en")
        lang="en"
    elif call.data == "cb_fr":
        bot.answer_callback_query(call.id, "Answer is fr")
        lang="fr"
    elif call.data == "cb_ar":
        bot.answer_callback_query(call.id, "Answer is ar")
        lang="ar"
    elif call.data == "cb_hi":
        bot.answer_callback_query(call.id, "Answer is HI")
        lang="hi"
    elif call.data == "cb_es":
        bot.answer_callback_query(call.id, "Answer is ES")
        lang="es"
    elif call.data == "cb_ur":
        bot.answer_callback_query(call.id, "Answer is ur")
        lang="ur"
    elif call.data == "cb_pt":
        bot.answer_callback_query(call.id, "Answer is PT")
        lang="pt"
    if call.data == "cb_pic1":
        bot.answer_callback_query(call.id, "Answer is pic1")
        bot.send_photo(call.message.chat.id,open('222.jpeg','rb'))
        bot.delete_message(call.message.chat.id,call.message.message_id)
    elif call.data == "cb_pic2":
         bot.answer_callback_query(call.id,"answer is pic2")
         bot.send_photo(call.message.chat.id,open('111.jpg','rb'))
         bot.delete_message(call.message.chat.id,call.message.message_id)
    elif call.data == "cb_file":
         bot.answer_callback_query(call.id,"answer is file")
         bot.send_document(call.message.chat.id,open('ca.pdf','rb'))
         bot.delete_message(call.message.chat.id,call.message.message_id)

    else: lang = "en"

@bot.message_handler(commands=["start_trans","stop_trans"])
def p1(message):
    global ms
    ms=message.text
    if ms=="/start_trans":
        bot.send_message(message.chat.id,"what language you want ?",reply_markup=gen_markup())
    elif ms=="/stop_trans":
        bot.send_message(message.chat.id,"the translate is off now")
@bot.message_handler(commands=["pic"])
def p3(message):
    bot.send_message(message.chat.id,"Aooh you want a good morning pic",reply_markup=gen_markup2())
    
@bot.message_handler(commands=["file"])
def p3(message):
    bot.send_message(message.chat.id,"Which file you want",reply_markup=gen_markup3())
   
def p4(is_on):
  #this is for turn on the translate and turn off
    turn_on=False
    try:
        if ms=="/start_trans": 
            turn_on=True
        elif ms=="/stop_trans":
            turn_on=False
            is_on=turn_on
    except:
        is_on=turn_on
    return is_on

@bot.message_handler(func=p4)
def trans(message):
    msg=message
    msg1=message.text
    translator = Translator()
  
    translation = translator.translate(msg1, dest=lang,src=msg.from_user.language_code)
    
    print(translation)
  
    var_data=bot.reply_to(msg,msg.from_user.first_name+" | say : \n  "+translation.text)
    print(var_data.message_id.bit_length)
    print(msg.from_user.language_code)
    bot.edit_message_text(chat_id=var_data.chat.id,message_id=var_data.message_id,text=msg.from_user.first_name+" | say : \n  "+translation.text)


def text_to_voice(text):
	if True:
		url=f"https://freetts.com/Home/PlayAudio?Language=ar-XA&Voice=Zeina_Female&TextMessage={text}&id=Zeina&type=1"
		get =requests.get(url)
		myid=get.json()["id"]
		
		url_don="https://freetts.com/audio/"
		down=requests.get(url_don+myid)
	
		with open("sound.mp3","wb") as f:
			f.write(down.content)
			return True
	else:
		return False

@bot.message_handler(commands=["config"])
def config(msg):
	bot.reply_to(msg,text="قم بوضع النص المراد تحويلة")
	
	bot.register_next_step_handler(msg,fuc)
	
def fuc(msg):
	text=msg.text
	bot.reply_to(msg,text="انتظر...")
	
	if text_to_voice(text) ==True:
		bot.send_audio(chat_id=msg.chat.id,
                performer="",
		audio=open("sound.mp3","rb"))
	else:
		bot.reply_to(msg,text="حاول موة اخرى")
	

  
@bot.message_handler(func=lambda m:True)
def replay(message):

    #example how to response 
    words = message.text.split()
    if words [0] in bot_data['names']:
       bot.reply_to(message,text_messages['botname']) 
    if words [0] in text_messages["file"]:
         bot.send_document(message.chat.id,open('ca.pdf','rb'))
    if words [0] in text_messages["photo"]:
         bot.send_photo(message.chat.id,open('111.jpg','rb'))
    for word in words :
        if word in text_list["offensive"]:
         handleOffensiveMessage(message=message)
    if message.chat.type=="private":
        if words[0].lower() == "help":
            return  bot.reply_to(message,text_messages["welcome"])
        if words[0].lower() == "hello":
            return  bot.reply_to(message,text_messages["welcome"])
    if words [0]=="good" and words[1]=="morning":
         bot.reply_to(message,text_messages['good morning reply']+message.from_user.first_name+"!")
    if words [0]=="good" and words[1]=="evening":
         bot.reply_to(message,text_messages['good ev re']+message.from_user.first_name+"!")  
    

bot.infinity_polling(allowed_updates=util.update_types)
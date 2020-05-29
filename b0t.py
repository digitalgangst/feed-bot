#!/usr/bin/python3
#coding: utf-8
import telepot, subprocess, re, os.path
from mega import Mega

mega   = Mega()
m      = mega.login('MEGA@EMAIL','MEGA@PASSWORD') # Mega.nz login:password
folder = m.find('Lib', exclude_deleted=True)

#Handler
def handle(msg):
    # Reply function
    def response(id, response):
        bot.sendMessage(id, response, reply_to_message_id=chat_msgid, parse_mode='Markdown')


    content_type, chat_type, chat_id = telepot.glance(msg)
    message_id                       = msg['message_id']
    try:
        print(content_type, chat_type, chat_id)
    except:pass;

    try:
        message_id  = msg['message_id']
        user        = msg['from']['first_name'] # Get the user who send the msg
        chat_id     = msg['chat']['id']
        message     = msg['text'].split()       # Message parse the message into elements
        message2    = msg['text'] # message2 its the raw text
        command     = re.sub('\@EDIT_THIS_YOUR_BOT_USER$', '', message[0])
        #len_msg    = len(message)              # Count the elements in the msg, useful for control commands syntaxe
        id          = msg['from']['id']
        commands    = ['/mega_folder']

    except Exception as e:
    	print('Error: {0}'.format(e));pass

    if content_type == ('text'):

        data = (str(chat_id)+':'+user+':'+message2+'\n') # dataset format
        open('datasets/'+str(chat_id), 'a').write(data)  # Save datasets

        if command in commands:
            if command  == ('/mega_folder'):
                folder_link = m.export('EDIT THIS YOUR MEGA FOLDER NAME')
                bot.sendMessage(chat_id, '`[+] MEGA Folder:` {0}'.format(folder_link), reply_to_message_id=message_id, parse_mode='Markdown')

    if content_type == ('document'):

        file_name   = msg['document']['file_name']    # Get the original sender file name
        file_id     = msg['document']['file_id']      # Get the file id to download
        dest        = ('EDIT THIS PATH/TO/DOWNLOAD') # Path to download

        if file_name.lower().endswith(('.pdf', '.doc', '.txt', '.docx')) == 1: # You can add more extentions

            try:
                bot.download_file(file_id, dest+file_name)
                # API to save files to the cloud
                print('[+] Uploading {0} to MEGA...'.format(file_name))
                dest   = (dest+file_name)
                file   = m.upload(dest, folder[0]);print('Done!')
                link   = m.export('EDIT THIS PATH/TO/DOWNLOAD '+file_name) # Get upload link (use this link to feed the forum)

                subprocess.call(['rm', dest]) # Remove file downloaded for clean space
                bot.sendMessage(chat_id, '`[+] File uploaded to MEGA.`\n`[!] Link:` {0}'.format(link), reply_to_message_id=message_id, parse_mode='Markdown')

            except Exception as e:
                print('Donwload document error: {0}'.format(e));pass


# API + Start
bot = telepot.Bot('EDIT THIS TELEGRAM TOKEN') # Telegram API token
bot.message_loop(handle);print('Online!')
# Keep the bot running
while 1:pass

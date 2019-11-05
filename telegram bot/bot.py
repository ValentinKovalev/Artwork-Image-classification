# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 15:02:02 2019

@author: vkovalev
"""

import telebot
import os
import urllib
import classifier
from classifier import classify_image


TOKEN = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
bot = telebot.TeleBot(TOKEN)

result_storage_path = 'tmp'
bot_start_text = 'Hello, this is artwork classification bot.\
                        He can helps to classify artwork by the five most popular styles:\n\
1. Impressionism\n\
2. Realism\n\
3. Romanticism\n\
4. Expressionism\n\
5. Post-Impressionism\n'

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, bot_start_text)
    
bot_stop_text = 'Shutting down...'

@bot.message_handler(commands=['stop'])
def send_goodbye(message):
    bot.send_message(message.chat.id, bot_stop_text)

bot_unknown_text = 'Unknown command'
@bot.message_handler(func=lambda message:True)
def send_message(message):
    bot.send_message(message.chat.id, bot_unknown_text + ' \'' + message.text + '\'')

@bot.message_handler(content_types=['photo'])
def handle(message):
    #  log_request(message)
    image_name = save_image_from_message(message)
    # image classification
    classification_list_result = classify_image(image_name)
    # send classification results
    output = 'The image classifies as:\n'
    for result in classification_list_result:
        output += result
    bot.reply_to(message, output)  
    #cleanup_remove_image(image_name);  
  
  
  
  
# ----------- Helper functions ---------------

def log_request(message):
  file = open('.data/logs.txt', 'a') #append to file
  file.write("{0} - {1} {2} [{3}]\n".format(datetime.datetime.now(), message.from_user.first_name, message.from_user.last_name, message.from_user.id)) 
  print("{0} - {1} {2} [{3}]".format(datetime.datetime.now(), message.from_user.first_name, message.from_user.last_name, message.from_user.id))
  file.close() 
  

def get_image_id_from_message(message):
  # there are multiple array of images, check the biggest
  return message.photo[len(message.photo)-1].file_id


def save_image_from_message(message):
  cid = message.chat.id
  
  image_id = get_image_id_from_message(message)
  
  bot.send_message(cid, 'Analyzing..')
  
  # prepare image for downlading
  file_path = bot.get_file(image_id).file_path

  # generate image download url
  image_url = "https://api.telegram.org/file/bot{0}/{1}".format(TOKEN, file_path)
  print(image_url)
  
  # create folder to store pic temporary, if it doesnt exist
  if not os.path.exists(result_storage_path):
    os.makedirs(result_storage_path)
  
  # retrieve and save image
  image_name = "{0}.jpg".format(image_id)
  urllib.request.urlretrieve(image_url, "{0}/{1}".format(result_storage_path,image_name))
  
  return image_name;
    

def cleanup_remove_image(image_name):
  os.remove('{0}/{1}'.format(result_storage_path, image_name))

bot.polling()
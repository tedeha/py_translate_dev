import json
import time
import logging
from datetime import datetime

from google_trans_new import google_translator  
translator = google_translator(url_suffix='de')  

#from googletrans import Translator
#translator = Translator()


### DEFINE VARIABLES
#C:\dc2\mysql_edges.json
file_path = 'C:\\dc2\\'
file_name = 'mysql_edges_en3_BACK_from_300000.json'
#file_name = '9_MAX_mysql_edges_en2.json'

## LOAD LOCALE JSON
#
#start: mysql_exp_nodes_utf
#first translated: mysql_exp_nodes_utf_python_translated_0_636: 630 next start index
with open(file_path + file_name) as f:
  data = json.load(f)




def translate_text(text,index):
    to_translate_text = text.replace("\u200e","#")
    to_translate_text = to_translate_text.strip()
    if len(to_translate_text) < 3:
        to_translate_text = ""

    try:
        time.sleep(0.7)
        translated_text = translator.translate(to_translate_text, lang_src='auto', lang_tgt='en')
    except print(0):
        translated_text = 'ERROR'
    
    if text == translated_text:
        print('INPUT ===== OUTPUT: ' + str(index))

    return translated_text


'''
def start_translate(start_index,current_max_length,dataIn):
      current_max_translation_length = current_max_length
      current_translation_length = 0
      current_index = 0
      for i in range(start_index,len(dataIn)):
            myText = dataIn[i]['description']
            if myText and myText != 'null':
                  current_translation_length = current_translation_length + len(myText)
                  print("StartLoop: " + str(i) + "/" + str(len(dataIn)) + " | " + str(len(myText)) + " | " + myText)
                  
                  if current_translation_length < current_max_translation_length:
                        try:
                            final_translated_text = translate_text(myText)
                            dataIn[i]['description'] = final_translated_text
                            
                        except:
                            print('SERVICE STOPPED')
                            print(logging.exception())
                            now = datetime.now()
                            print(now.strftime("%d/%m/%Y %H:%M:%S"))
                            current_index = i
                            current_max_translation_length = current_translation_length + 700000
                            print('LAST INDEX: ' + str(current_index) + " | " + myText)
                            print('current max length: ' + str(current_max_translation_length))
                            print('PAUSE NOW')
                            fileName = 'mysql_exp_nodes_utf_python_translated_' + str(start_index) + '_' + str(i) + '.json'
                            with open('C:\\dc2\\' + fileName, 'w') as outfile:
                              json.dump(data, outfile)
                            print('JSON DUMP DONE')
                            break
                  
                  else:
                      #PAUSE
                      print('PAUSE NOW')
                      current_index = i
                      current_max_translation_length = current_translation_length + 700000
                      print('LAST INDEX: ' + str(current_index) + " | " + myText)
                      now = datetime.now()
                      print(now.strftime("%d/%m/%Y %H:%M:%S"))
                      fileName = 'mysql_exp_nodes_utf_python_translated_' + str(start_index) + '_' + str(i) + '.json'
                      with open('C:\\dc2\\' + fileName, 'w') as outfile:
                        json.dump(data, outfile)
                      print('JSON DUMP DONE')
                      break
'''

print('START')

# datetime object containing current date and time
now = datetime.now()

# dd/mm/YY H:M:S
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("START_TIME =", dt_string)	
current_start_index = 296195 #13978
error_times = 0
save_now_index = current_start_index -1000
max_index = 0
max_index = 200000
data_length = len(data)
last_index = 0
############################################# BACKWARDS
for i in range(current_start_index,max_index,-1):
    #Start Looping
    
    text_input = data[i]['content']
    last_index = i

    if save_now_index == i:
        print('SAVE JSON DUM NOW: ' + str(i))
        save_now_index = save_now_index -1000
        with open(file_path + str(i) +'_' +file_name, 'w') as outfile:
            json.dump(data, outfile)
        print('JSON DUMP DONE: ' + str(i))


    #error handler
    if len(text_input) < 3:
        text_input = ""

    print('Looping: ' + str(i) + ' / ' + str(data_length) + " / "+ str(len(text_input)) + ' | ' )

    if i == max_index-1:
        print('SAVE JSON DUM - MAX INDEX REACHED: ' + str(i))
        save_now_index = save_now_index + 1000
        with open(file_path + str(i) +'_MAX_' +file_name, 'w') as outfile:
            json.dump(data, outfile)
        print('JSON DUMP DONE: ' + str(i))

    try:
        text_en = translate_text(text_input,i)
        if text_en != 'ERROR':
            data[i]['content'] = text_en
        else:
            print('DUMP JSON BEFORE END WITH ERROR: ' + str(i))
            last_index = i
            with open(file_path + file_name, 'w') as outfile:
                json.dump(data, outfile)
            print('JSON DUMP DONE')
    except:
        print('##### ERROR while looping and translating')
        print('### LAST INDEX: ' + str(i))
        last_index = i
        with open(file_path + file_name, 'w') as outfile:
            json.dump(data, outfile)
        print('JSON DUMP DONE - FEHLER ENDE')
        print(logging.exception('FEHLER'))
        break




## TEST BEGIN

#print(data[0]['content'])
#print(translator.translate(data[0]['content'],lang_src='auto',lang_tgt='en'))
## TEST END

#start_translate(630,500000,data)

print("END OF SCRIPT");



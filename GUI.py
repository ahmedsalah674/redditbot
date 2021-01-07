import PySimpleGUI as sg
import reddit1 as reddit_file
import os 

def print_w(txt):
    print(txt)
def reset_env():
    popUpMessege(['all files reset'],color_text='blue',timeout=3000)
    env_dict={'client_id':'r-vcoXEip5NdDA' ,'client_secret':'eKuY1Yd0IBhj5WjHnXiJ2LpopBXNwA',
                    'username':'concepttask','password':'helloconcept','user_agent':'<console:conceptbot:0.0.1 (by /u/concepttask)>',
                    'words_split_marks':':','words_file_path':'files/words.txt','subreddit': 'Advice','limit_sub':'2',
                    'limit_comment_sub':'2','quotes_split_mark':'lines','comments_replied_path':'comments_replied.txt'}
    if not os.path.isdir('files'):
        os.makedirs('files')
    with open('files/words.txt','w') as words:x=words.write('')
    with open('files/comments_replied.txt','w') as comments :x=comments.write('')
    with open('files/env.txt','w') as env:write_in_file(env_dict,'files/env.txt',split='=',dic=True)
    return env_dict

def get_data():
    if os.path.isfile('files/env.txt'):
        env_settings,error_lines,errors=reddit_file.read_env('files/env.txt')
    else:
        env_settings={} 
        error_lines=[] 
        errors=True
    if len(env_settings.keys())!=12 or error_lines!=[] or errors or (not os.path.isfile('files/words.txt')) or (not  os.path.isfile('files/comments_replied.txt')):
            env_settings=reset_env()
    
    words,errors = reddit_file.read_words(env_settings['words_file_path'],env_settings['words_split_marks'])
    if words:
        env_settings['words']=words
    else:env_settings['words']={}
    env_settings['errors']=errors
    env_settings['env_path']='files/env.txt'
    return env_settings

def write_in_file(data,file_name,split='',lines=True,dic=False):
    if not dic:
        with open(file_name, "w") as f:
            if lines:
                for line in data:
                    f.write(line+ '\n')
            else:
                for line in data:
                    f.write(line+ split)
    else:
        with open(file_name, "w") as f:
            if lines:
                for line in data:
                    f.writelines(line + split + data[line]+'\n')
            else:
                for line in data:
                    f.write(line+ split + data[line])

def clean_words(words):
    words_clean=dict()
    for key in words.keys():
        if key[0] ==' ' and key[len(key)-1]==' ':
            words_clean[key[1:len(key)-1]]=words[key]
        else:
             words_clean[key]=words[key]
    return  words_clean
     
def popUpMessege(listMessage,color_text='black',timeout=5000):
    jobs_running_layout = [[sg.Text(str(message),text_color=color_text,background_color='white')] for message in listMessage ]
    jobs_running_window = sg.Window("Message", jobs_running_layout, disable_close=True,background_color='white' ,margins=(10,10))
    jobs_running_window.read(timeout=timeout)
    # jobs_running_window.hide()
    jobs_running_window.close()

def login_win():
    data=get_data()
    layout = [[sg.Text("Username:"),sg.Input(key='-User-')],
            [sg.Text(  "Password:"),sg.Input(key='-Pass-',password_char='*')],
            [sg.Text('',size = (30,1),key='-Failed-',text_color='Red')],
            [sg.Button('Login'),sg.Button('Exit') ] ]
    window = sg.Window('Login', layout)
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            quit()
            break
        elif values['-User-'] == data['username'] and values['-Pass-'] == data['password']:
            window.close()
            main_win()
            break
        else:
            window['-Failed-'].update('Wrong username or password!')

def main_win():
    data=get_data()
    layout2 = [
                [sg.Text('Edit env file:',size=(11,2),text_color='black'),sg.Button('env',size=(5,0))],
                [sg.Text('Edit words file:',size=(11,2),text_color='black'),sg.Button('words',size=(5,0))],
                [sg.Text('Edit quotes file:',size=(11,2),text_color='black'),sg.Button('quotes',size=(5,0))],
                [sg.Button('Logout',key='Logout',enable_events=True,pad=(0,10),size=(20,00))],
                [sg.Button('Comment',key='Comment',enable_events=True,pad=(0,10),size=(20,00))],
                [sg.Button('Reset',key='Reset',enable_events=True,pad=(0,10),size=(20,00))],
                ]
    window2 =sg.Window('Main',layout2,size=(250,300),margins=(35,15))
    while True:
        event2 , values2 = window2.read()
        if event2 == sg.WIN_CLOSED :
            quit()
            break
        elif event2== 'Logout' :
            window2.close()
            login_win()
            break
        elif event2== 'Reset' :
            reset_env()
            window2.close()
            login_win()
            break
        elif event2=='Comment':
            reddit_file.main(data)
            window2.close()
            break
        elif event2 == 'env':
            window2.close()
            edit_env_win()
            break
        elif event2 == 'words':
            window2.close()
            edit_word_win()
            break
        elif event2 == 'quotes':
            window2.close()
            edit_quote_win()
            break
    
def edit_env_win():
    data=get_data()
    layout3 = [ 
                [sg.Text('Enter subreddit type and number of subreddit and number of comments ',size = (50,1))],
                [sg.Text('subreddit:'),sg.Input(key='-subreddit-',enable_events=True,size=(22,0),pad=(80,10))],
                [sg.Text('number of subreddit:'),sg.Combo([i for i in range(1,11)],key='-limit_sub-',enable_events=True,size=(20,0),pad=(20,10),default_value='Choose number',readonly=True)],
                [sg.Text('number of comments :'),sg.Combo([i for i in range(1,11)],key='-limit_comment_sub-',enable_events=True,size=(20,0),pad=(10,10),default_value='Choose number',readonly=True)],
                [sg.Text('',size = (50,1),key='-result-',text_color='Red')],
                [sg.Button('edit'),sg.Button('Back')]
                ]
    edit_word=sg.Window('Edit env',layout3,margins=(10,10))
    while True:
        event3 , values3 = edit_word.read()
        if event3 == sg.WIN_CLOSED:
            quit()
        elif event3 == 'Back':
            edit_word.close()
            main_win()
            break
        elif event3 == 'edit':
            if  values3['-subreddit-'] == "" or values3['-limit_sub-'] == "choose number" or values3['-limit_comment_sub-'] == "choose number":
                edit_word['-result-'].update('Please fill the empty fields first!',text_color = 'Red')
            else:
                env_dict={'client_id':'r-vcoXEip5NdDA' ,'client_secret':'eKuY1Yd0IBhj5WjHnXiJ2LpopBXNwA',
                'username':'concepttask','password':'helloconcept','user_agent':'<console:conceptbot:0.0.1 (by /u/concepttask)>',
                'words_split_marks':':','words_file_path':'files/words.txt','subreddit':values3['-subreddit-'],'limit_sub':values3['-limit_sub-'],
                'limit_comment_sub':values3['-limit_comment_sub-'],'quotes_split_mark':'lines','comments_replied_path':'files/comments_replied.txt'
                }
                env_write=[key+'='+str(env_dict[key])+'\n' for key in env_dict]
                popUpMessege(['env edited successfully!'],color_text='green',timeout=3000)
                with open(data['env_path'],'w') as env:
                    env.writelines(env_write)
                edit_word.close()  
                edit_env_win()
                break          
    

def edit_word_win():
    data=get_data()
    keys=[key for key in data['words'].keys()]
    layout3 = [ 
                [sg.Text('Choose word for delete it or write new one if you want to add',size = (50,1))],
                [sg.Text('words in file:'),sg.Combo(keys,enable_events=True,key ='-combo-',size=(43,0),pad=(10,0),default_value='Choose word',readonly=True)],
                [sg.Text("New word   :"),sg.Input(key='-new-',pad=(10,0))],
                [sg.Text('',size = (50,1),key='-result-',text_color='Red')],
                [sg.Button('Add'),sg.Button('delete'),sg.Button('Back')]
                ]
    edit_word=sg.Window('Edit Words',layout3,margins=(10,10))
    while True:
        event3 , values3 = edit_word.read()
        if event3 == sg.WIN_CLOSED:
            quit()
            break
        elif event3 == 'Back':
            edit_word.close()
            main_win()
            break
        elif event3 == 'Add':
            if values3['-new-'] == "":
                edit_word['-result-'].update('Please fill the New word fields first!',text_color = 'Red')
                popUpMessege(['Please fill the New word fields first!'],color_text='red',timeout=3000)
            else:
                if ' '+values3['-new-']+' ' not in data['words']:
                    new_file='files/'+ values3['-new-'] +'.txt'
                    if not os.path.exists('files'):
                        os.mkdir('files')
                    data['words'][values3['-new-']] = new_file
                    write_in_file(clean_words(data['words']),data['words_file_path'],split=data['words_split_marks'],dic=True)
                    with open(new_file,'w') as doc:doc.write('')
                edit_word['-result-'].update('Word added successfully!',text_color = 'green')
                popUpMessege(['Word added successfully!'],color_text='green',timeout=3000)

                edit_word['-combo-'].update(value = 'Choose word')
                edit_word['-new-'].update(value = '')
                edit_word.close()
                edit_word_win()
                break

        elif event3 == 'delete':
            if values3['-combo-'] == "Choose word":
                edit_word['-result-'].update('Please choose word first!',text_color = 'Red')
            elif values3['-combo-'] != "Choose word" and (values3['-combo-']in data['words']) :
                if os.path.isfile(values3['-combo-']):
                    os.remove(values3['-combo-'])
                data['words'].pop(values3['-combo-'])
                write_in_file(clean_words(data['words']),data['words_file_path'],split=data['words_split_marks'],dic=True)
                popUpMessege('Word added successfully!',color_text='green',timeout=2000)
                edit_word.close()
                edit_word_win() 
                break           

def edit_quote_win():
    data=get_data()
    keys=[key for key in data['words'].keys()]
    layout3 = [ 
                [sg.Text('Choose word and write quote for delete it or add a new one',size = (50,1))],
                [sg.Text('Type:'),sg.Combo(keys,enable_events=True,key ='-combo-',size=(20,1),pad=(10,10),default_value='Choose word',readonly=True)],
                [sg.Text("Quote:"),sg.Input(key='-Quote-')],
                [sg.Text('',size = (50,1),key='-result-',text_color='Red')],
                [sg.Button('Add'),sg.Button('delete'),sg.Button('Back')]
                ]
    edit_quote =sg.Window('Edit Quote',layout3,margins=(10,10))
    while True:
        event3 , values3 = edit_quote.read()
        if event3 == sg.WIN_CLOSED:
            quit()
            break
        elif event3 == 'Back':
            edit_quote.close()
            main_win()
            break
        elif event3 == 'Add':
            if values3['-Quote-'] == "" or values3['-combo-'] == "Choose word":
                edit_quote['-result-'].update('Please fill the empty fields!',text_color = 'Red')
            else:
                quotes=reddit_file.set_quotes(data['words'][values3['-combo-']],split_mark='lines',gui=True)
                if values3['-Quote-'] not in quotes :
                    quotes.append(values3['-Quote-'])
                    write_in_file(quotes , data['words'][values3['-combo-']])
                edit_quote['-combo-'].update(value = "Choose word")
                edit_quote['-Quote-'].update(value = '')
                edit_quote['-result-'].update('Quote added successfully!',text_color = 'Green')

        elif event3 == 'delete':
            if values3['-Quote-'] == "" or values3['-combo-'] == "Choose word":
                edit_quote['-result-'].update('Please fill the empty fields!',text_color = 'Red')
            else:
                quotes=reddit_file.set_quotes(data['words'][values3['-combo-']],split_mark='lines',gui=True)
                if values3['-Quote-'] in quotes:
                    quotes.remove(values3['-Quote-'])
                    write_in_file(quotes,data['words'][values3['-combo-']])
                    edit_quote['-combo-'].update(value = 'Choose word')
                    edit_quote['-Quote-'].update(value = '')
                    edit_quote['-result-'].update('Quote added successfully!',text_color = 'Green')
                else:
                    edit_quote['-result-'].update('Quote not found quote!',text_color = 'red')

def run():
    # login_win()
    main_win()
if __name__ == "__main__":
    run()


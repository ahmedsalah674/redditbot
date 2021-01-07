import praw
import re
import os
import random
from prawcore import NotFound
import time
import PySimpleGUI as sg
import GUI as GUi_file

def sub_exists(sub,reddit):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists

def set_quotes(file_path,split_mark='lines',gui=False):
    quotes=list()
    if os.path.isfile(file_path) :
        with open(file_path,'r',encoding='utf-8') as doc:
            if split_mark == 'lines':
                quotes=doc.readlines()
                quotes=[re.sub('\n','',quote) for quote in quotes]
            else:
                quotes=doc.read()
                if split_mark in quotes:
                    quotes=quotes.split(split_mark)
                    quotes=[re.sub('\n','',quote) for quote in quotes]
    
    if gui==False and not quotes: 
        quotes.append(os.path.basename(file_path))
    return quotes

def read_words(words_file_path,split_mark=';'):
    if os.path.isfile(words_file_path):
        with open(words_file_path,'r',encoding='utf-8') as doc:
            lines=doc.readlines()
            if lines :
                words_dict=dict()
                error_lines=list()
                for words in lines:
                    if split_mark in words:
                        temp=[]
                        index= words.index(split_mark)
                        if index != 0 and len(words)>index:
                            temp.append(' ' + words[:index] + ' ')
                            temp.append(re.sub('\n','',words[index+1:]))
                            words_dict[temp[0]]= temp[1]
                        else: 
                            error_lines.append((lines.index(words) + 1))
                    else:
                        error_lines.append((lines.index(words) +1))
                return words_dict,error_lines
            else: 
                return False ,False
    else: 
        return False ,False
    
def read_comments_replied(file_name):
    if not os.path.isfile(file_name):
        comments_replied_to = []
    else:
        with open(file_name, "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))
    return comments_replied_to

def add_comments_replied(comments_replied , file_name):
    with open(file_name, "w") as f:
        for post_id in comments_replied:
            f.write(post_id + "\n")

def reply_subreddit(subreddit,words_dict,comments_replied,comments_replied_path,limit_sub=1,limit_comment_sub=1,quotes_split_mark=''):
    not_found = 1
    for submission in subreddit.hot(limit=limit_sub):
        breaked=0
        for comment in submission.comments:
            sleep=0
            if breaked < limit_comment_sub and (comment.id not in comments_replied)  and hasattr(comment,"body"):
                for word in words_dict :  
                    quotes=set_quotes(words_dict[word],split_mark=quotes_split_mark)  
                    if re.search(word, comment.body, re.IGNORECASE):
                        index = random.randint(0,len(quotes)-1)
                        try:
                            comment.reply(quotes[index])
                            GUi_file.popUpMessege([str("Bot replying to : " + submission.title)],color_text='green',timeout=5000)
                            comments_replied.append(comment.id)
                            add_comments_replied(comments_replied,comments_replied_path) 
                            not_found=0
                            breaked += 1
                            sleep=1
                            break
                        except Exception as ex:
                            print(ex) 
                if sleep == 1:  
                    GUi_file.popUpMessege(['wait 10s for next comment'],color_text='green',timeout=10000)
                    time.sleep(10)
            if breaked == limit_comment_sub :
                break
    return not_found

def read_env(file_path):
    keys=['client_id','client_secret','username','password','user_agent','words_file_path','words_split_marks','subreddit','limit_sub','limit_comment_sub','quotes_split_mark','comments_replied_path']
    temp=[]
    error_lines=[]
    if os.path.isfile(file_path):
        with open(file_path,'r',encoding='utf-8')as test:
            test_lines= test.read()
            test_lines=re.sub(' ', '',test_lines)
            test_lines=test_lines.split('\n')
            env_dict=dict()
            for line in test_lines:
                    split_line=line.split('=')
                    if (len(split_line) !=2) or (line.index('=')==0) or (line.index('=')==len(line)-1):
                        error_lines.append(test_lines.index(line)+ 1)
                    else:
                        env_dict[split_line[0].lower()]=split_line[1]
        if error_lines :
            return {},error_lines,False
        else:
            found=0
            error=0
            for key in env_dict:
                if(key in temp) or key not in keys:
                    error=1 
                elif(key in keys):
                    found +=1
                    temp.append(key)
            if env_dict['limit_sub'].isnumeric() ==False or env_dict['limit_comment_sub'].isnumeric()==False:
                error=1
            if found == len(env_dict) and not bool(error):
                return env_dict,[],False
            else:  
                return {},[],bool(error)
    else:return{},[],0

def main(env_settings):
    reddit = praw.Reddit(client_id = env_settings['client_id'], client_secret = env_settings['client_secret'],
    user_agent = env_settings['user_agent'],username=env_settings['username'],password=env_settings['password'])
    comments_replied = read_comments_replied(env_settings['comments_replied_path'])
    if sub_exists(env_settings['subreddit'],reddit):
        subreddit = reddit.subreddit(env_settings['subreddit'])
        not_found=reply_subreddit(subreddit=subreddit,words_dict=env_settings['words'],comments_replied=comments_replied,comments_replied_path=env_settings['comments_replied_path'],limit_comment_sub=int(env_settings['limit_comment_sub']),limit_sub=int(env_settings['limit_sub']),quotes_split_mark=env_settings['quotes_split_mark'])
        if not_found :
            GUi_file.popUpMessege(['the robot cant find the words in the limit of subreddit and comments'],color_text='red',timeout=5000)
            
    else: 
        GUi_file.popUpMessege(['the subreddit is not found'],color_text='red',timeout=5000)
    
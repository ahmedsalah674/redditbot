import praw
import re
import os
import random
from prawcore import NotFound
# from prawcore.exceptions import Forbidden
import time



def sub_exists(sub,reddit):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists


# def set_reddit_data(client_id,client_secret,username,password,user_agent):
#     reddit = praw.Reddit(client_id = client_id, client_secret = client_secret,
#                      user_agent = user_agent,username=username,password=password)
#     return reddit



def set_quotes(file_path,split_mark='lines'):
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
    
    if not quotes: 
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
    # sub=0
    for submission in subreddit.hot(limit=limit_sub):
        breaked=0
        # sub +=1
        for comment in submission.comments:
            sleep=0
            if breaked < limit_comment_sub and (comment.id not in comments_replied)  and hasattr(comment,"body"):
                for word in words_dict :  
                    quotes=set_quotes(words_dict[word],split_mark=quotes_split_mark)  
                    if re.search(word, comment.body, re.IGNORECASE):
                        index = random.randint(0,len(quotes)-1)
                        # print('the subreddit title is ',submission.id,'the lenth of comments subreddit is ', len(submission.comments))
                        try:
                            comment.reply(quotes[index])
                            print("Bot replying to : ", submission.title)
                            comments_replied.append(comment.id)
                            add_comments_replied(comments_replied,comments_replied_path) 
                            not_found=0
                            # print('the comment id is ',comment.id,'and the word is' ,word,'\n')
                            # print('the relpy is ',quotes[index],'\n')
                            breaked += 1
                            sleep=1
                            break
                        except Exception as ex:
                            print(ex) 
                    # else :
                    #     print('not found this word',word,'in comment ',comment.id ,'in the subreddit', sub )
                if sleep == 1:  
                    print('\nwait 10 seconds for search about next comment')                          
                    time.sleep(10)
            if breaked == limit_comment_sub :
                # print('breaked -> ',breaked)
                break
    return not_found


def read_env(file_path):
    keys=['client_id','client_secret','username','password','user_agent','words_file_path','words_split_marks','subreddit','limit_sub','limit_comment_sub','quotes_split_mark','comments_replied_path']
    temp=[]
    error_lines=[]
    if os.path.isfile(file_path):
        with open(file_path,'r',encoding='utf-8')as test:
            # print (test.readlines())
            test_lines= test.read()
            # test_lines=[re.sub('\n', '',line) for line in test_lines if line!='']
            test_lines=re.sub(' ', '',test_lines)# for line in test_lines if line!='' or line!=' ']
            test_lines=test_lines.split('\n')
            # for line in test_lines:
            env_dict=dict()
            for line in test_lines:
                if line!='' :# print(line)
                    split_line=line.split('=')
                    if (len(split_line) !=2) or (line.index('=')==0) or (line.index('=')==len(line)-1):
                        error_lines.append(test_lines.index(line)+ 1)
                        print('error line',line,test_lines.index(line)+ 1)
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
                # print('wroooooong')
            if found == len(env_dict) and not bool(error):
                return env_dict,[],False
            else:  
                return {},[],bool(error)
    else:return{},[],0


def main():
    env_settings,error_lines,errors=read_env(r'files/env.txt')
    if error_lines==[] and errors==False and env_settings=={}:
        print('env file not found')
    elif error_lines==[] and errors==False and env_settings!={}:
        client_id =env_settings['client_id'] 
        client_secret = env_settings['client_secret'] 
        username =  env_settings['username']
        password = env_settings['password'] 
        user_agent = env_settings['user_agent'] 

        words_file_path=env_settings['words_file_path']
        words_split_marks=env_settings['words_split_marks']

        subreddit = env_settings['subreddit']
        limit_sub=int(env_settings['limit_sub'])
        limit_comment_sub=int(env_settings['limit_comment_sub'])
        quotes_split_mark=env_settings['quotes_split_mark']
        comments_replied_path=env_settings['comments_replied_path'] 
        
        reddit = praw.Reddit(client_id = client_id, client_secret = client_secret,user_agent = user_agent,username=username,password=password)
        comments_replied = read_comments_replied(comments_replied_path)
        words_dict,error_lines_words=read_words(words_file_path,split_mark=words_split_marks)


        if sub_exists(subreddit,reddit):
            subreddit = reddit.subreddit(subreddit)
            if error_lines_words==False and words_dict == False:
                print('the file of words not found or didn\'t have any data') 
            elif len(error_lines_words) == 0 and len(words_dict) > 0:
                not_found=reply_subreddit(subreddit=subreddit,words_dict=words_dict,comments_replied=comments_replied,comments_replied_path=comments_replied_path,limit_comment_sub=limit_comment_sub,limit_sub=limit_sub,quotes_split_mark=quotes_split_mark)
                if not_found :
                    print('the robot can\'t found the words in the limt of subreddit')
            elif  len(error_lines) and len(words_dict)  > 0 :        
                    not_found=reply_subreddit(subreddit=subreddit,words_dict=words_dict,comments_replied=comments_replied,comments_replied_path=comments_replied_path,limit_comment_sub=limit_comment_sub,limit_sub=limit_sub,quotes_split_mark=quotes_split_mark)
                    if not_found :
                        print('the robot cant found the words in the limt of subreddit')
                    print('there are errors in words file in lines :', error_lines)
            elif len(error_lines) and len(words_dict)  == 0 :
                    print('the words split mark is wrong')
            
        else: 
            print('the subreddit is not found')

    elif error_lines!=[]:
        print('env file have invalid syntax in lines :',error_lines)
    elif errors:
        print ('the env file have wrong key or (less,more) than the model want')
    return 0
if __name__ == "__main__":
    print('the return of main',main())


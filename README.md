<!-- <p align="center"><img src="https://res.cloudinary.com/dtfbvvkyp/image/upload/v1566331377/laravel-logolockup-cmyk-red.svg" width="400"></p> -->

<p align="center">
<h1>redditbot</h1>
</p>


## About project

- This project is a bot reply about number in number of subreddit you determine the numbers finaly the the comment replies -> number_subreddit * number_comment_subreddit .

## install Project

Foleder install have shell file for install libraries project need it and clone this repo .
libraries is.
-praw
-regex
-times
-prawcore
If you have libraries before just clone project.

## env file
This file have all settings of code that you can update it .
the rules of env file is :
-keys must be 12 and all of them have value after '=' mark and the same names .
-client_id -> clint_id of reddit .
-client_secret -> client_secret of reddit.
-username -> username for login.
-password -> password for login.
-user_agent -> uniqe value for reddit.
-words_file_path -> words_file path like 'files/words.txt'.
-words_split_marks -> split mark in words file default ';' you can eddit it .
-subreddit ->caticgory that you search about it.
-limit_sub -> how many subreddit you want to search in comments.
-limit_comment_sub -> how many comment you want to reply on it in the one of subreddit  .
-quotes_split_mark -> how to split quotes in quotes file the default is new line and value = 'lines'  .
-comments_replied_path ->path of file that have ids of comments that the bot was replied on it .

 ## words file
words file have many of words and the path of file that have many quotes as replies if the the bot found the word in the comment body and you can edit split mark for it put must be evey word with path in line .
for example:
word1;path_word1
word2;path_word2

# how to login 
the env file have the default 

# purpose: Make a reddit bot in python that responds to a user's call w/ a simple message
#          learn how to interact with reddit api
#          take what I learn and make a serverless nodejs reddit bot
#          learn more about nodejs
# basics learned from John G Fisher's youtube video
# /u/jfishersolutions | "how to create a reddit bot with python"
#https://pythondata.com/quick-tip-sqlalchemy-for-mysql-and-pandas/
#https://www.pythonanywhere.com

# wrapper for reddit api
import praw

#store prior comments to prevent posting multiple times on same comment
import pandas as pd
import numpy as np
import sqlalchemy as sql

# debugging text
from inspect import getframeinfo, stack
#==================================================================================


#purpose: debugging function
#input: message to print
#output: prints to terminal last line with message
#return: none
def debuginfo(message):
    caller = getframeinfo(stack()[1][0])
    print(caller.filename + ":" + str(caller.lineno) + message)
    return

#purpose: sets up connection to mysql db using sqlalchemy and pandas lib's
#input: none
#output: none
#return: pandas dataframe
def queryDB():
    # used to store data via file on system instead of db    
    # commentIdsSet = set()
    # with open("set.txt", 'r') as f:
    #     for line in f:
    #         for id in line.split():
    #             commentIdsSet.add(id)
    # commentIdsList =[]
    
    #setup database w/ user /pwd and db host address
    
    # connection_string = 'mysql+mysqlconnector://evanmrrobot:PkTyq8c4q7e5M23L@'\
    #                     'evanmrrobot.mysql.pythonanywhere-services.com'\
    #                     '/evanmrrobot$test'
    #mysql:/user:passwd@127.0.0.1:3307/dbname
    #37.59.55.185 is ip address of domain remotemysql.com
    connection_string = 'mysql+mysqlconnector://PxyXvBHFfG:Hep9ZdVdEv@remotemysql.com:3306/PxyXvBHFfG'
    sql_engine = sql.create_engine(connection_string, echo = True)
    
    #check to see if db has table created already
    if not sql_engine.dialect.has_table(sql_engine, "comment_ids"):
        metadata = sql.MetaData(sql_engine)
        #create table
        comment_ids_table = sql.Table(
            'comment_ids', metadata,
            sql.Column('comment_id', sql.String(16), nullable=False),)
        #implement table
        metadata.create_all()
    
    #just query if already made or if just made from prior if condition
    query =query = "select comment_id "\
            "FROM comment_ids "
    #store table info in pandas data frame
    df = pd.read_sql_query(query, sql_engine)

    print("row names:", df.index.values)
    print("column names:", df.columns.values)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(df)
    return df    

def insertDB(df):
    try:
        connection_string = 'mysql+mysqlconnector://PxyXvBHFfG:Hep9ZdVdEv@remotemysql.com:3306/PxyXvBHFfG'
        sql_engine = sql.create_engine(connection_string, echo = True)
        print("81row names:", df.index.values)
        print("82column names:", df.columns.values)
        df.to_sql("comment_ids", sql_engine, if_exists = 'append', index = False, chunksize = 100)#chunksize not necessary?

        print("db updated")
    except:
        print("POST to database ERROR")
    return


def replyComment():
    reply = str("I made a bot."+"\n")
    with open("reply.txt", 'r') as f:
        for line in f:
            reply = reply + line
    return reply


def main():
    debuginfo("last line")
    
    #reddit api access
    reddit =praw.Reddit(client_id = 'xBNqMOTulaVWdw',
                        client_secret = 'jx8k4vyygNs-jdFftbveNHWI4lA',
                        username = 'evanMrRoBot',
                        password = 'PkTyq8c4q7e5M23L',
                        user_agent = 'mrrobotApp 1.5')
  
    #subreddit to interact with
  
    sub = reddit.subreddit('testingground4bots')#subreddit sandbox for testing
    #phrase a user uses to call the bot
    phrase = '!evanMrRoBot Hello friend'
    
    debuginfo("last line")

    #sets up connection to mysql db using sqlalchemy and pandas lib's
    df = queryDB()

    commentIdsList = []
    numpyArray = df.to_numpy()
    print("numpArray:",numpyArray)
    reply = replyComment()
    
    for comment in sub.stream.comments():
        print("comment.id :",comment.id, "\n")
        #print("comment.body:",comment.body, "\n")
        if phrase in comment.body:
            print("phrase:",phrase, "\n")
            word = comment.body.replace(phrase, '')
            print("word:",word, "\n")
            try:
                print('comment.author:', comment.author)  
                # print('before commenIdsSet:', commentIdsSet)          
                # if comment.id in commentIdsSet:
                #     continue
                if comment.id in numpyArray:
                    continue
                #commentIdsSet.add(comment.id)
                numpyArray = np.append(numpyArray, comment.id)
                print("numpyArray:", numpyArray)
                commentIdsList.append(comment.id)
                # reply = "hey this is the official reply"
                # print("reply:", reply)
                comment.reply(reply)#word + ': ' + reply)
                print("bot responded and posted message")
                #print('after commenIdsSet:', commentIdsSet)                    
            except:
                print("comment post ERROR")
        
        #update db        
        if len(commentIdsList) == 1:
            #f = open("set.txt","a+")    
            #f.write(commentIdsList[0]+" ")
            #f.close()
            dfValue = pd.DataFrame([commentIdsList[0]], columns=['comment_id'])
            print("148row names:", dfValue.index.values)
            print("149column names:", dfValue.columns.values)            
            df = df.append(dfValue)          
            
            print("df after update:\n")
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
                print(df)            
            insertDB(df)
            df = pd.DataFrame() #empty                 
            del commentIdsList[0]
    debuginfo("last line")
    return

if __name__ == '__main__':
    main()
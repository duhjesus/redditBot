###### Note: 
        1. one last vulnerability of python dependency, *pycrypto*, left. no remedy yet, will look into it. 
           don't believe to be using it.
        2. all accounts have been deleted and passwords are throwaways.
        
## purpose: 
         * Make a reddit bot in python that responds to a user's call w/ a simple message
         * interact with reddit api, pandas/numpy data library refresher
         * store reddit comment/posts in a mysql server to avoid duplicate actions(spamming of bot)
         * a simple file storage would've been easier, but does not scale.

###### basics learned from:
1. John G Fisher's youtube video: /u/jfishersolutions | "how to create a reddit bot with python"
used as a starting point to learn more about reddit.
2. [mysql research](https://pythondata.com/quick-tip-sqlalchemy-for-mysql-and-pandas/)
used to learn to interact w/ sql server and store large amounts of data(overkill, but interesting)
3. [mysql server](https://remotemysql.com/) host used to host a sql server and interact w/ it via python
4. [server](https://www.pythonanywhere.com) not used, restrictions on outgoing calls

future project: take what I learn and make a serverless nodejs reddit bot

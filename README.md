# Dirk´s Passwordgenerator

As I am using hasicorp vault and KeePass i required something to create an password with my TouchPortal.  
This little tool creates passwords and put them into you KeePass File and even in you vault KeyValue store.  

vault must be manually configured, if not required you can turn off the vault support.


## How to start 
```
python3 passwordgen.py
```


## support functions:

>Password Generator (c) 2021 by Dirk Derichsweiler  
>usage: passwordgen <parameters  
>  
>parameter:  
>  
>--create  generates an random password  
>--title <value>   tile for Keepass entry  
>--username <value> username for Keepass entry  
>--count  amount of characters  
>--hide   hide password  
>--temp   do not write to keepassfile  
>  
>--getuser <searchstring>   get username  
>--getpassword <search string>  get password  

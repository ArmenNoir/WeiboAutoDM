# WeiboAutoDM ver0.2

> This program focuses on automatically sending DMs on Sina Weibo’s webpage at certain time to certain user.



## Requirements

- python3
- selenium
- pause



## Instructions

First to run **weibo_cookie.py**, this will open webdriver of Chrome to fetch cookies. You can login in within 60s of the default code setting. The output is below:

```
cookies saved!
```

~~If you have a valid cookie, just modify `dm.json`. Then, set all the arguments in `dm.json`~~

Now only need to modify **config** in code. Still work but *.json* file can’t be read as *utf-8* so temporarily stop using it. 

```
{
    "uid": "1934183965",
    "msg": "hello, type here but no ENTER",
    "clock": "2023-02-11 16~00",
    "cookie_path": ""
}
```

Finally, **run sendingDM.py**.

If you have set the hour and minute, program will run at set time.

```
Finished
```

However, if you just set date, it is for first run test, the program will automatically send messages after 10 seconds once the messages arrive at text area of the DM webpage.

```
logger.warn('You have not set the time!\nProgram will run after 10s for test')
You have not set the time!
Program will run after 10s for test
Finished
```



## Arguments

All arguments are set in ~~dm.json~~ config in the code. ~~in the same folder with WeiboAutoDM.~~

```
{
    "uid": "1934183965",
    "msg": "hello, type here but no ENTER",
    "clock": "2023-02-11 16~00",
    "cookie_path": ""
}
```

### uid

The UID of specific user, only one for a program. Generally you could use oid, but I have never tried on that.
Default UID 1934183965 is the admin of Weibo, anyone could send messages to this user for test.

### msg

Any string but no `\n`

### clock

format as

`YYYY-MM-DD HH~mm`

or

`YYYY-MM-DD`

`YYYY-MM-DD HH~mm` this format will let program run at the set time to automatically send messages, consider better to use when you debug this program is OK on your PC.

`YYYY-MM-DD` this format is used only for debug. Automatically sending messages 10 seconds after web driver arrives at DM page.

### cookie_path

The directory of your saved cookie for https://weibo.com/login.php

Default as “”, means cookie is in the same folder with the .py



## WARNING

1. Users should **NOT** run this program less than **1 minute** before the set time.
2. If you get cookie by scan QR code, in this way cookie could only last a few hours(at least 4 hours by my test). If you want to keep cookie valid longer(at least 1 day by my test), it is better to use **SMS verification code** to login in then fetch cookie.



## Further

1. For now, text area in Weibo only support inputs messages without `ENTER`, but it could be done with `CTRL+ENTER` to input texts with `ENTER`
2. This program **only support 1 receiver at 1 set time**. If you want to send to multiple user at the same time, it is better to run in multiple terminal to make sure the timeliness.
3. About timeliness. After multiple tests on program, for now without the interruption of bad network, the delay is less than **0.02** second. Will continue to improve and concentrate more on this feature.
4. The origin of this program is to send to someone at certain minute, so the second is ignored. Also, Weibo doesn’t show the second of sent messages, so initially all set time will be changed to `%H%M:00` to make sure the timeliness.
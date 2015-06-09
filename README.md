# AWS Reserved Instance Details #
**This django app can help us to get aws Reserved Instance details by aws Boto API. Also it can shows the Ri(short for Reserved Instance) using situation: How many Ri you have, and how many Ri you have occupied with every type. It can help you to save money.**

**It shows like below:**
![](http://i.imgur.com/2fYwUpU.jpg)

- This django app support muti aws account. You can use individual column searching to filter data.
ri\_num is the number of Ri your have bought.The used\_num is the server quantity of current using from our asset table.

- You can update the Ri data by clicking the button on the top. It shows like below:
![](http://i.imgur.com/RUufAXt.jpg)

## Environment:
**django 1.6.6**

**jquery-1.8.3.min.js**

**boto (AWS python api environment,update to the lastest version)**

**DataTables-1.10.7**

**bootstrap-2.3.2**

## Other:
- This is a django app, please add the related configure to your project main settings.py and urls.py.

- http://yourdomain/ri/showtable is for the page ShowTable. If you have muti aws accounts,please change the button code of template show_table.html "href="http://yourdomain/tables/ri/accounts=a1-a2-a3/". To split the muti accounts with '-'  
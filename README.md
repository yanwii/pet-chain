### 百度莱茨狗购买脚本

之前版本程序有点问题，现已修复，可以抢单，请注意设置金额。

>

### 领养
一共可以领养四只狗  
[第一只](https://pet-chain.baidu.com/chain/splash)  
[第二只](https://pet-chain.baidu.com/chain/splash?appId=2&tpl=wallet)  
[第三只](https://pet-chain.baidu.com/chain/splash?appId=3&tpl=wallet)  
[第四只](https://pet-chain.baidu.com/chain/splash?appId=4&tpl=wallet)  

>

### 说明

使用前请安装threadpool

    pip2 install threadpool

如果想使用*selenium*自动登录，需要安装

    pip2 install -U selenium

1.编辑config.ini  
    
    [Pet-Chain]
    interval    程序间隔
    common      普通品质价格
    rare        稀有品质价格
    excellence  卓越品质价格
    epic        史诗品质价格
    mythical    神话品质价格
    webdriver   firefox/chrome

    [Login]
    username    百度用户名
    password    百度密码  

2.如果不使用selenium，则需要保存headers  
打开[莱茨狗市场页面](https://pet-chain.baidu.com/chain/dogMarket?t=1517819157016)，登录  
打开浏览器调试模式，点击价格排序，并将*queryPetsOnSale*请求的headers复制到*data/headers.txt*中  



只有实时价格小于设置的价格，才会尝试购买  

>

### 用法

    # 直接运行
    python2 pet_chain.py run
    
    # 使用selenium登录并运行
    python2 pet_chain.py login


>

### 最后

欢迎加微信一起讨论  

![](./wechat/webwxgetmsgimg.png)
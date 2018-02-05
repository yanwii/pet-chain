百度莱茨狗购买脚本

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

### 用法

    # 直接运行
    python2 pet_chain.py run
    
    # 使用selenium登录并运行
    python2 pet_chain.py login
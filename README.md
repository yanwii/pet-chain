百度莱茨狗购买脚本

### 说明

使用前请安装threadpool

    pip2 install threadpool


打开[莱茨狗市场页面](https://pet-chain.baidu.com/chain/dogMarket?t=1517819157016)，登录  
打开浏览器调试模式，点击价格排序，并将*queryPetsOnSale*请求的headers复制到*data/headers.txt*中  

编辑config.ini  

    interval    程序间隔
    common      普通品质价格
    rare        稀有品质价格
    excellence  卓越品质价格
    epic        史诗品质价格
    mythical    神话品质价格

只有实时价格小于设置的价格，才会尝试购买  

### 用法

    python2 pet_chain.py


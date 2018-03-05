### 百度莱茨狗购买脚本

支持属性选择，初始金额，初始等级，稀有数


>

### web版本效果

![](wechat/byzanz-demo.gif)


>

### 配置
配置根目录下config.json

    num_of_rare_attr    稀有属性个数
    max_num_of_pages    最大页数
    body                体型
    eyes                眼睛
    mouth               嘴巴
    pattern             花纹
    color_of_body       体型颜色
    color_of_eyes       眼睛颜色
    color_of_pattern    花纹颜色
    color_of_belly      肚皮颜色
    sort_by             按照rare/price排序
    initial_degree      初始等级
    initial_amount      初始金额

>

### 说明

使用前请安装pillow,flask
    
    pip2 install flask
    pip2 install pillow


>

### 用法

    # 直接运行
    python2 pet_chain.py run
    
    # 网页版 
    python2 web.py
    在浏览器中打开： http://127.0.0.1:5000/ 
>
### 最后

欢迎加入微信群、QQ群一起讨论  
![](./wechat/1321922313.jpg)

![](./wechat/webwxgetmsgimg.png)
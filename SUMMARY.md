# 接口文档

* [Introduction](README.md)
* response自动按照前端的request.head中的accept字段设置的格式进行渲染，若无设置则默认为json
* 超级管理员 https://chuiyan.fivyex.com/admin
* 主机已启动SSL协议，可以靠https访问；已设置后台运行，可以全天候访问

#### 修改记录

<font color=#FF0000 >优惠券查询、订单查询、菜品查询：请求从POST改为GET，需要的request.body改为request.params
<br>修改各应用的返回参数
<br>增加各应用对应的URL
<br>查询订单处的create_time在debug时使用的是仅有日期的格式，实际已改为日期+时间的格式
<br>以下部分使用localhost+POSTMAN的配置debug完毕
<br>添加--商品推荐部分，待完成--数据库：商品分类；后端：评论系统</font>

[TOC]

## 1.登录

### 具体请求

>请求方式 POST<br>
> URL: https://chuiyan.fivyex.com/user/login
###Request.body
```
{ 
    'code':
}
```
### Response.body

```
{
    'userID': 1,
    'userOPENID':'xxxxxxxx',
    'token': 'xxxxxxxx'
}
```
#### ERRORS

```
客户端错误
{'error': '没有收到code'},status=400
```
```
服务器错误
{'error': 'code为空'},status=500
{'error': '该用户已存在但未激活'},status=500
{'error': '登录失败'},status=500  登录的用户在数据库已存在，但更新token失败
{'error': '登录异常错误'},status=500
```
#### 返回参数

|参数|类型|说明|
|:----- |:-----|----- |
|userID |int |数据库内id（openid和token作为备选/string）|
|userOPENID |string |微信下发用户唯一标识|
|token|string|服务器生成的uuid

## 2.优惠券查询

### 具体请求

>请求方式 GET<br>
> URL：https://chuiyan.fivyex.com/user/couponfind?userID=参数&status=参数
###request.params
```
url中所需要的参数如下
    'userID':1,
    'status':1
```
### response.body

```
[
    {
        "status": "未使用",
        "detail": {
            "coupon_name": "保罗券",
            "coupon_price": 5.0,
            "coupon_invalid_time": "2021-06-30",
            "coupon_sub": "老板的券"
        }
    },
    {
        "status": "未使用",
        "detail": {
            "coupon_name": "司马券",
            "coupon_price": 3.0,
            "coupon_invalid_time": "2021-06-24",
            "coupon_sub": "wwxsm"
        }
    }
]
```
#### 请求参数

|参数|类型|说明|
|:----- |:-----|----- |
|userID |int |登录时返回的userID（openid和token作为备选）|
|status |int |查询的优惠券状态，前端默认传递 1，即有效优惠券。查询已使用则 2，查询未使用已过期则 3|

#### 返回参数

|参数|类型|说明|
|:----- |:-----|----- |
|status |string |返回优惠券的状态|
|detail |字典 |优惠券的金额和时间|
|coupon_name|string|优惠券名字|
|coupon_price|float|优惠券金额|
|coupon_invalid_time|string|优惠券失效时间|
|coupon_sub|string|优惠券描述|
#### ERRORS

```
客户端错误
{'error': '优惠券状态参数错误'},status=400
{'error': '传递userID为空'},status=400
```
```
服务器错误
{'error': '服务器查找优惠券错误'},status=500
{'error':'无法转换为int类型'},status=500
```
## 3.下单

### 具体请求

>请求方式 POST<br>
> URL: https://chuiyan.fivyex.com/good/ordering
###request.body
```
{
            "userID":7,
            "machineID":"1",
            "goods":[
            {
                "goodID":"2",
                "goodAmount":7,
                "salty":1,
                "spicy":4
            },
            {
            "goodID":"1",
            "goodAmount":2,
            "salty":4,
            "spicy":1
            }],
            "totalprice":65,
            "note":"加辣",
            "couponID":0
}
```
### response.body

```
{
    "success": "保存订单成功",
    "order_uid": "chuiyan8ef89db6-d1c4-11eb-a411-802bf98d5ef62021-06-20 20:39:30735124"
}
```
#### 请求参数

|参数|类型|说明|
|:----- |:-----|----- |
|userID |string |登录时返回的userID（若debug出错，openid和token备选）|
|machineID |string |用户下单选择的售货机ID|
|goods|array|元素为字典的数组|
|goodID|string|查询菜品获得的ID|
|goodAmount|int|下单数量|
|totalprice|float|总金额|
|note|string|订单备注|
|couponID|int|查询优惠券获得的id,如果该订单使用了优惠券则传id,<font color=#FF0000 >如果没有则传0</font>|
#### ERRORS

```
客户端错误
{'error':'下单数量大于库存'},status=400
```
```
服务器错误
{'error':'下单出错'},status=500
{'error':'查找不到对应ID的菜品'},status=500
{'error':'查找不到对应ID的菜品'},status=500
{'error':'查询对应菜品的属性失败'},status=500
{'error':'录入订单的菜品失败'},status=500
```
## 4.查询订单-订单号

### 具体请求

>请求方式 GET<br>
> URL: https://chuiyan.fivyex.com/good/orderfind?order_uid=参数
###request.params
```
'order_uid':"chuiyan636d7c65-d1cb-11eb-82e0-802bf98d5ef62021-06-20 21:28:24158751"
```
### response.body

```
{
    "order_pickup_machine_address": "广东省广州市黄埔区开创大道与香雪五路交叉路口东南侧",
    "create_time": "2021-06-20",
    "qr_path": "D:\\Academic\\design\\mysite\\media/2021-06-20 212824158751.jpg",
    "order_note": "加辣",
    "ordergood_ser": [
        {
            "ingredientsURL": "/static/image/goods/2.jpg",
            "ingredientsNAME": "红烧肉",
            "Amount": 7
        },
        {
            "ingredientsURL": "/static/image/packs/1.jpg",
            "ingredientsNAME": "猪肉炖粉条",
            "Amount": 2
        }
    ]
}
```
#### 返回参数

|参数|类型|说明|
|:----- |:-----|----- |
|order_pickup_machine_address|string|售货机地址|
|create_time|string|订单在数据库的创建时间|
|qr_path|string|二维码url|
|order_note|string|订单备注|
|ordergood_ser|array|该订单包含的菜品及调料包信息|
|ingredientsURL|string|调料包图片url|
|ingredientsNAME|string|调料包名字|
|Amount|int|调料包数量|
####ERRORS
```
{'error':'查询数据库中的订单出错'},status=500
```
## 5.查询商品-全部

### 具体请求

>请求方式 GET<br>
> URL: https://chuiyan.fivyex.com/good/goodfind
###response.body
```
[
    {
        "goodser": {
            "goodsID": "1",
            "goodAmount": "猪肉炖粉条",
            "goodDescription": "东北名菜 吃完好满足！",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/1.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 12.5,
        "type1": "其他",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "2",
            "goodAmount": "红烧肉",
            "goodDescription": "满满的汤汁",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/2.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 10.5,
        "type1": "其他",
        "type2": "平底锅"
    }
]
```
#### 返回参数

|参数|类型|说明|
|:----- |:-----|----- |
|goodsID |string |菜品id|
|goodAmount|int|菜品库存|
|goodDescription|string|菜品描述|
|goodImgURL|string|菜品图片url|
|goodStatus|boolean|是否上架，是为true，否为false|
|rec_salt|int|推荐咸度|
|rec_amount|int|推荐份量|
|price|float|菜品价格|
#### ERRORS

```
服务器错误
{'error':'查询数据库中的菜品出错'},status=500
```
## 5.查询商品-菜系

### 具体请求

>请求方式 GET<br>
>URL: https://chuiyan.fivyex.com/good/cuisine?category=1
><br> 1-川 2-鲁 3-粤 4-其他
>
>### response.body
```
[
    {
        "goodser": {
            "goodsID": "4",
            "goodAmount": "麻婆豆腐",
            "goodDescription": "麻婆给您做的豆腐",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/4.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 8.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "11",
            "goodAmount": "宫保鸡丁",
            "goodDescription": "小鸡中的战斗机欧耶",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/11.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 13.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "12",
            "goodAmount": "酸菜鱼",
            "goodDescription": "又酸又菜又多余",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/12.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 14.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "13",
            "goodAmount": "夫妻肺片",
            "goodDescription": "吃完就有恋爱的感觉",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/13.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 15.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "20",
            "goodAmount": "钵钵鸡",
            "goodDescription": "冷串yyds",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/20.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 22.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "34",
            "goodAmount": "辣子鸡",
            "goodDescription": "辣鸡中的战斗机欧耶",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/34.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 11.0,
        "type1": "川",
        "type2": "平底锅"
    }
]
```
## 5.查询商品-锅具

### 具体请求

>请求方式 GET<br>
>URL: https://chuiyan.fivyex.com/good/cooker?category=1
><br>1-平底锅 2-汤锅 3-微波炉 4-电饭煲
>
>### response.body
```
[
    {
        "goodser": {
            "goodsID": "1",
            "goodAmount": "猪肉炖粉条",
            "goodDescription": "东北名菜 吃完好满足！",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/1.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 12.5,
        "type1": "其他",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "2",
            "goodAmount": "红烧肉",
            "goodDescription": "满满的汤汁",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/2.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 10.5,
        "type1": "其他",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "3",
            "goodAmount": "可乐鸡翅",
            "goodDescription": "吃完敲可乐",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/3.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 7.0,
        "type1": "其他",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "4",
            "goodAmount": "麻婆豆腐",
            "goodDescription": "麻婆给您做的豆腐",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/4.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 8.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "11",
            "goodAmount": "宫保鸡丁",
            "goodDescription": "小鸡中的战斗机欧耶",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/11.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 13.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "12",
            "goodAmount": "酸菜鱼",
            "goodDescription": "又酸又菜又多余",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/12.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 14.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "13",
            "goodAmount": "夫妻肺片",
            "goodDescription": "吃完就有恋爱的感觉",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/13.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 15.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "16",
            "goodAmount": "汽锅鸡",
            "goodDescription": "母鸡中的战斗机欧耶",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/16.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 18.0,
        "type1": "其他",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "19",
            "goodAmount": "羊肉串",
            "goodDescription": "孜然碰到辣椒 ",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/19.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 21.0,
        "type1": "其他",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "20",
            "goodAmount": "钵钵鸡",
            "goodDescription": "冷串yyds",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/20.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 22.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "34",
            "goodAmount": "辣子鸡",
            "goodDescription": "辣鸡中的战斗机欧耶",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/34.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 11.0,
        "type1": "川",
        "type2": "平底锅"
    },
    {
        "goodser": {
            "goodsID": "35",
            "goodAmount": "法式黑椒牛排",
            "goodDescription": "上流生活的必备",
            "goodImgURL": "https://chuiyan.fivyex.com/static/image/goods/35.jpg",
            "goodStatus": true
        },
        "rec_salt": 2,
        "rec_amount": 2,
        "price": 5.0,
        "type1": "其他",
        "type2": "平底锅"
    }
]
```
## 6.推荐菜品

### 具体请求

>请求方式 GET
> <br>URL https://chuiyan.fivyex.com/good/orderrec?userID=参数
###request.params
```
userID=3
```
### response.body

```
{
    "recoomendation": [
        {
            "good_name": "大盘鸡",
            "good_img": "https://chuiyan.fivyex.com/static/image/goods/18.jpg"
        },
        {
            "good_name": "麻婆豆腐",
            "good_img": "https://chuiyan.fivyex.com/static/image/goods/4.jpg"
        },
        {
            "good_name": "可乐鸡翅",
            "good_img": "https://chuiyan.fivyex.com/static/image/goods/3.jpg"
        },
        {
            "good_name": "糖醋里脊",
            "good_img": "https://chuiyan.fivyex.com/static/image/goods/6.jpg"
        }
    ]
}
```
## 7.随机四个轮播图

### 具体请求

>GET
> <br>URL https://chuiyan.fivyex.com/good/imgrotation
###response.body
```
{
    "urls": [
        {
            "good_img": "https://chuiyan.fivyex.com/static/image/goods/17.jpg"
        },
        {
            "good_img": "https://chuiyan.fivyex.com/static/image/goods/11.jpg"
        },
        {
            "good_img": "https://chuiyan.fivyex.com/static/image/goods/16.jpg"
        },
        {
            "good_img": "https://chuiyan.fivyex.com/static/image/goods/4.jpg"
        }
    ]
}
```

## 8.与STM-32交互

### 具体请求

```
请求方式 GET

<br>URL https://chuiyan.fivyex.com/good/ordercheck?order_uid=参数
```

### request.params

```
url所需要的参数
"order_uid":chuiyan62000baa-d29b-11eb-a41d-802bf98d5ef62021-06-21 22:17:17081556
```
### response.body

```
{
    "ingredient_ser": [
        {
            "pack1": [
                10.0,
                0,
                0,
                0,
                0,
                6.0,
                0.0,
                0.0
            ],
            "pack2": [
                0,
                15.0,
                15.0,
                0.0,
                15.0,
                0,
                0,
                0
            ],
            "pack3": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "pack4": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "num": 3
        },
        {
            "pack1": [
                10.0,
                0,
                0,
                0,
                0,
                15.0,
                0.0,
                10.0
            ],
            "pack2": [
                0,
                15.0,
                0.0,
                0.0,
                5.0,
                0,
                0,
                0
            ],
            "pack3": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "pack4": [
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0
            ],
            "num": 2
        }
    ]
}
```
## 9.与STM-32交互(2)

### 具体请求

```
请求方式 POST
<br>URL https://chuiyan.fivyex.com/good/orderchange
```



### request.body

```
{
    "order_uid":"62000baa-d29b-11eb-a41d-802bf98d5ef62021-06-21 22:17:17081556",
    "status":1
}
```
## 10.返回所有售货机地址

### 具体请求

```
请求方式 GET
<br>URL https://chuiyan.fivyex.com/good/machinefind
```

### response.body

```
[
    {
        "machine": {
            "center": [
                "113.3407",
                "23.165994"
            ],
            "name": "华南理工大学-北三宿舍",
            "detailAddress": "广东省广州市天河区北湖北路与北湖南路交叉口东南方向120米",
            "phone": "11111111",
            "workTime": "5:30-23:30"
        }
    },
    {
        "machine": {
            "center": [
                "113.490204",
                "23.171902"
            ],
            "name": "保罗一号机",
            "detailAddress": "广东省广州市黄浦区开创大道与大望路交汇处",
            "phone": "87236822",
            "workTime": "6:00-22:00"
        }
    },
    {
        "machine": {
            "center": [
                "113.25234",
                "23.088628"
            ],
            "name": "二号码头餐吧",
            "detailAddress": "广东省广州市海珠区海珠区革新路太古仓码头2号栈桥",
            "phone": "87231920",
            "workTime": "7:30-22:30"
        }
    },
    {
        "machine": {
            "center": [
                "113.342433",
                "23.1668"
            ],
            "name": "华南理工大学-博学楼",
            "detailAddress": "广东省广州市天河区五山路381号",
            "phone": "88910900",
            "workTime": "8:00-22:45"
        }
    },
    {
        "machine": {
            "center": [
                "113.277231",
                "23.120831"
            ],
            "name": "广州市清水濠小学-南门",
            "detailAddress": "广东省广州市越秀区培桂横巷与永安东街交叉口西南方向160米",
            "phone": "80990521",
            "workTime": "5:00-24:00"
        }
    }
]
```
## 11.返回个人所有订单

### 具体请求

```
请求方式 GET
<br>URL https://chuiyan.fivyex.com/good/orderbyuser?userID=3&status=2
```

### request.params

```
[
    {
        "order_pickup_machine_address": "广东省广州市越秀区培桂横巷与永安东街交叉口西南方向160米",
        "orderstatus": "已支付，待取货",
        "create_time": "2021-06-24T02:23:43.811787",
        "order_price": 51.0,
        "ing": {
            "ingredientsURL": "https://chuiyan.fivyex.com/static/image/packs/1.jpg",
            "ingredientsNAME": "宫保鸡丁炒料",
            "salt&spicy": [
                1,
                3
            ]
        }
    },
    {
        "order_pickup_machine_address": "广东省广州市天河区五山路381号",
        "orderstatus": "已支付，待取货",
        "create_time": "2021-06-24T02:38:34.400560",
        "order_price": 511.0,
        "ing": {
            "ingredientsURL": "https://chuiyan.fivyex.com/static/image/packs/1.jpg",
            "ingredientsNAME": "羊肉串炒料",
            "salt&spicy": [
                1,
                2
            ]
        }
    }
]
```
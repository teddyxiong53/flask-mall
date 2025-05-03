# Flask 电商平台

## 项目概述
这是一个基于Flask的电商平台项目，包含用户认证、商品展示、购物车、订单管理等功能。

## 功能特性
- 用户注册/登录
- 商品浏览与搜索
- 购物车管理
- 订单创建与支付
- 收货地址管理

## 环境要求
- Python 3.8+
- Flask 2.0+
- SQLite/MySQL/PostgreSQL

## 安装步骤
1. 克隆项目
```bash
git clone <项目地址>
cd flask-mall
```

2. 创建虚拟环境并激活
```bash
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
```bash
export FLASK_APP=app
export FLASK_ENV=development
```

5. 初始化数据库
```bash
flask db upgrade
```

## 运行项目
```bash
flask run
```

访问 http://localhost:5000 查看应用

## 数据库迁移
创建新迁移：
```bash
flask db migrate -m "迁移描述"
```

应用迁移：
```bash
flask db upgrade
```

回滚迁移：
```bash
flask db downgrade
```
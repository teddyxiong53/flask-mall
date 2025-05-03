from faker import Faker
from app import create_app, db
from app.models import Product
import random

app = create_app()
fake = Faker(['zh_CN'])

def create_fake_products(count=100):
    with app.app_context():
        for _ in range(count):
            # 生成商品类别
            categories = ['电子产品', '服装', '食品', '图书', '家居', '运动', '美妆', '玩具']
            category = random.choice(categories)
            
            # 根据类别生成相应的商品名称和描述
            if category == '电子产品':
                name = f"{random.choice(['Apple', 'Samsung', 'Xiaomi', 'Huawei'])} {random.choice(['手机', '平板', '笔记本', '耳机'])}"
            elif category == '服装':
                name = f"{random.choice(['休闲', '商务', '运动', '时尚'])} {random.choice(['T恤', '衬衫', '裤子', '外套'])}"
            else:
                name = fake.word() + random.choice(['精选', '特制', '优质', '臻品'])
            
            description = '\n'.join([
                fake.sentence(),
                f"品牌: {fake.company()}",
                f"产地: {fake.city()}",
                f"特点: {', '.join(fake.words(3))}"
            ])
            
            # 根据类别设置合理的价格范围
            price_ranges = {
                '电子产品': (999, 9999),
                '服装': (99, 999),
                '食品': (10, 199),
                '图书': (29, 199),
                '家居': (99, 1999),
                '运动': (99, 899),
                '美妆': (99, 599),
                '玩具': (29, 299)
            }
            min_price, max_price = price_ranges.get(category, (50, 500))
            price = round(random.uniform(min_price, max_price), 2)
            
            # 生成库存数量
            stock = random.randint(10, 200)
            
            # 生成图片URL（使用占位图片）
            image_url = f"https://picsum.photos/400/300?random={random.randint(1, 1000)}"
            
            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                image_url=image_url,
                category=category
            )
            db.session.add(product)
        
        db.session.commit()
        print(f'成功创建 {count} 个商品数据')

if __name__ == '__main__':
    create_fake_products()
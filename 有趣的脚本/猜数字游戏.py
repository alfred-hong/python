import random

# 创建随机数
n = random.randrange(1,100)
# 获取输入
guess = int(input("输入任意数值: "))

while n != guess: # 判断是否正确
    # 小于
    if guess < n:
        print("太小了")
        guess = int(input("再次输入数值: "))
    # 大于
    elif guess > n:
        print("太大了!")
        guess = int(input("再次输入数值: "))
    else:
        break
print("真棒，你猜对了!!")
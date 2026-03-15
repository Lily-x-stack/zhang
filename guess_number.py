# -*- coding: utf-8 -*-
"""
猜数字小游戏
随机生成1-100之间的数字，让用户猜测
"""

import random

def guess_number_game():
    target = random.randint(1, 100)
    print("="*40)
    print("       猜数字小游戏")
    print("我已经想好了一个1-100之间的数字")
    print("="*40 + "\n")
    
    while True:
        user_input = input("请输入你猜的数字: ")
        
        try:
            guess = int(user_input)
        except ValueError:
            print("请输入有效的整数\n")
            continue
        
        if guess < 1 or guess > 100:
            print("请输入1-100之间的数字\n")
            continue
        
        if guess > target:
            print("太大了\n")
        elif guess < target:
            print("太小了\n")
        else:
            print("猜对了！\n")
            break

if __name__ == "__main__":
    guess_number_game()

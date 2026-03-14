def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def main():
    input_str = input("请输入数字列表，用空格分隔：")
    try:
        numbers = [float(x) for x in input_str.split()]
        if not numbers:
            print("错误：没有输入任何数字！")
            return
        avg = calculate_average(numbers)
        print(f"列表元素的平均值为：{avg:.2f}")
    except ValueError:
        print("错误：请输入有效的数字！")

if __name__ == "__main__":
    main()

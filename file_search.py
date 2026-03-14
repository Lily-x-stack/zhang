import os

def search_keyword_in_files():
    folder_path = input("请输入要检索的文件夹路径：")
    
    if not os.path.exists(folder_path):
        print("错误：文件夹路径不存在！")
        return
    
    if not os.path.isdir(folder_path):
        print("错误：输入的不是文件夹路径！")
        return
    
    keyword = input("请输入要检索的关键词：")
    
    if not keyword:
        print("错误：关键词不能为空！")
        return
    
    results = []
    
    try:
        files = os.listdir(folder_path)
    except PermissionError:
        print("错误：没有读取文件夹的权限！")
        return
    
    txt_files = [f for f in files if f.endswith('.txt') and os.path.isfile(os.path.join(folder_path, f))]
    
    if not txt_files:
        print("该文件夹下没有找到.txt文件")
        return
    
    for filename in txt_files:
        file_path = os.path.join(folder_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                file_results = []
                for line_num, line in enumerate(lines, 1):
                    if keyword in line:
                        file_results.append((line_num, line.strip()))
                if file_results:
                    results.append((filename, file_results))
        except PermissionError:
            print(f"警告：无法读取文件 {filename}（权限不足）")
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as f:
                    lines = f.readlines()
                    file_results = []
                    for line_num, line in enumerate(lines, 1):
                        if keyword in line:
                            file_results.append((line_num, line.strip()))
                    if file_results:
                        results.append((filename, file_results))
            except Exception as e:
                print(f"警告：无法读取文件 {filename}（编码错误）")
        except Exception as e:
            print(f"警告：读取文件 {filename} 时出错：{str(e)}")
    
    if not results:
        print(f"\n未找到包含关键词 '{keyword}' 的文件")
        return
    
    print("\n" + "="*50)
    print(f"检索结果：共找到 {len(results)} 个包含关键词 '{keyword}' 的文件")
    print("="*50)
    
    for filename, matches in results:
        print(f"\n【{filename}】共 {len(matches)} 处匹配：")
        for line_num, content in matches:
            print(f"  第 {line_num} 行：{content}")
    
    save_choice = input("\n是否将检索结果保存到 search_result.txt？(y/n)：")
    if save_choice.lower() == 'y':
        result_file_path = os.path.join(folder_path, 'search_result.txt')
        try:
            with open(result_file_path, 'w', encoding='utf-8') as f:
                f.write(f"关键词检索结果\n")
                f.write(f"关键词：{keyword}\n")
                f.write(f"检索路径：{folder_path}\n")
                f.write("="*50 + "\n\n")
                for filename, matches in results:
                    f.write(f"【{filename}】共 {len(matches)} 处匹配：\n")
                    for line_num, content in matches:
                        f.write(f"  第 {line_num} 行：{content}\n")
                    f.write("\n")
            print(f"结果已保存到：{result_file_path}")
        except Exception as e:
            print(f"保存结果时出错：{str(e)}")

if __name__ == "__main__":
    search_keyword_in_files()

import tkinter as tk
from PIL import Image, ImageTk

# 全局变量
items = ["China", "Beijing", "Shanghai", "Guangzhou", "Wuhan"]
items_per_page = 3
filtered_items = items
current_page = 0
total_pages = (len(filtered_items) + items_per_page - 1) // items_per_page

# 创建主窗口
window = tk.Tk()
window.geometry('1000x700')
window.title('盒子 v0.1版')

# 在窗口顶部添加字样的标签
www_label = tk.Label(window, text="b站up-TF惜夕", font=("Arial", 10, "bold"))
www_label.place(x=380, y=30)

# 创建列表框
listbox = tk.Listbox(window, width=100)
listbox.place(x=200, y=180)

# 创建搜索输入框和按钮
search_entry = tk.Entry(window)
search_entry.place(x=400, y=100)

def search(event=None):
    keyword = search_entry.get().strip()
    if not keyword:
        show_new_popup("请输入你想搜索的内容")
        return
    global filtered_items, total_pages, current_page
    filtered_items = [item for item in items if keyword.lower() in item.lower()]
    total_pages = (len(filtered_items) + items_per_page - 1) // items_per_page
    current_page = 0
    update_listbox()
    page_label.config(text=f'当前页: 第{current_page+1}页 / 共{total_pages}页')
    show_return_button()

search_button = tk.Button(window, text="搜索", command=search, bg="red", fg="white")
search_button.place(x=550, y=100)

# 绑定回车键触发搜索
window.bind("<Return>", search)

# 创建页码标签
page_label = tk.Label(window, text=f'当前页: 第{current_page+1}页 / 共{total_pages}页')
page_label.place(x=470, y=500)

# 翻到下一页
def next_page():
    global current_page
    if current_page < total_pages - 1:
        current_page += 1
        update_listbox()
        page_label.config(text=f'当前页: 第{current_page+1}页 / 共{total_pages}页')

# 翻到上一页
def prev_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        update_listbox()
        page_label.config(text=f'当前页: 第{current_page+1}页 / 共{total_pages}页')

next_button = tk.Button(window, text="下一页", command=next_page, bg="red", fg="white")
next_button.place(x=600, y=500)

prev_button = tk.Button(window, text="上一页", command=prev_page, bg="red", fg="white")
prev_button.place(x=420, y=500)

# 跳转到指定页码
def goto_page():
    global current_page
    input_text = entry.get()
    if input_text:
        try:
            page_num = int(input_text) - 1
            if 0 <= page_num < total_pages:
                current_page = page_num
                update_listbox()
                page_label.config(text=f'当前页: 第{current_page+1}页 / 共{total_pages}页')
            else:
                show_new_popup("无效的页码")
        except ValueError:
            show_new_popup("请输入有效的页码")
    else:
        show_new_popup("请输入页码再尝试跳转！")

entry = tk.Entry(window)
entry.place(x=400, y=150)

goto_button = tk.Button(window, text="跳转", command=goto_page, bg="red", fg="white")
goto_button.place(x=550, y=150)

# 显示返回按钮
def show_return_button():
    return_button.place(x=600, y=100)

# 返回至完整列表
def return_to_full_list():
    global filtered_items, total_pages, current_page
    filtered_items = items
    total_pages = (len(filtered_items) + items_per_page - 1) // items_per_page
    current_page = 0
    update_listbox()
    page_label.config(text=f'当前页: 第{current_page+1}页 / 共{total_pages}页')
    return_button.place_forget()

return_button = tk.Button(window, text="返回", command=return_to_full_list, bg="red", fg="white")

# 创建无搜索结果标签
no_results_label = tk.Label(window, text="无搜索结果", font=("Arial", 12, "bold"), fg="red")

# 显示弹窗
def show_popup():
    popup_window = tk.Toplevel(window)
    popup_window.geometry('600x400')
    popup_window.title('弹窗')

    # 打开图像文件
    image = Image.open('1.jpg')

    # 调整图像大小以适应弹窗
    image = image.resize((400, 300))

    # 创建PhotoImage对象并分配给标签
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(popup_window, image=photo)
    label.image = photo
    label.pack()

# 显示新的弹窗
def show_new_popup(message):
    new_popup_window = tk.Toplevel(window)
    new_popup_window.geometry('200x100')
    new_popup_window.title('提示')

    message_label = tk.Label(new_popup_window, text=message)
    message_label.pack()
    
popup_button = tk.Button(window, text="弹窗按钮", command=show_popup)
popup_button.place(x=300, y=500)

# 添加新列表项目
add_entry = tk.Entry(window)
add_entry.place(x=650, y=150)

def add_item():
    global items, filtered_items, total_pages
    new_item = add_entry.get().strip()
    if new_item:
        items.append(new_item)
        if search_entry.get().strip() and new_item.lower() in filtered_items:
            filtered_items.append(new_item)
        if len(filtered_items) % items_per_page == 1:
            total_pages = (len(filtered_items) + items_per_page - 1) // items_per_page
        update_listbox()
        add_entry.delete(0, tk.END)

add_button = tk.Button(window, text="添加", command=add_item, bg="green", fg="white")
add_button.place(x=800, y=150)

# 更新列表框内容
def update_listbox():
    listbox.delete(0, tk.END)
    start_index = current_page * items_per_page
    end_index = min(start_index + items_per_page, len(filtered_items))
    if start_index >= len(filtered_items):
        no_results_label.place(x=400, y=210)
    else:
        no_results_label.place_forget()
        for i in range(start_index, end_index):
            item = f"序号{i+1}     {filtered_items[i]}"
            listbox.insert(tk.END, item)
    page_label.config(text=f'当前页: 第{current_page+1}页 / 共{total_pages}页')


# 初始化列表框和页码标签
update_listbox()

# 进入主循环
window.mainloop()

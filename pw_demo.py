from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        # 1. 启动浏览器（可以选择无头模式或非无头模式）
        browser = p.chromium.launch(headless=False)  # 设置为 False 可以看到浏览器窗口
        page = browser.new_page()

        # 2. 打开目标网页
        url = "https://price.21food.cn/market-p2.html"
        page.goto(url)

        # 3. 等待页面加载完成（可以指定某个选择器来确保内容加载完毕）
        try:
            page.wait_for_selector(".sjs_top_cent_erv", timeout=10000)  # 替换为实际的选择器，超时时间为 10 秒
        except Exception as e:
            print("等待元素超时或发生错误:", e)
            browser.close()
            return

        # 4. 提取页面内容
        # 方法 1：获取整个页面的 HTML
        full_html = page.content()
        print("Full HTML Content:")
        print(full_html)

        # 方法 2：提取特定元素的内容
        try:
            dynamic_content = page.eval_on_selector(".target-class", "el => el.textContent")  # 替换为实际的选择器
            print("Dynamic Content Extracted:", dynamic_content)
        except Exception as e:
            print("提取动态内容失败:", e)

        # 方法 3：执行自定义 JavaScript 并获取结果
        try:
            js_result = page.evaluate("""
                () => {
                    // 这里可以写任意的 JavaScript 代码
                    return document.title;  // 返回页面标题
                }
            """)
            print("Page Title (via JS):", js_result)
        except Exception as e:
            print("执行 JavaScript 失败:", e)

        # 5. 关闭浏览器
        browser.close()

if __name__ == "__main__":
    main()
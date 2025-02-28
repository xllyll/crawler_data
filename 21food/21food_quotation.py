import base64
import time
import xlwt
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import food_core
from orc import image_utils


# 加载数据
def loadData(browser, id, pageIndex):
    try:
        # 创建新页面
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        stealth_sync(page)  # 隐藏 Playwright 特征

        # 打开目标网页
        url = f"https://price.21food.cn/market/{id}-p{pageIndex}.html"
        print(f"URL: {url}")
        page.goto(url)
        page.mouse.move(100, 200)  # 模拟鼠标移动
        page.mouse.click(100, 200)  # 模拟鼠标点击
        # 检查是否出现 IP 屏蔽页面
        error_main = page.query_selector("div.error_main")
        if error_main:
            print("检测到 IP 屏蔽页面，开始处理验证码...")
            # 处理验证码
            # 获取验证码图片
            captcha_image_element = page.query_selector("div.error_min_t_right img")
            if captcha_image_element:
                # 获取验证码图片的二进制数据
                captcha_image_data = captcha_image_element.screenshot(type="png")
                # 如果需要 Base64 编码，可以手动转换
                captcha_image_base64 = base64.b64encode(captcha_image_data).decode("utf-8")
                image_utils.save_base64_to_png(captcha_image_base64,"images/output.png")
                # # 识别验证码
                # captcha_text = get_captcha_text(captcha_image_data)
                #
                # # 填写验证码并提交表单
                # page.fill("input#delipcode", captcha_text)
                # page.click("input[type='submit']")
                #
                # # 等待页面跳转或验证成功
                # page.wait_for_load_state("networkidle")
            return 1
        # 等待页面加载完成
        page.wait_for_selector("div.sjs_top_cent_erv li", timeout=15000)

        # 获取所有的 <li> 元素
        li_elements = page.query_selector_all("div.sjs_top_cent_erv li")

        # 遍历每个 <li> 元素并提取数据
        for li in li_elements:
            td_elements = li.query_selector_all("td")
            if len(td_elements) < 7:
                continue  # 跳过不完整的数据行

            td1 = td_elements[0].query_selector("a")
            td2 = td_elements[1]
            td3 = td_elements[2]
            td4 = td_elements[3].query_selector("span")
            td5 = td_elements[4].query_selector("span")
            td6 = td_elements[5].query_selector("span")
            td7 = td_elements[6].query_selector("span")

            good_name = td1.inner_text() if td1 else ""
            href = td1.get_attribute("href") if td1 else ""
            good_id = href.replace(f"/product/{id}-", "").replace(".html", "") if href else ""

            companyName = td2.inner_text() if td2 else ""
            max_p = td4.inner_text() if td4 else ""
            min_p = td5.inner_text() if td5 else ""
            a_p = td6.inner_text() if td6 else ""
            q_time = td7.inner_text() if td7 else ""

            print(f"ID: {good_id}, Name: {good_name}, Company: {companyName}, Max: {max_p}, Min: {min_p}, Avg: {a_p}, Time: {q_time}")

            # 创建 Quotation 对象
            qData = food_core.Quotation(
                0, good_id, good_name, id, companyName, max_p, min_p, a_p, q_time
            )
            food_core.saveQuotationData2DB(qData)


        # 获取总页数
        total_page = 1
        if pageIndex == 1:
            page_a_elements = page.query_selector_all("div.page a")
            if len(page_a_elements) > 1:
                total_page = int(page_a_elements[-2].inner_text())
            print(f"Total Pages: {total_page}")

        return total_page

    finally:
        page.close()
        context.close()

# 主函数
def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 启动浏览器

        # 第一页加载并获取总页数
        total_pages = loadData(browser, 8, 1)
        time.sleep(5)

        # 加载后续页面
        for i in range(2, total_pages + 1):
            loadData(browser, 8, i)
            time.sleep(5)

if __name__ == "__main__":
    main()
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
def main():
    with sync_playwright() as p:
        # 1. 启动浏览器（可以选择无头模式或非无头模式）
        browser = p.chromium.launch(headless=False)  # 设置为 False 可以看到浏览器窗口
        context = browser.new_context()
        page = context.new_page()
        stealth_sync(page)  # 隐藏 Playwright 特征
        # 2. 打开目标网页
        url = "https://price.21food.cn/market-p2.html"
        page.goto(url)
        # page.wait_for_timeout(5000)
        full_html = page.content()
        print("Full HTML Content:")
        print(full_html)
        getData(full_html)

        # 获取所有的 <li> 元素
        li_elements = page.query_selector_all("div.sjs_top_cent_erv li")

        # 遍历每个 <li> 元素并提取数据
        for li in li_elements:
            td_elements = li.query_selector_all("td")
            td1 = td_elements[0].query_selector("a")
            name = td1.inner_text()
            href = td1.get_attribute("href")
            id = href.replace("/market/","")
            id = id.replace(".html","")
            print(f"ID: {id} name {name}")

def getData(html):
    soup = BeautifulSoup(html, "html.parser")
    sjs_top_cent_erv = soup.find_all('div',class_="sjs_top_cent_erv")
    datalist = []  #用来存储爬取的网页信息
    print(len(sjs_top_cent_erv))
    return datalist

if __name__ == "__main__":
    main()
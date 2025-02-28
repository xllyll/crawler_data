import time
import sqlite3  # 进行SQLite数据库操作
import xlwt
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import food_core
companyDatas = []

def loadData(id,pageIndex):

    with sync_playwright() as p:
        # 1. 启动浏览器（可以选择无头模式或非无头模式）
        browser = p.chromium.launch(headless=True)  # 设置为 False 可以看到浏览器窗口 True 隐藏浏览器窗口
        # context = browser.new_context()
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        stealth_sync(page)  # 隐藏 Playwright 特征
        # 2. 打开目标网页
        url = "https://price.21food.cn/market/"+str(id)+"-p"+str(pageIndex)+".html"
        print(f"url:{url}")
        page.goto(url)
        page.mouse.move(100, 200)  # 模拟鼠标移动
        page.mouse.click(100, 200)  # 模拟鼠标点击

        page.wait_for_selector("div.sjs_top_cent_erv li", timeout=15000)

        # page.wait_for_timeout(5000)
        full_html = page.content()
        # print("Full HTML Content:")
        # print(full_html)
        getData(full_html)

        # 获取所有的 <li> 元素
        li_elements = page.query_selector_all("div.sjs_top_cent_erv li")

        # 遍历每个 <li> 元素并提取数据
        for li in li_elements:
            td_elements = li.query_selector_all("td")
            td1 = td_elements[0].query_selector("a")
            td2 = td_elements[1]
            td3 = td_elements[2]
            td4 = td_elements[3].query_selector("span")
            td5 = td_elements[4].query_selector("span")
            td6 = td_elements[5].query_selector("span")
            td7 = td_elements[6].query_selector("span")
            good_name = td1.inner_text()
            href = td1.get_attribute("href")
            good_id = href.replace("/product/"+str(id)+"-","")
            good_id = good_id.replace(".html","")

            companyName = td2.inner_text()
            max_p = td4.inner_text()
            min_p = td5.inner_text()
            a_p = td6.inner_text()
            q_time = td7.inner_text()

            print(f"ID: {good_id} name {good_name} city: {companyName} max_p: {max_p} min_p: {min_p} a_p: {a_p} q_time: {q_time}")
            data = {
                'id':good_id,
                'name':good_name,
                'companyId':id,
                'companyName':companyName,
                'max_p':max_p,
                'min_p':min_p,
                'a_p':a_p,
                'q_time':q_time
            }
            # companyDatas.append(data)
            qData  = food_core.Quotation(0,good_id,good_name,id,companyName,max_p,min_p,a_p,q_time)
            food_core.saveQuotationData2DB(qData)

def getData(html):
    soup = BeautifulSoup(html, "html.parser")
    sjs_top_cent_erv = soup.find_all('div',class_="sjs_top_cent_erv")
    datalist = []  #用来存储爬取的网页信息
    print(len(sjs_top_cent_erv))
    return datalist

def saveData():
    print("save.......")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0) #创建workbook对象
    sheet = book.add_sheet('21food_company', cell_overwrite_ok=True) #创建工作表
    col = ("公司ID","公司名称","所在城市")
    for i in range(0,3):
        sheet.write(0,i,col[i])  #列名
    for i in range(0, len(companyDatas)):
        # print("第%d条" %(i+1))       #输出语句，用来测试
        data = companyDatas[i]
        sheet.write(i+1,0,data['id'])
        sheet.write(i+1,1,data['name'])
        sheet.write(i+1,2,data['city'])
    book.save('21food_company.xls') #保存




if __name__ == "__main__":
    # companyDatas = food_core.queryAllCompanies()
    # for company in companyDatas:
    #     id = company['id']
    #     print(f"=============>{time.time()} {id} ")
    loadData(8,1)
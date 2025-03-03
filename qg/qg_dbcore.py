import sqlite3
from types import GetSetDescriptorType


def initDB():
    # SQLite 不支持表字段的 COMMENT 属性，可以使用其他方式记录表结构说明
    sql = '''
        CREATE TABLE IF NOT EXISTS t_company (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 公司Id
            name TEXT,                            -- 公司名称
            city TEXT                             -- 所在城市
        );
        CREATE TABLE IF NOT EXISTS t_goods (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 商品Id
            name TEXT                             -- 商品名称
        );
        CREATE TABLE IF NOT EXISTS t_quotation (
            id INTEGER PRIMARY KEY AUTOINCREMENT, -- 报价Id
            good_id INTEGER,                      -- 商品ID
            good_name TEXT,                       -- 商品名称
            company_id TEXT,                   -- 公司ID
            company_name TEXT,                    -- 公司名称
            max_price TEXT,                       -- 最高价
            min_price TEXT,                       -- 最低价
            price TEXT,                           -- 平均价
            q_time TEXT                           -- 时间
        );
    '''  # 创建数据表
    conn = sqlite3.connect('qg_food.db')  # 连接数据库（如果不存在则会创建）
    try:
        # 使用 executescript 方法执行多条 SQL 语句
        conn.executescript(sql)
        print("数据库表创建成功！")
    except Exception as e:
        print(f"创建数据库表失败：{e}")
    finally:
        conn.close()  # 关闭连接



def queryAllCompanies():
    # 连接数据库
    conn = sqlite3.connect("qg_food.db")
    cur = conn.cursor()
    companys = []
    try:
        # 查询所有公司信息
        sql = '''
            SELECT id, name, city FROM t_company
        '''
        cur.execute(sql)

        # 获取所有结果
        rows = cur.fetchall()

        # 打印结果
        if rows:
            print("查询结果：")
            for row in rows:
                company = {
                    "id":row[0],
                    "name":row[1],
                    "city":row[2]
                }
                print(f"ID: {row[0]}, 名称: {row[1]}, 城市: {row[2]}")
                companys.append(company)
        else:
            print("没有找到任何记录！")
    except Exception as e:
        print(f"查询数据失败：{e}")
    finally:
        # 关闭游标和连接
        cur.close()
        conn.close()
    return companys

class QGQuotation:
    id = None
    goodId = None
    goodName = None
    companyId = None
    companyName = None
    maxPrice = None
    minPrice = None
    price = None
    qTime = None
    def __init__(self, id, goodId, goodName, companyId, companyName, maxPrice, minPrice, price, qTime):
        self.id = id
        self.goodId = goodId
        self.goodName = goodName
        self.companyId = companyId
        self.companyName = companyName
        self.maxPrice = maxPrice
        self.minPrice = minPrice
        self.price = price
        self.qTime = qTime



def saveQuotationData2DB(q:QGQuotation):
    # 连接数据库
    conn = sqlite3.connect("qg_food.db")
    cur = conn.cursor()

    try:
        # 查询是否已存在相同的数据（同一天、同一公司、同一商品）
        sql_check = '''
            SELECT id FROM t_quotation 
            WHERE good_id = ? AND company_id = ? AND q_time = ?
        '''
        cur.execute(sql_check, (q.goodId, q.companyId, q.qTime))
        result = cur.fetchone()  # 获取第一条匹配的记录

        if result is None:
            # 如果不存在相同的数据，则插入新数据
            sql_insert = '''
                INSERT INTO t_quotation (good_id, good_name, company_id, company_name, max_price, min_price, price, q_time) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cur.execute(sql_insert, (q.goodId, q.goodName, q.companyId, q.companyName, q.maxPrice, q.minPrice, q.price, q.qTime))
            conn.commit()
            print("数据插入成功！🎁🎁🎁")
        else:
            print("数据已存在，跳过插入！👣👣👣")
    except Exception as e:
        print(f"插入数据失败：{e}")
    finally:
        # 关闭游标和连接
        cur.close()
        conn.close()

def batchSaveQuotationData2DB(quotation_list):
    conn = sqlite3.connect("21food.db")
    cur = conn.cursor()

    try:
        sql = '''
            INSERT INTO t_quotation (good_id, good_name, company_id, company_name, max_price, min_price, price, q_time) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        data = [
            (q.goodId, q.goodName, q.companyId, q.companyName, q.maxPrice, q.minPrice, q.price, q.qTime)
            for q in quotation_list
        ]
        cur.executemany(sql, data)
        conn.commit()
        print(f"成功插入 {len(quotation_list)} 条数据！")
    except Exception as e:
        print(f"插入数据失败：{e}")
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    initDB()
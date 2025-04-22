import requests
import os
from datetime import datetime
from playwright.async_api import async_playwright
import asyncio

async def save_page_source(url, output_dir="output"):
    """
    保存網頁源代碼到HTML文件
    
    Args:
        url: 目標網頁URL
        output_dir: 輸出目錄路徑
    """
    try:
        # 創建輸出目錄
        os.makedirs(output_dir, exist_ok=True)
        a = async_playwright()
        print(a, '     oi8yhgorjiunjefrwovnuj')
        # 生成輸出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"page_source_{timestamp}.html"
        output_path = os.path.join(output_dir, filename)
        async with async_playwright() as p:
            print("sdwqfrgethyjufjthdrgef")
            # 啟動瀏覽器
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            print(f"正在訪問頁面: {url}")
            # 訪問頁面
            await page.goto(url)
            
            # 等待頁面加載完成
            await page.wait_for_load_state('networkidle')
            print("頁面加載完成")
            
            # 獲取頁面源代碼
            content = await page.content()
            
            # 保存到文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"頁面源代碼已保存到: {output_path}")
            
            # 關閉瀏覽器
            await browser.close()
            
            return output_path
        
        print("sdwqfrgethyjufjthdrgef")
    except Exception as e:
        print(f"保存頁面源代碼時發生錯誤: {str(e)}")
        return None


async def run(username):
    """
    主要執行函數
    """
    url = f'https://www.threads.net/@{username}'
    return await save_page_source(url=url)

async def main(username):
    """
    主要執行函數
    """
    url = f'https://www.threads.net/@{username}'
    return await save_page_source(url=url)

if __name__ == "__main__":
    # 測試用例
    username = "ray.realms"
    asyncio.run(main(username))


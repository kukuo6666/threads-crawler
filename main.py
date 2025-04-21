import os
import json
import asyncio
import argparse
from datetime import datetime
from scarch_html import main as fetch_html
from scarch_parser import parse_threads_posts, read_html_file

def save_posts_to_json(posts_data, username):
    """
    將解析後的貼文資料儲存為 JSON 檔案
    """
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"posts_{username}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(posts_data, f, ensure_ascii=False, indent=2)
    
    return filepath

async def process_user_threads(username):
    """
    處理指定用戶的 Threads 頁面
    """
    try:
        print(f"Fetching threads for user @{username}...")
        html_path = await fetch_html(username)
        
        if not html_path:
            print("Failed to fetch HTML content")
            return False
        
        print(f"HTML saved to: {html_path}")
        
        # 讀取並解析 HTML 內容
        print("Parsing posts...")
        html_content = read_html_file(html_path)
        
        if not html_content:
            print("Failed to read HTML file")
            return False
            
        posts_data = parse_threads_posts(html_content)
        
        if not posts_data:
            print("No posts found in the HTML content")
            return False
        
        # 儲存解析結果為 JSON
        json_path = save_posts_to_json(posts_data, username)
        print(f"Posts data saved to: {json_path}")
        
        return True
        
    except Exception as e:
        print(f"Error processing threads: {str(e)}")
        return False

def parse_arguments():
    """
    解析命令行參數
    """
    parser = argparse.ArgumentParser(description='Threads 帖文爬蟲工具')
    parser.add_argument('-u', '--username', 
                      type=str, 
                      required=True,
                      help='要爬取的 Threads 用戶名')
    return parser.parse_args()

async def main():
    """
    主程式進入點
    """
    try:
        args = parse_arguments()
        username = args.username
        
        if not username:
            print("Username cannot be empty")
            return
        
        success = await process_user_threads(username)
        if success:
            print("Process completed successfully!")
        else:
            print("Process failed!")
            
    except Exception as e:
        print(f"Error in main: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
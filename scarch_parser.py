import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def extract_post_info(post_element):
    """
    從單個貼文元素中提取資訊
    """
    # 擷取作者資訊
    author_info = {}
    author_link = post_element.select_one('a[href^="/@"]')
    if author_link:
        author_info['username'] = author_link.get('href').replace('/@', '')
        # 檢查是否有驗證標記
        verified_badge = post_element.select_one('svg[aria-label="Verified"]')
        author_info['verified'] = verified_badge is not None
        
    # 擷取發文時間
    time_element = post_element.select_one('time')
    post_time = time_element.get('datetime') if time_element else None
    
    # 擷取貼文內容
    content_element = post_element.select_one('.x1a6qonq')
    content = content_element.get_text() if content_element else ''
    
    # 擷取互動數據
    interactions = {}
    interaction_stats = post_element.select('.xu9jpxn')
    if interaction_stats:
        # 點讚數
        likes = interaction_stats[0].get_text()
        interactions['likes'] = int(likes) if likes else 0
        # 評論數
        comments = interaction_stats[1].get_text() if len(interaction_stats) > 1 else '0'
        interactions['comments'] = int(comments) if comments else 0
        # 分享數
        shares = interaction_stats[-1].get_text() if len(interaction_stats) > 2 else '0'
        interactions['shares'] = int(shares) if shares else 0
    
    # 組合所有資訊
    post_data = {
        'author': author_info,
        'posted_at': post_time,
        'content': content,
        'interactions': interactions
    }
    
    return post_data

def read_html_file(file_path):
    """
    讀取 HTML 檔案
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return None

def parse_threads_posts(html_content):
    """
    解析 HTML 內容中的所有貼文
    """
    if not html_content:
        return []
        
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = soup.select('.xrvj5dj.xd0jker.x1evr45z')
    
    all_posts = []
    for post in posts:
        post_data = extract_post_info(post)
        all_posts.append(post_data)
    
    return all_posts

if __name__ == "__main__":
    # 測試用例
    html_content = read_html_file('./page_source_20250421_125537.html')
    if html_content:
        posts = parse_threads_posts(html_content)
        print(json.dumps(posts, ensure_ascii=False, indent=2))
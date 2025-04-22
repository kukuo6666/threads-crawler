from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import asyncio
from typing import Optional, List
from datetime import datetime
import subprocess
import json
import os

from scarch_html import run as fetch_html
from scarch_parser import parse_threads_posts, read_html_file

app = FastAPI(
    title="Threads 爬蟲 API",
    description="用於抓取 Threads 用戶帖文的 API 服務",
    version="1.0.1"
)

class ThreadsPost(BaseModel):
    """帖文數據模型"""
    author: dict
    posted_at: Optional[str]
    content: str
    interactions: dict

class ThreadsResponse(BaseModel):
    """API 響應模型"""
    username: str
    timestamp: str
    total_posts: int
    posts: List[ThreadsPost]

@app.get("/")
async def root():
    """API 根路徑"""
    return {
        "message": "歡迎使用 Threads 爬蟲 API",
        "version": "1.0.1",
        "endpoints": [
            {
                "path": "/crawl/{username}",
                "method": "GET",
                "description": "抓取指定用戶的 Threads 帖文"
            }
        ]
    }

@app.get("/crawl/{username}", response_model=ThreadsResponse)
async def crawl_user_threads(username: str):
    """
    抓取指定用戶的 Threads 帖文
    
    - **username**: Threads 用戶名（不需要包含 @ 符號）
    """
    try:
        # 運行 main.py 腳本
        process = subprocess.run(
            [".venv/Scripts/python.exe", "main.py", "--username", username],
            capture_output=True,
            encoding='utf-8',  # 明確指定使用 UTF-8 編碼
            text=True,
            check=True
        )
        

        if process.returncode != 0:
            print(f"Error output: {process.stderr}")
            raise HTTPException(status_code=500, detail="爬蟲腳本執行失敗")
            
        # 查找最新的輸出文件
        output_dir = "output"
        json_files = [f for f in os.listdir(output_dir) if f.startswith(f"posts_{username}_")]
        if not json_files:
            raise HTTPException(status_code=404, detail="未找到輸出文件")
            
        latest_file = max(json_files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
        json_path = os.path.join(output_dir, latest_file)
        
        # 讀取 JSON 文件
        with open(json_path, 'r', encoding='utf-8') as f:
            posts_data = json.load(f)
        
        # 構建響應數據
        response_data = {
            "username": username,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_posts": len(posts_data),
            "posts": posts_data
        }
        
        return response_data
        
    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e.stderr}")
        raise HTTPException(status_code=500, detail="爬蟲腳本執行出錯")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info",  # 添加這行
        access_log=True    # 添加這行
    ) 
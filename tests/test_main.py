import asyncio
from unittest.mock import patch

from fastapi.testclient import TestClient
import pytest

# 在导入 app 之前模拟 setup_services
# 这样可以确保在 TestClient 初始化并触发 lifespan 事件时，
# 调用的是模拟的函数而不是原始的函数。
@patch('main.setup_services', new_callable=lambda: asyncio.coroutine(lambda: None))
def test_read_main(mock_setup_services):
    """
    测试根路径 (/) 是否返回 'Hello world!'
    """
    # 我们需要在导入app之前进行patch，但由于Python的导入机制，
    # 直接在顶层执行此操作很棘手。
    # 一个更清晰的方法是动态导入或重载模块，
    # 但为了简单起见，我们在这里导入并依赖pytest的执行顺序。
    # 更健壮的方案是使用 pytest fixture 来处理 patch 和 client 的创建。
    from main import app
    
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == "Hello world!"

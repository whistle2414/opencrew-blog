import requests
from types.blog import BlogPostDraft, BlogPostInput
MCP_URL = 'http://localhost:3000/save-post'
class MCPSaveError(Exception): pass
def save_post_via_mcp(draft, input):
    payload = {'title':draft.title,'content':draft.content,'topic':input.topic,'created_by':input.created_by,'tags':input.tags,'seo_keywords':input.seo_keywords,'status':'draft'}
    try:
        r = requests.post(MCP_URL, json=payload, timeout=10)
        r.raise_for_status()
    except requests.exceptions.ConnectionError: raise MCPSaveError('MCP 연결 실패')
    except requests.exceptions.Timeout: raise MCPSaveError('MCP 시간초과')
    result = r.json()
    if not result.get('success'): raise MCPSaveError(f'저장실패:{result}')
    return result
import json, re
from langchain_anthropic import ChatAnthropic
from types.blog import BlogPostDraft
MODEL_NAME = 'claude-3-5-sonnet-20241022'
def get_llm(): return ChatAnthropic(model=MODEL_NAME, temperature=0.7, max_tokens=4096)
def parse_blog_response(raw, topic):
    text = re.sub(r'\x60\x60\x60(?:json)?\s*', '', raw)
    text = re.sub(r'\x60\x60\x60', '', text).strip()
    try: data = json.loads(text)
    except:
        m = re.search(r'\{.*\}', text, re.DOTALL)
        if m: data = json.loads(m.group())
        else: raise ValueError(f'JSON실패\n{text[:200]}')
    t = data.get('title','').strip(); c = data.get('content','').strip()
    if not t: raise ValueError('title없음')
    if not c: raise ValueError('content없음')
    return BlogPostDraft(title=t, content=c, topic=topic, raw_output=raw)
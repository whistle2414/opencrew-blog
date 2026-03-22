from types.blog import BlogPostInput, LENGTH_MAP

def build_blog_prompt(i: BlogPostInput) -> str:
    mc = LENGTH_MAP.get(i.length, 600)
    tg = {'informative':'정보 전달형','casual':'친근 대화체','professional':'격식체'}.get(i.tone,'정보 전달형')
    kw = f'SEO: {chr(44).join(i.seo_keywords)}' if i.seo_keywords else ''
    return f'블로그 작가입니다. 주제:{i.topic} 언어:{i.language} 톤:{tg} 최소{mc}자\n{kw}\n코드블록 없이 JSON만:\n{{\
import argparse, sys
from types.blog import BlogPostInput
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--topic');p.add_argument('--tone',choices=['informative','casual','professional'])
    p.add_argument('--length',choices=['short','medium','long']);p.add_argument('--language',default='ko')
    p.add_argument('--tags',default='');p.add_argument('--keywords',default='')
    p.add_argument('--mode',default='openclaw',choices=['openclaw','direct'])
    args=p.parse_args()
    if args.topic:
        req={'topic':args.topic,'tone':args.tone,'length':args.length,'language':args.language,'tags':args.tags,'seo_keywords':args.keywords,'intent':'workflow','workflow':'blog_create_and_save'}
    else:
        print('='*50);topic=input('블로그 주제: ').strip()
        if not topic: sys.exit('주제필요')
        tone=input('톤(엔터=기본): ').strip() or None
        length=input('길이(엔터=기본): ').strip() or None
        req={'topic':topic,'tone':tone,'length':length,'intent':'workflow','workflow':'blog_create_and_save'}
    if args.mode=='openclaw':
        from openclaw.intent_router import IntentRouter
        result=IntentRouter().dispatch(req)
    else:
        from workflow.blog_create_and_save import run_blog_create_and_save
        r=run_blog_create_and_save(BlogPostInput(topic=req['topic'],tone=req.get('tone') or 'informative',length=req.get('length') or 'medium'))
        result={'success':r.success,'title':r.title,'content_preview':r.content_preview,'error':r.error}
    print('\\n'+'='*50)
    print(f'[OK] {result.get(\
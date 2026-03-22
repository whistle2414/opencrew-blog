from types.blog import BlogPostInput
WF={'blog_create_and_save':'workflow.blog_create_and_save'}
class WorkflowDispatcher:
    def dispatch(self,req):
        wf=req.get('workflow','blog_create_and_save')
        if wf not in WF: return {'success':False,'error':f'없는workflow:{wf}'}
        from openclaw.context_manager import ContextManager
        ctx=ContextManager().load_for_workflow(wf)
        def tolist(v): return v if isinstance(v,list) else [x.strip() for x in v.split(',') if x.strip()]
        inp=BlogPostInput(topic=req.get('topic',''),tone=req.get('tone') or ctx.get('default_tone','informative'),length=req.get('length') or ctx.get('default_length','medium'),language=req.get('language','ko'),tags=tolist(req.get('tags',[])),seo_keywords=tolist(req.get('seo_keywords',[])))
        from workflow.blog_create_and_save import run_blog_create_and_save
        r=run_blog_create_and_save(inp)
        return {'success':r.success,'intent':'workflow','workflow':wf,'title':r.title,'content_preview':r.content_preview,'error':r.error}
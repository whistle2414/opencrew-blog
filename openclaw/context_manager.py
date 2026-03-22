import importlib
CONTEXT_MAP={'blog_create_and_save':'openclaw.context.blog_rules'}
class ContextManager:
    def load_for_workflow(self,name):
        m=CONTEXT_MAP.get(name)
        return getattr(importlib.import_module(m),'CONTEXT',{}) if m else {}
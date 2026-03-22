VALID={'monitoring','coding','analysis','department','workflow','chat'}
class IntentRouter:
    def route(self,req):
        e=req.get('intent','').lower()
        return e if e and e in VALID else 'workflow'
    def dispatch(self,req):
        if self.route(req)=='workflow':
            from openclaw.intents.workflow.dispatcher import WorkflowDispatcher
            return WorkflowDispatcher().dispatch(req)
        return {'success':False,'error':'지원하지 않는 intent'}
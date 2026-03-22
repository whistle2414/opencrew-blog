from types.blog import BlogPostDraft, LENGTH_MAP
FORBIDDEN = ['AI가 작성했습니다','ChatGPT','인공지능이 쓴']
class ValidationError(Exception): pass
def validate_post(draft, length='medium'):
    if not draft.title or len(draft.title.strip()) < 5: raise ValidationError('title 오류')
    mc = LENGTH_MAP.get(length, 600)
    if len(draft.content.strip()) < mc: raise ValidationError(f'content 부족 최소{mc}자')
    for p in FORBIDDEN:
        if p in draft.content: raise ValidationError(f'금지표현:{p}')
    return draft
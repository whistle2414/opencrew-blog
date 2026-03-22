from types.blog import BlogPostDraft, LENGTH_MAP
FORBIDDEN = ['AI가 작성했습니다','ChatGPT','인공지능이 쓴','이 글은 자동으로']
class ValidationError(Exception): pass
def validate_post(draft: BlogPostDraft, length: str = 'medium') -> BlogPostDraft:
    if not draft.title or len(draft.title.strip()) < 5:
        raise ValidationError('title 오류: 최소 5자 이상의 제목을 작성하세요.')
    if len(draft.title.strip()) > 200:
        raise ValidationError(f'title이 200자 초과({len(draft.title.strip())}자). 줄여주세요.')
    mc = LENGTH_MAP.get(length, 600)
    actual = len(draft.content.strip())
    if actual < mc:
        raise ValidationError(f'content 부족: {actual}자/{mc}자. {mc-actual}자 더 추가하세요.')
    found = [p for p in FORBIDDEN if p in draft.content]
    if found:
        raise ValidationError(f'금지 표현 포함: {found}. 해당 표현을 제거하세요.')
    return draft

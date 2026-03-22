from crewai import Agent, Task, Crew
from types.blog import BlogPostInput, BlogPostResult
from prompts.blog_writer_prompt import build_blog_prompt
from services.llm_provider import get_llm, parse_blog_response
from validators.post_validator import validate_post, ValidationError
from adapters.mcp.save_post import save_post_via_mcp, MCPSaveError

MAX_RETRY = 1

def run_blog_create_and_save(input: BlogPostInput) -> BlogPostResult:
    print(f'\n[workflow] 시작 - topic: {input.topic}')
    retry_hint = None
    for attempt in range(1, MAX_RETRY + 2):
        if attempt > 1:
            print(f'[workflow] 재시도 {attempt-1}회차...')
        raw = _generate(input, retry_hint)
        try:
            draft = parse_blog_response(raw, input.topic)
            print(f'[workflow] 파싱 성공: {draft.title}')
        except ValueError as e:
            print(f'[workflow] 파싱 실패: {e}')
            if attempt <= MAX_RETRY:
                retry_hint = f'이전 응답이 JSON 형식이 아님. 반드시 순수 JSON만 출력. 오류: {e}'
                continue
            return BlogPostResult(success=False, error=f'파싱 실패({MAX_RETRY}회 후): {e}')
        try:
            validate_post(draft, length=input.length)
            print('[workflow] 검증 통과')
        except ValidationError as e:
            print(f'[workflow] 검증 실패: {e}')
            if attempt <= MAX_RETRY:
                retry_hint = f'이전 응답 검증 실패. 수정 필요: {e}'
                continue
            return BlogPostResult(success=False, error=f'검증 실패({MAX_RETRY}회 후): {e}')
        retry_hint = None
        break
    try:
        result = save_post_via_mcp(draft, input)
        print(f'[workflow] 저장 완료: {result}')
    except MCPSaveError as e:
        return BlogPostResult(success=False, error=f'MCP 저장 오류(재시도없음): {e}')
    return BlogPostResult(success=True, title=draft.title, content_preview=draft.content[:100])

def _generate(input: BlogPostInput, retry_hint: str = None) -> str:
    base = build_blog_prompt(input)
    prompt = f'[재시도]\n{retry_hint}\n\n{base}' if retry_hint else base
    agent = Agent(role='블로그작가', goal=f'{input.topic} JSON작성', backstory='10년경력', llm=get_llm(), verbose=False)
    task = Task(description=prompt, expected_output='순수JSON {title,content}', agent=agent)
    print(f'[workflow] Claude 호출 (hint:{"있음" if retry_hint else "없음"})')
    return str(Crew(agents=[agent], tasks=[task], verbose=False).kickoff())

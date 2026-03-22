from crewai import Agent, Task, Crew
from types.blog import BlogPostInput, BlogPostResult
from prompts.blog_writer_prompt import build_blog_prompt
from services.llm_provider import get_llm, parse_blog_response
from validators.post_validator import validate_post, ValidationError
from adapters.mcp.save_post import save_post_via_mcp, MCPSaveError
def run_blog_create_and_save(input):
    print(f'[workflow] 시작:{input.topic}')
    agent = Agent(role='블로그작가', goal=f'{input.topic} JSON작성', backstory='10년경력', llm=get_llm(), verbose=False)
    task = Task(description=build_blog_prompt(input), expected_output='순수JSON', agent=agent)
    raw = str(Crew(agents=[agent], tasks=[task], verbose=False).kickoff())
    try: draft = parse_blog_response(raw, input.topic)
    except ValueError as e: return BlogPostResult(success=False, error=f'파싱:{e}')
    try: validate_post(draft, length=input.length)
    except ValidationError as e: return BlogPostResult(success=False, error=f'검증:{e}')
    try: r = save_post_via_mcp(draft, input)
    except MCPSaveError as e: return BlogPostResult(success=False, error=f'저장:{e}')
    return BlogPostResult(success=True, title=draft.title, content_preview=draft.content[:100])
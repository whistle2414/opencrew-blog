"""
batch_runner.py

topics.txt 파일에서 주제 목록을 읽어
순서대로 블로그 글을 자동 생성하고 저장한다.

사용법:
  python batch_runner.py                    # topics.txt 사용
  python batch_runner.py --file my_list.txt # 다른 파일 지정
  python batch_runner.py --dry-run          # 실제 생성 없이 목록만 확인
  python batch_runner.py --delay 30         # 글 사이 대기 시간(초) 지정

topics.txt 형식:
  # 주석은 무시됨
  다이어트 방법
  홈트레이닝 루틴
  건강한 식단 만들기
"""

import argparse
import time
import sys
from datetime import datetime
from pathlib import Path

from types.blog import BlogPostInput
from openclaw.intent_router import IntentRouter


def load_topics(filepath: str) -> list[str]:
    path = Path(filepath)
    if not path.exists():
        print(f"[batch] 파일을 찾을 수 없습니다: {filepath}")
        sys.exit(1)
    topics = []
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            topics.append(line)
    return topics


def run_batch(topics: list[str], tone: str, length: str, delay: int, dry_run: bool):
    total = len(topics)
    ok = 0
    fail = 0
    results = []

    print(f"\n{'='*54}")
    print(f"  OpenCrew 배치 생성 시작")
    print(f"  총 {total}개 주제 | tone={tone} | length={length}")
    if dry_run:
        print(f"  [DRY RUN 모드 - 실제 생성 안 함]")
    print(f"{'='*54}\n")

    for i, topic in enumerate(topics, 1):
        print(f"[{i}/{total}] 주제: '{topic}'")

        if dry_run:
            print(f"  → DRY RUN: 건너뜀\n")
            continue

        req = {
            'topic': topic,
            'tone': tone,
            'length': length,
            'intent': 'workflow',
            'workflow': 'blog_create_and_save',
        }

        start = datetime.now()
        try:
            result = IntentRouter().dispatch(req)
            elapsed = (datetime.now() - start).seconds

            if result.get('success'):
                ok += 1
                print(f"  ✅ 성공 ({elapsed}초) | 제목: {result.get('title')}")
                results.append({'topic': topic, 'status': 'ok', 'title': result.get('title')})
            else:
                fail += 1
                print(f"  ❌ 실패 | 오류: {result.get('error')}")
                results.append({'topic': topic, 'status': 'fail', 'error': result.get('error')})

        except Exception as e:
            fail += 1
            print(f"  ❌ 예외 발생: {e}")
            results.append({'topic': topic, 'status': 'fail', 'error': str(e)})

        if i < total:
            print(f"  [{delay}초 대기 중...]\n")
            time.sleep(delay)

    # 결과 요약
    print(f"\n{'='*54}")
    print(f"  배치 완료: 성공 {ok}개 / 실패 {fail}개 / 전체 {total}개")
    print(f"{'='*54}")

    # 실패 항목 출력
    failed = [r for r in results if r['status'] == 'fail']
    if failed:
        print(f"\n실패 항목 재확인:")
        for r in failed:
            print(f"  - {r['topic']}: {r.get('error','')}")

    return ok, fail


def main():
    p = argparse.ArgumentParser(description='OpenCrew 배치 글 생성')
    p.add_argument('--file',    default='topics.txt',   help='주제 목록 파일 (기본: topics.txt)')
    p.add_argument('--tone',    default='informative',  choices=['informative','casual','professional'])
    p.add_argument('--length',  default='medium',       choices=['short','medium','long'])
    p.add_argument('--delay',   default=10, type=int,   help='글 사이 대기 시간(초) 기본: 10')
    p.add_argument('--dry-run', action='store_true',    help='실제 생성 없이 목록만 확인')
    args = p.parse_args()

    topics = load_topics(args.file)
    if not topics:
        print('[batch] 주제 목록이 비어 있습니다.')
        sys.exit(1)

    print(f'[batch] {len(topics)}개 주제 로드 완료: {args.file}')
    for i, t in enumerate(topics, 1):
        print(f'  {i}. {t}')

    run_batch(topics, args.tone, args.length, args.delay, args.dry_run)


if __name__ == '__main__':
    main()

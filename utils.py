import re

def parse_thinking(content: str) -> tuple[str, str]:
    match = re.search(f'<think>(.*)</think>', content)

    if not match:
        print('No match!')
        return '', content

    thinking_str = match.group(0)
    print('Match!')
    return thinking_str, content.split('</think>')[1]

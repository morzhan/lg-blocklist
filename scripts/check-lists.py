#!/usr/bin/env python3
"""Validate the exact-domain lists before publishing them."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
FILES = (
    '01-ads-and-telemetry.txt',
    '02-optional-lg-services.txt',
    '03-optional-clock-sensitive.txt',
)
LABEL = re.compile(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\Z')
CLOCK = re.compile(r'(^|\.)(nextlgsdp\.com|tv\.wiselg\.com)\Z')


def main():
    errors = []
    seen = {}
    total = 0
    for filename in FILES:
        path = ROOT / filename
        try:
            text = path.read_bytes().decode('ascii')
        except (OSError, UnicodeError) as error:
            errors.append(f'{filename}: {error}')
            continue
        names = text.splitlines()
        if not names:
            errors.append(f'{filename}: list is empty')
        if not text.endswith('\n') or '\r' in text:
            errors.append(f'{filename}: use LF line endings and a final newline')
        if names != sorted(names):
            errors.append(f'{filename}: domains must be sorted')
        for line, domain in enumerate(names, 1):
            location = f'{filename}:{line}'
            labels = domain.split('.')
            if len(domain) > 253 or len(labels) < 2 or not all(LABEL.fullmatch(label) for label in labels) or labels[-1].isdigit():
                errors.append(f'{location}: invalid exact domain {domain!r}')
            if domain in seen:
                errors.append(f'{location}: duplicate of {seen[domain]}: {domain}')
            else:
                seen[domain] = location
            if CLOCK.search(domain) and filename != FILES[2]:
                errors.append(f'{location}: known clock-sensitive name belongs in {FILES[2]}')
            if filename == FILES[2] and not CLOCK.search(domain):
                errors.append(f'{location}: document any new clock family and extend the validator before adding it')
        total += len(names)
        print(f'{filename}: {len(names)} domains')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Validated {total} domains across {len(FILES)} lists.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

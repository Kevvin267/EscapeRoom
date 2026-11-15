"""Probe the real V2 schema, saving settings only after a valid response."""
import argparse
import os
from dotenv import load_dotenv, set_key
from escape_room.llm import ModelUnavailable
from escape_room.v2 import propose


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', required=True)
    parser.add_argument('--provider', choices=['gemini', 'groq'], default='gemini')
    parser.add_argument('--transport', choices=['interactions', 'generate_content'],
                        default='interactions')
    args = parser.parse_args()
    load_dotenv(override=True)
    os.environ['LLM_PROVIDER'] = args.provider
    os.environ[args.provider.upper() + '_MODEL'] = args.model
    os.environ['GEMINI_TRANSPORT'] = args.transport
    print('Testing actual game parser; allow up to 60 seconds.', flush=True)
    try:
        action = propose('examine bookshelf', online=True)
        if (action.verb, action.target, action.value) != ('examine', 'bookshelf', ''):
            print('FAILED: unexpected action. Settings unchanged.')
            return 1
    except ModelUnavailable as error:
        print(str(error))
        print('FAILED: settings unchanged.')
        return 1
    set_key('.env', args.provider.upper() + '_MODEL', args.model)
    if args.provider == 'gemini':
        set_key('.env', 'GEMINI_TRANSPORT', args.transport)
    set_key('.env', 'LLM_PROVIDER', args.provider)
    print('SUCCESS: real game parser worked. Settings saved; restart Streamlit.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

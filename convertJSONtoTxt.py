import json
from dateutil import parser

def format_event(event):
    # Parse timestamp with timezone support
    dt = parser.isoparse(event.get('created_at', ''))
    timestamp = int(dt.timestamp())
    date_str = dt.strftime('%Y-%m-%d')

    # Author info
    author_email = 'konstantinos.tzanakis@tum.de'

    # Action
    action = event.get('action_name', '').strip()
    if action == 'joined':
        return None

    # Target info (branch name, title, etc.)
    target_type = event.get('target_type')
    push_data = event.get('push_data', {})
    ref = push_data.get('ref', '')
    target_title = event.get('target_title')
    commit_title = push_data.get('commit_title', '')

    # Construct event action text
    if (target_type != 'WikiPage::Meta'):
        if(target_type is None or target_type=='null'):
            action = f"{action} branch '{ref}'"  
            desc = commit_title if commit_title else "-"
            return f"{timestamp} | {author_email} | {date_str} | {action} | {desc}"
        else:
           action = f"{action} branch '{target_title}'"  
           desc = target_type
           return f"{timestamp} | {author_email} | {date_str} | {action} | {desc}"
    else:
        return None

# Load events
with open('ktzan_contributions.json', 'r') as f:
    events = json.load(f)

# Print formatted output
with open('ktzan_contributions.txt', 'w') as outfile:
    for event in events:
        formatted_line = format_event(event)
        if formatted_line is not None:
            outfile.write(formatted_line + '\n')

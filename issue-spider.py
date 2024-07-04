import requests
import pandas as pd
import toml
import re

# 从 env.toml 文件中读取配置
config = toml.load('env.toml')
TOKEN = config['github']['token']
REPO = config['github']['repo']

def get_issues(repo, state='open', labels=None):
    url = f'https://api.github.com/repos/{repo}/issues'
    headers = {'Authorization': f'token {TOKEN}'}
    params = {'state': state, 'labels': labels, 'per_page': 100}
    issues = []

    while url:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        issues.extend(response.json())
        url = response.links.get('next', {}).get('url')

    return issues

def get_comments(issue_url):
    headers = {'Authorization': f'token {TOKEN}'}
    comments = []

    response = requests.get(issue_url, headers=headers)
    response.raise_for_status()
    comments.extend(response.json())

    return comments

def classify_issues_by_labels(issues):
    label_dict = {}
    for issue in issues:
        labels = [label['name'] for label in issue.get('labels', [])]
        comments = get_comments(issue['comments_url'])
        if not labels:
            labels = ['No Label']
        for label in labels:
            if label not in label_dict:
                label_dict[label] = []
            label_dict[label].append({
                'image': extract_image_name(issue['title']),
                'number': issue['number'],
                'url': issue['html_url'],
                'comments': comments,
                'label': label
            })
    return label_dict

def extract_image_name(title):
    match = re.search(r'\[.*?\] Board image (.*?) need update', title)
    return match.group(1) if match else title

def determine_update_status(label):
    if label == 'packages-index-update':
        return 'Yes'
    elif label == 'packages-index-wait':
        return 'No'
    elif label == 'No Label':
        return 'No Label, Unknown'
    else:
        return 'Unknown'

issues = get_issues(REPO)
classified_issues = classify_issues_by_labels(issues)

# 输出分类结果
for label, issues in classified_issues.items():
    print(f'\nLabel: {label}')
    for issue in issues:
        print(f"- {issue['image']} (# {issue['number']})")
        for comment in issue['comments']:
            print(f"  - Comment by {comment['user']['login']}: {comment['body']}")

# 如果需要将结果保存为 CSV 文件
data = []
for label, issues in classified_issues.items():
    for issue in issues:
        comments = "\n".join([f"{comment['user']['login']}: {comment['body']}" for comment in issue['comments']])
        update_status = determine_update_status(issue['label'])
        data.append([issue['image'], issue['number'], issue['url'], comments, update_status])

df = pd.DataFrame(data, columns=['Image', 'Number', 'URL', 'Comments', 'Need Update'])
df.to_csv('classified_issues_with_comments.csv', index=False)

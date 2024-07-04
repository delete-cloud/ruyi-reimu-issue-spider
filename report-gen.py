import pandas as pd

# 读取生成的 CSV 文件
df = pd.read_csv('classified_issues_with_comments.csv')

# 创建汇总文档内容
summary_content = "# ruyi device provision功能镜像版本更新情况汇总\n\n"
summary_content += "本文档总结了ruyi-reimu仓库下的镜像版本更新情况。\n\n"

# 添加子标题
summary_content += "## 需要更新的镜像版本\n\n"
needs_update = df[df['Need Update'] == 'Yes']
for index, row in needs_update.iterrows():
    summary_content += f"### 问题 #{row['Number']}\n"
    summary_content += f"- **镜像名称**: {row['Image']}\n"
    summary_content += f"- **链接**: [Issue Link]({row['URL']})\n"
    summary_content += f"- **是否需要更新**: {row['Need Update']}\n"
    summary_content += f"- **评论**:\n"
    for comment in row['Comments'].split('\n'):
        summary_content += f"  - {comment}\n"
    summary_content += "\n"

summary_content += "## 不需要更新的镜像版本\n\n"
no_update = df[df['Need Update'] == 'No']
for index, row in no_update.iterrows():
    summary_content += f"### 问题 #{row['Number']}\n"
    summary_content += f"- **镜像名称**: {row['Image']}\n"
    summary_content += f"- **链接**: [Issue Link]({row['URL']})\n"
    summary_content += f"- **是否需要更新**: {row['Need Update']}\n"
    summary_content += f"- **评论**:\n"
    for comment in row['Comments'].split('\n'):
        summary_content += f"  - {comment}\n"
    summary_content += "\n"

summary_content += "## 未知更新状态的镜像版本\n\n"
unknown_update = df[df['Need Update'].isin(['No Label, Unknown', 'Unknown'])]
for index, row in unknown_update.iterrows():
    summary_content += f"### 问题 #{row['Number']}\n"
    summary_content += f"- **镜像名称**: {row['Image']}\n"
    summary_content += f"- **链接**: [Issue Link]({row['URL']})\n"
    summary_content += f"- **是否需要更新**: {row['Need Update']}\n"
    summary_content += f"- **评论**:\n"
    for comment in row['Comments'].split('\n'):
        summary_content += f"  - {comment}\n"
    summary_content += "\n"

# 将汇总内容写入文档
with open('镜像版本更新情况汇总.md', 'w', encoding='utf-8') as file:
    file.write(summary_content)

print("汇总文档已成功创建。")

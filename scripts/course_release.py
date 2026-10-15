"""公开下载入口与限期分享配置；不保存解压密码。"""
REPOSITORY = 'wybert/social-media-analysis-tutorials'
RELEASE_TAG = 'classroom-2026-10'
ARCHIVE_NAME = 'social-media-analysis-classroom-2026-10-16.zip'
ARCHIVE_URL = f'https://github.com/{REPOSITORY}/releases/download/{RELEASE_TAG}/{ARCHIVE_NAME}'
EXPIRES_AT = '2026-10-25T23:59:59+08:00'


def write_expiry_workflow(root):
    workflow = root / '.github/workflows/expire-classroom-download.yml'
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text('''name: Expire encrypted classroom download
on:
  schedule:
    # UTC 16:00 = 北京时间次日00:00；队列调度可能延迟。
    - cron: '0 16 * * *'
  workflow_dispatch:
permissions:
  contents: write
jobs:
  expire:
    runs-on: ubuntu-latest
    env:
      GH_TOKEN: ${{ github.token }}
      GH_REPO: ''' + REPOSITORY + '''
    steps:
      - name: Remove the encrypted asset after the sharing deadline
        shell: bash
        run: |
          set -euo pipefail
          cutoff=$(date -u -d '2026-10-25T15:59:59Z' +%s)
          if [ "$(date -u +%s)" -le "$cutoff" ]; then
            echo 'The classroom sharing window is still open.'
            exit 0
          fi
          asset=$(gh release view ''' + RELEASE_TAG + ''' --json assets --jq '.assets[] | select(.name == "''' + ARCHIVE_NAME + '''") | .name')
          if [ -n "$asset" ]; then
            gh release delete-asset ''' + RELEASE_TAG + ''' "$asset" --yes
            echo 'Encrypted classroom download removed.'
          else
            echo 'No encrypted classroom asset remains.'
          fi
''', encoding='utf-8')

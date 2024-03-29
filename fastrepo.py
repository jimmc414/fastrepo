import os
import requests
from subprocess import check_call, check_output, CalledProcessError, STDOUT

def is_git_repo(path='.'):
    try:
        check_output(['git', '-C', path, 'status'], stderr=STDOUT)
        return True
    except CalledProcessError:
        return False

# Get the current folder name to use as the repository name
current_directory = os.path.basename(os.path.normpath(os.getcwd()))
NEW_REPO_NAME = current_directory

# Check if the current directory is a git repository
if is_git_repo():
    proceed = input("This directory is already a Git repository. Do you want to continue? [y/N]: ")
    if proceed.lower() != 'y':
        print("Operation cancelled by the user.")
        exit()

# Prompt for a repository description
repo_description = input("Enter an optional description for the repository (press enter to skip): ")

# Retrieve your GitHub Personal Access Token from the environment
GITHUB_TOKEN = os.getenv('GITHUB_REPO_TOKEN')

# The GitHub API endpoint for creating a repository
url = f'https://api.github.com/user/repos'

headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}

data = {
    'name': NEW_REPO_NAME,
    'description': repo_description,
    'private': False  # Set to True if you want a private repository
}

# Create the .gitignore file with specified contents, including .csv and .xlsx
gitignore_contents = """
# Outputs
*_output.txt
output.txt

# Data files
*.csv
*.xlsx

# Env
.env

# Editors
.project
.settings
.springBeans
**/.favorites.json
**/.idea
**/.vscode
**/*.Session.vim
**/*.sw[a-z]
**/*.vim
**/*.zwc
**/*~

# OS generated files
**/._*
**/.AppleDouble
**/.dropbox
**/.dropbox.attr
**/.dropbox.cache
**/.DS_Store
**/.DS_STORE
**/.lnk
**/.LSOverride
**/$RECYCLE.BIN/
**/Desktop.ini
**/ehthumbs.db
**/Thumbs.db

# Files that might appear in the root of a volume
**/.com.apple.timemachine.donotpresent
**/.DocumentRevisions-V100
**/.fseventsd
**/.Spotlight-V100
**/.TemporaryItems
**/.Trashes
**/.VolumeIcon.icns

# Directories potentially created on remote AFP share
**/.apdisk
**/.AppleDB
**/.AppleDesktop
**/Network Trash Folder
**/Temporary Items

# Temp files
**/.temp
**/.tmp
tmp/

# Files that commonly contain secrets
**/*.key
**/*.pem
**/*.pfx
**/*.p12
**/*.jks
**/*.keystore
**/*.pkcs12
**/*.pkcs8
**/*.pkpass
**/*.secrets

# Logs
**/*.log

# Build directories
**/_build/
**/dist
build/
out/
target/

# Python
__pycache__/
__pypackages__/
.ipynb_checkpoints
*$py.class
celerybeat-schedule
develop-eggs/
dmypy.json
eggs/
ipython_config.py
local_settings.py
pip-delete-this-directory.txt
pip-log.txt
pip-wheel-metadata/
venv
"""

with open('.gitignore', 'w') as gitignore_file:
    gitignore_file.write(gitignore_contents)

# Additionally, create a LICENSE file with the provided contents
license_contents = """
MIT License

Copyright (c) 2024 Jim McMillan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

with open('LICENSE', 'w') as license_file:
    license_file.write(license_contents)

# Create a new repository on GitHub
response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    print(f'Repository {NEW_REPO_NAME} created successfully.')
    repo_https_url = response.json()['clone_url']

    # Initialize local Git repository, add files, and commit
    check_call(['git', 'init'])
    check_call(['git', 'add', '.'])
    check_call(['git', 'commit', '-m', 'Initial commit'])

    # Add the remote GitHub repository and push
    check_call(['git', 'remote', 'add', 'origin', repo_https_url])
    check_call(['git', 'push', '-u', 'origin', 'master'])
else:
    print('Failed to create repository. Response:', response.text)

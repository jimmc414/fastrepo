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

# Create the .gitignore file with specified contents
gitignore_contents = """
# Outputs
*_output.txt
output.txt

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
**/.dccache
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
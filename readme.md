# fastrepo.py

FastRepo is a Python script that automates the creation of a new GitHub repository and commits the current directory's contents to it without user intervention.

## Features

- Creates a new GitHub repository with the current directory's name.
- Adds all files in the current directory to the new repository.
- Commits the files to the repository.
- Configurable to use either HTTPS or SSH.

## Usage

To use FastRepo, run the script in the directory you want to upload:

```bash
python fastrepo.py
```

## Obtaining a GitHub Personal Access Token

A GitHub Personal Access Token (PAT) is required to authenticate with the GitHub API and access private repositories. Follow these steps to generate a token:

Log in to your GitHub account and navigate to the Settings page by clicking on your profile picture in the top-right corner and selecting Settings.

In the left sidebar, click on Developer settings.

Click on Personal access tokens in the left sidebar.

Click the Generate new token button.

Enter a name for the token in the Note field (e.g., "Repo-Prep").

Select the appropriate scopes for the token. For the fastrepo.py script, the minimum required scope is repo (which grants full control of private repositories). You may need to select additional scopes depending on your use case.

Click the Generate token button at the bottom of the page.

In the fastrepo.py script, replace the GITHUB_REPO_TOKEN placeholder with your actual token or add to the %GITHUB_REPO_TOKEN% env variable as detailed to automatically pull it from your environment.

- Add Github Personal Access Token to environment variable GITHUB_REPO_TOKEN
  - Windows:

      ```shell
      setx GITHUB_REPO_TOKEN "YourGitHubToken"
      ```

  - Linux:

      ```shell
      echo 'export GITHUB_REPO_TOKEN="YourGitHubToken"' >> ~/.bashrc
      source ~/.bashrc
      ```
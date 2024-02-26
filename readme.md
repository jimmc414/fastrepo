# fastrepo.py

FastRepo is a Python script that automates the creation of a new GitHub repository and commits the current directory's contents to it, including the setup of a `.gitignore` and a `LICENSE` file without user intervention.

## Features

- Creates a new GitHub repository with the current directory's name.
- Adds all files in the current directory to the new repository, excluding specified files in `.gitignore`.
- Automatically generates a `.gitignore` file that excludes patterns such as `*.csv`, `*.xlsx`, environment files, and more, ensuring sensitive or unnecessary files are not committed.
- Includes a `LICENSE` file with a predefined MIT license in the repository.
- Commits the files to the repository.
- Configurable to use either HTTPS or SSH.

## Usage

To use FastRepo, run the script in the directory you want to upload:

```bash
python fastrepo.py
```

## Preparations

Before running `fastrepo.py`, ensure:

- A GitHub Personal Access Token (PAT) is obtained and set in your environment as `GITHUB_REPO_TOKEN`.
- You have decided whether to include `.csv` and `.xlsx` files in your project. By default, these files are ignored to prevent accidental upload of potentially sensitive data.

## Obtaining a GitHub Personal Access Token

A GitHub Personal Access Token (PAT) is required to authenticate with the GitHub API and access private repositories. Follow these steps to generate a token:

1. Log in to your GitHub account and navigate to the Settings page by clicking on your profile picture in the top-right corner and selecting Settings.
2. In the left sidebar, click on Developer settings.
3. Click on Personal access tokens in the left sidebar.
4. Click the Generate new token button.
5. Enter a name for the token in the Note field (e.g., "Repo-Prep").
6. Select the appropriate scopes for the token. For the `fastrepo.py` script, the minimum required scope is `repo` (which grants full control of private repositories). You may need to select additional scopes depending on your use case.
7. Click the Generate token button at the bottom of the page.

In the `fastrepo.py` script, replace the `GITHUB_REPO_TOKEN` placeholder with your actual token or add it to the `GITHUB_REPO_TOKEN` environment variable as detailed to automatically pull it from your environment.

- **Add GitHub Personal Access Token to environment variable `GITHUB_REPO_TOKEN`**
  - Windows:

    ```shell
    setx GITHUB_REPO_TOKEN "YourGitHubToken"
    ```

  - Linux:

    ```shell
    echo 'export GITHUB_REPO_TOKEN="YourGitHubToken"' >> ~/.bashrc
    source ~/.bashrc
    ```

This ensures that your script can authenticate with GitHub to create the repository and push the initial commit.
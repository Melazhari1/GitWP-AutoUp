import subprocess
import os

class GitApp:
    def __init__(self, repo_path):
        self.repo_path = repo_path

    def run_git_command(self, command):
        try:
            result = subprocess.run(command, cwd=self.repo_path, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr

    def initialize_repo(self):
        if not os.path.exists(self.repo_path):
            os.makedirs(self.repo_path)
        result = self.run_git_command(['git', 'init'])
        print(result)

    def add_file(self, filename, content):
        filepath = os.path.join(self.repo_path, filename)
        with open(filepath, 'w') as file:
            file.write(content)
        result = self.run_git_command(['git', 'add', filename])
        print(result)

    def commit_changes(self, message):
        result = self.run_git_command(['git', 'commit', '-m', message])
         #print(result)

    def get_status(self):
        result = self.run_git_command(['git', 'status'])
        print(result)

    def add_all(self):
        result = self.run_git_command(['git', 'add', '--all'])
        print(result)

    def create_and_checkout_branch(self, branch_name):
        result = self.run_git_command(['git', 'checkout', '-b', branch_name])
        print(result)

    def is_current_branch(self, branch_name):
        result = self.run_git_command(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        return result == branch_name

    def checkout_branch(self, branch_name):
        result = self.run_git_command(['git', 'checkout', branch_name])
        print(result)

    def branch_exists(self, branch_name):
        result = self.run_git_command(['git', 'branch', '--list', branch_name])
        return bool(result)
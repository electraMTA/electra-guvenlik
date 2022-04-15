from github import Github
import base64

def get_blob_content(repo, branch, path_name):
    ref = repo.get_git_ref(f'heads/{branch}')
    tree = repo.get_git_tree(ref.object.sha, recursive='/' in path_name).tree
    sha = [x.sha for x in tree if x.path == path_name]
    if not sha:
        return None
    return repo.get_git_blob(sha[0])

TOKEN = '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'
git = Github(TOKEN)
user = git.get_user()
org = git.get_organization('electraMTA')
backupRepo = org.get_repo('electrabackups')
target = 'veriyedekleri/core-14.04.2022|16.56.sql'

contents = get_blob_content(backupRepo, 'main', target).encoding
print(contents)

backupRepo.delete_file(target, 'delete automation', target, 'main')
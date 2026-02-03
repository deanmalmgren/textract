```sh
# Add upstream remote and fetch
git remote add upstream https://github.com/deanmalmgren/textract.git
git fetch upstream

# sync my fork's main branch with upstream master
gh repo sync -b main --source deanmalmgren/textract
```

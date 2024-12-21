# ase_charging_station_part_2

### Hints how to use git:
#### Cloning a repository:
`git clone \<name of the repo\>`

#### Get the updates that happened on the repo
`git pull`

#### Adding stuff to git
`git add \<file-name\>`
`git add -u` add everything that was changed

#### Undo add
`git reset \<file-name\>` or
`git reset` reset everything you planned to add so far

#### Show adding / reset status
`git status`

#### Stage a version of your files
`git commit`
`git commit -m "text of the commit message"`
`git commit -m "text of the commit message" -m "more deeply description"`
`git commit --amend --no-edit` if you made a small mistake with you last commit and want to fix it
you can use `--amend` to change the last commit and add `--no-edit` if you want to keep the old commit
message

#### Pushing the commit online to github
`git push`
`git push --force` is needed if you overwrite something you already pushed

#### Creating your branch
`git branch \<branch_name\>`
Switch to the branch
`git checkout \<branch_name\>`

#### Getting updates of other group members
`git pull` to get updates of the branch you are currently working on
`git fetch --all --prune` to update everything

#### Putting your own branch on the newest version of another branch
`git rebase \<branch_name\>`
`git rebase main` you probably want to rebase on main...

#### In case of rebase/merge conflict
First: resolving the conflict in the editor and saving the file
`git add` of the file to stage the changes
`git rebase --continue`
`git merge --continue`
And then you have to type a new commit message.

#### Showing a list of all commits on your branch
`git log`
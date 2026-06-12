$repoUrl = "https://github.com/argovalex/skipper-quiz.git"
git init
git add .
git commit -m "initial: skipper quiz bot"
git remote add origin $repoUrl
git branch -M main
git push -u origin main

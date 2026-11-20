# GitHub submission steps (run locally)

These commands create the requested repository and branch/PR workflow. GitHub login and remote URL are personal, so replace the URL with your own repository URL.


```bash
git init
git add README.md .gitignore requirements.txt
 git commit -m "Add project setup and documentation"
git branch -M main
git checkout -b feature/analysis
git add data/employees.csv data/departments.csv data/employees_with_issues.csv
git commit -m "Add employee and department sample datasets"
git add src/assessment.py
git commit -m "Implement Python core and employee analysis"
git add notebooks/week1_analysis.ipynb
git commit -m "Add notebook analysis walkthrough"
git add reports/
git commit -m "Add generated charts and submission notes"
git add data/employees.json data/high_earners.csv data/users.json data/employees_cleaned.csv
git commit -m "Add generated data exports"
git push -u origin feature/analysis
```

Create the PR on GitHub from `feature/analysis` into `main`, then merge it. To practice a deliberate README conflict on a disposable branch, edit the same README heading separately on `main` and `feature/analysis`, commit both edits, then merge main into the feature branch and resolve the conflict manually. Do not do this on important work without a backup.

After merging, run `git log --oneline --graph --decorate` and capture a screenshot. GitHub repository and PR links must be created by you using your account; this project does not fabricate links or claim a push/merge happened.

Required terminal demonstrations:
```bash
mkdir -p data notebooks reports src
cp data/employees.csv data/employees_backup.csv
mv data/employees_backup.csv data/employees.csv
 grep -n "Chennai" data/employees.csv
jupyter nbconvert --to script notebooks/week1_analysis.ipynb --output week1_analysis.py --output-dir notebooks
```

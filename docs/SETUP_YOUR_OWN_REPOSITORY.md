# Set up your own repository (do this first)

**You submit your own repository, not ours.** The organizers' starter repository is read-only: you cannot push to it, and you should not try. Instead, each team creates a **new repository of its own**, copies the starter files into it, and works there. The link to *your* repository is what you submit.

## Step 1. Create an empty repository

On GitHub (or GitLab), one team member creates a **new, empty repository** under their own account or organization.

* Name it something like `rush-hour-<team-name>`.
* Choose **Private**, unless the organizers ask for public.
* Do **not** tick "Add a README", ".gitignore", or "license". Leave it empty.

## Step 2. Copy the starter into it

Pick one way. All three give you the same result: a repository you own, with the starter files in it.

**A. From the ZIP (works for everyone)**

```bash
# unzip rush_hour_team_repo.zip, then:
cd rush_hour_team_repo
git init -b main
git add .
git commit -m "Start from the RUSH HOUR starter"
git remote add origin https://github.com/<your-account>/<your-repo>.git
git push -u origin main
```

**B. "Use this template" (if the organizers published the starter as a template repository)**

Open the organizers' starter page on GitHub and click **Use this template**, then **Create a new repository**. GitHub creates your own copy with the files already in it. Clone your copy and work there.

**C. Clone the starter, then point it at your repository**

```bash
git clone <organizers-starter-url> my-team-repo
cd my-team-repo
git remote remove origin
git remote add origin https://github.com/<your-account>/<your-repo>.git
git push -u origin main
```

If a push ever says "permission denied" and the address is the organizers' repository, you are pointing at the wrong remote. Run `git remote -v` and check that `origin` is *your* repository.

## Step 3. Work in your repository

Everyone on the team clones **your** repository, commits, and pushes to it. Add your teammates as collaborators so they can push (Settings, then Collaborators).

## Step 4. Give the organizers access

* **Private repository:** add the organizer account you are told to use as a collaborator with **Read** access. Without this, the judges cannot see your work.
* **Public repository:** nothing to do, but remember that anyone can see it.

## Step 5. Submit

Before the deadline:

1. Run `python code/export_results.py` and `python code/check_submission.py`, and fix every `FAIL`.
2. Tick `SUBMISSION_CHECKLIST.md`.
3. Push your final commit.
4. Send the organizers **the link to your repository and the commit hash or tag** you are submitting (`git rev-parse HEAD` prints the hash).

Judges score the commit you name, so do not push changes you do not want judged after you submit.

## If the organizers fix something in the starter

The starter may be updated during the event (for example a bug fix). Your repository does not change by itself. The organizers will announce any update, and you copy the changed files into your repository by hand. Never replace the files in `data/`: your results depend on them.

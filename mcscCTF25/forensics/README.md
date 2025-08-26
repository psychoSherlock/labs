# Ithihas - Forensics Challenge

## Challenge Description

He calls himself PsychoSherlock — a self-proclaimed genius with an unhealthy obsession for mysteries and computers. After binge-watching crime thrillers and Mr. Robot for years, he decided coding was his ticket to glory. His dream? To infiltrate the legendary halls of MITS, master the art of algorithms, and someday become the CEO of the biggest tech empire in history. Armed with ambition, overconfidence, and a questionable sleep schedule, he's ready to prove himself. But the question remains… is he truly worthy? He's convinced his blogs are flawless… which is adorable, because they're not. Can you find out his mistake?

## Challenge Details

- **Difficulty**: Medium
- **Category**: Digital Forensics
- **Skills Required**: Git Forensics, Branch Analysis, Web Development

## Files Provided

- [`itihas.zip`](./itihas.zip) - Archive containing the blog project

## Hints

Why did he share the project in a zip file? He could have shared the website link. What if there's something hidden that you don't see yet? A tree with branches.

## Solution

<details>
<summary>Click to reveal solution</summary>

### Analysis Approach

1. The challenge involves a Git repository hidden within the zip file
2. After extracting the zip, initialize or examine the Git repository
3. The flag is split into two parts across different Git features

### Part 1: Examining Git History

The first part of the flag can be found by examining the Git commit history and tree:

```bash
# Navigate to the extracted directory
cd itihas

# View the Git commit history tree
git log --graph --oneline --all

# This reveals a removed blog post about a command sent by "Hacker Guy"
# The command's second part contains the first half of the flag: "tr33s_"
```

### Part 2: Checking Other Branches

The second part of the flag is hidden in a different branch:

```bash
# List all branches in the repository
git branch -a

# Switch to the "newWebsite" branch
git checkout newWebsite

# Examine the JavaScript files in this branch to find the second half of the flag: "4nd_br4nch3s"
```

### Combining the Flag

Putting both parts together gives us the complete flag: `mcsc{tr33s_4nd_br4nch3s}`

</details>

## Flag

`mcsc{tr33s_4nd_br4nch3s}`

## Author

Created by [psychoSherlock](https://github.com/psychoSherlock)

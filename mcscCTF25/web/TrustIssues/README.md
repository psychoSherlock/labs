<!-- filepath: /home/psychosherlock/Desktop/projects/labs/mcscCTF25/web/TrustIssues/README.md -->

## TrustIssues

- **Difficulty**: Easy
- **Category**: Web
- **Skills Required**: JavaScript Analysis, Web Reconnaissance, Client-side Security

The enemy left behind a portal that looks like a login screen… but something feels off. Your mission is to infiltrate it. Don’t just trust what you see on the surface. Gain access, step through the portal, and follow the trail. But beware, not everything beyond is what it seems…

## Files Provided

- [Live Challenge Portal](http://challenges.mcsc.space:9090/)
- [`index.html`](./index.html) - Main web page
- [`index.js`](./index.js) - JavaScript logic

## Setup and Installation

To run the challenge locally using Docker:

1. Build the Docker container:
   ```bash
   docker build -t imperialgate .
   ```
2. Run the container:
   ```bash
   docker run -p 9090:3000 imperialgate
   ```
   The challenge will be available at [http://localhost:9090](http://localhost:9090)

## Hints

Rumor says that the enemy was fooling us all in the first place. There is neither a portal nor a trail just some code not even hidden in plain site but in plain script

## Solution

<details>
<summary>Click to reveal solution</summary>

### Analysis Approach

1. Visit the challenge portal and inspect the login screen
2. Open the browser developer tools and review the JavaScript files
3. Find the hardcoded username and password in the client-side code
4. Log in using these credentials; you will be redirected to `/login`
5. The `/login` endpoint rick rolls you, but the flag is hidden in the JavaScript logs

### Step-by-Step Solution

#### Step 1: Access the Challenge

- Go to [http://challenges.mcsc.space:9090/](http://challenges.mcsc.space:9090/)
- Open browser developer tools (F12)

#### Step 2: Find Credentials

- Inspect `index.js` for hardcoded username and password
- Use these credentials to log in

#### Step 3: Find the Flag

- After login, you are redirected and rick rolled
- Check the JavaScript logs in the code:

```js
  // These logs might not be seen due to immediate redirect
  console.log("Extracting user metadata...");
  console.log("IP address logged: Tracking initiated");
  console.log("Breach pattern matches known enemy signature");
  console.log("Deploying countermeasures...");
  console.log("mcsc{s3cr3t_4rmY_r1ckr0ll3d}");
});
```

- The flag is: `mcsc{s3cr3t_4rmY_r1ckr0ll3d}`

</details>

## Author

Created by [psychoSherlock](https://github.com/psychoSherlock)

document.addEventListener("DOMContentLoaded", function () {
  const loginButton = document.getElementById("login-button");
  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  const container = document.querySelector(".login-container");

  let attempts = 0;

  const correctUsername = "pakarmy";

  const loginMessages = [
    "SECURITY BREACH: Authentication failure detected. Session compromised.",
    "ALERT: Unauthorized access attempt has been logged.",
    "WARNING: Invalid credentials provided. Security protocols activated.",
    "NOTICE: System has flagged this login attempt as suspicious.",
    "SECURITY ALERT: Access denied due to authentication failure.",
    "SYSTEM MESSAGE: Credentials verification failed. Access restricted.",
    "AUTHENTICATION ERROR: Please verify your credentials and try again.",
  ];

  loginButton.addEventListener("click", function () {
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    if (username === correctUsername && password === "secure@123") {
      loginSuccess();
    } else {
      loginFailed();
    }
  });

  function loginSuccess() {
    // Get the username and password before clearing the inputs
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();

    // Clear the input fields
    usernameInput.value = "";
    passwordInput.value = "";

    // Reset attempts counter
    attempts = 0;

    // Redirect to login URL with username and password as query parameters
    window.location.href = `/login?username=${encodeURIComponent(
      username
    )}&password=${encodeURIComponent(password)}`;
  }

  function loginFailed() {
    attempts++;

    const randomMessage =
      loginMessages[Math.floor(Math.random() * loginMessages.length)];

    const messageElement = document.createElement("div");
    messageElement.textContent = randomMessage;
    messageElement.style.color = "#e32636";
    messageElement.style.marginTop = "15px";
    messageElement.style.fontSize = "13px";
    messageElement.style.padding = "8px";
    messageElement.style.border = "1px dashed #e32636";
    messageElement.style.backgroundColor = "rgba(227, 38, 54, 0.1)";

    container.appendChild(messageElement);

    if (attempts >= 3) {
      const typewriterEffect = document.createElement("div");
      typewriterEffect.textContent =
        "INITIATING COUNTERMEASURES: Deploying chai and samosas to trace your location...";
      typewriterEffect.style.color = "#ddd";
      typewriterEffect.style.marginTop = "15px";
      typewriterEffect.style.fontSize = "12px";
      typewriterEffect.style.fontFamily = "monospace";
      typewriterEffect.style.textAlign = "left";
      typewriterEffect.style.padding = "5px";
      typewriterEffect.style.backgroundColor = "#111";
      typewriterEffect.style.borderLeft = "2px solid #e32636";

      container.appendChild(typewriterEffect);

      // Simulate typing
      let fullText = typewriterEffect.textContent;
      typewriterEffect.textContent = "";
      let i = 0;

      const typeWriter = function () {
        if (i < fullText.length) {
          typewriterEffect.textContent += fullText.charAt(i);
          i++;
          setTimeout(typeWriter, 50);
        }
      };

      typeWriter();
    }

    setTimeout(() => {
      const messages = container.querySelectorAll(
        "div:not(.war-symbol):not(.enemy-signature):not(.classified):not(.stamp)"
      );
      messages.forEach((msg) => {
        if (msg !== messageElement) {
          container.removeChild(msg);
        }
      });
    }, 5000);

    setTimeout(() => {
      if (container.contains(messageElement)) {
        container.removeChild(messageElement);
      }
    }, 3000);
  }
});

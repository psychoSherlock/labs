document
  .getElementById("submit-button")
  .addEventListener("click", function (event) {
    event.preventDefault(); // Prevents the form from submitting normally

    var username = document.getElementById("username").value; // Get the value from the input box

    // Navigate to /profile?username={username}
    window.location.href = "/profile?username=" + encodeURIComponent(username);
  });

document.getElementById("username").addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault(); // Prevent form submission
    document.getElementById("submit-button").click(); // Trigger the button click event
  }
});

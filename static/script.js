// Get the username from the URL parameter
var urlParams = new URLSearchParams(window.location.search);
var username = urlParams.get("username");
// console.log(username);

// Set the username dynamically
// document.getElementById("username").innerHTML = username;

// Generate the avatar image URL

var avatarUrl = `https://robohash.org/${username.length.toString()}.png`;

// Create and set the profile picture image dynamically
var profilePicture = document.createElement("img");
profilePicture.src = avatarUrl;
profilePicture.alt = "Profile Picture";

document.getElementById("profile-picture").appendChild(profilePicture);

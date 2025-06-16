
// directs user to the 'change account info' page
document.addEventListener("DOMContentLoaded", function() {
            const button = document.getElementById("CI");
            button.addEventListener("click", function(event) {
                event.preventDefault();
                window.location.href = "/change_account_info";
            });
        });


// deletes user
document.addEventListener("DOMContentLoaded", function() {
            const button = document.getElementById("DA");
            button.addEventListener("click", function(event) {
                event.preventDefault();
                window.location.href = "/api/delete_user";
                window.alert("Account Deleted Successfully");
            });
        });


//script purpose: reqeust the user's account information from the flask server
// and present it to the user
document.addEventListener("DOMContentLoaded", async function() {
    const response = await fetch("/api/get_profile_info", { method: "POST" });
    const data = await response.json();
    console.log(data);

    const WelcomeUser = document.getElementById('WelcomeUser');
    WelcomeUser.textContent = "Welcome, " + data.username + "!";

    const Username = document.getElementById('Username');
    Username.textContent = "Username: " + data.username;


    const Email = document.getElementById('Email');
    Email.textContent = "Email: " + data.email;
});


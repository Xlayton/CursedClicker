var apiurl = "http://f8f303c7ee02.ngrok.io"

function register() {
    var email = document.getElementById("email")
    var username = document.getElementById("username")
    var password = document.getElementById("password")
    var passwordVerify = document.getElementById("passVerify")
    if (password.value !== passwordVerify.value) {
        return false
    }
    fetch(apiurl + "/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "email": email.value,
                "uname": username.value,
                "password": password.value
            })
        })
        .then(res => res.text())
        .then(txt => {
            if (txt === "user registered") {
                window.location = "./login.html"
            } else {
                console.log(txt, "Fuck :)")
            }
        })
}

function login() {
    var email = document.getElementById("email")
    var password = document.getElementById("password")
    console.log(email.value, password.value)
    obj = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "email": email.value,
            "password": password.value
        })
    }
    console.log(obj)
    fetch(apiurl + "/login", obj)
        .then(res => res.json())
        .then(data => {
            document.cookie = "email=" + data.email
            fetch(apiurl + "/getmykey", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        "email": email.value
                    })
                }).then(res => res.json())
                .then(data => {
                    document.cookie = "key=" + data.key
                    window.location = "./game.html"
                })
        })
        .catch(() => {
            console.log("login failed lmao")
        })
}

if (document.getElementById("registerButton")) {
    document.getElementById("registerButton").addEventListener("click", register)
}
if (document.getElementById("loginButton")) {
    document.getElementById("loginButton").addEventListener("click", login)
}
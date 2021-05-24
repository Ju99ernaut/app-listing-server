var notifications = document.querySelector('.notifications');
var loginCont = document.querySelector('.login-form');
var roleCont = document.querySelector('.role-form');
var loginForm = loginCont.querySelector('#login');
var usernameForm = roleCont.querySelector('#username');
var emailForm = roleCont.querySelector('#email');
var token = null;

loginForm.addEventListener('submit', function (ev) {
    ev.preventDefault();
    login();
});

usernameForm.addEventListener('submit', function (ev) {
    ev.preventDefault();
    userRole();
});

emailForm.addEventListener('submit', function (ev) {
    ev.preventDefault();
    emailRole();
});

function login() {
    fetch('/auth', { method: 'POST', body: new FormData(loginForm) })
        .then(function (res) {
            return res.json()
        })
        .then(function (res) {
            token = res.token_type + " " + res.access_token;
            _login();
        })
    loginForm.reset();
}

function _login() {
    fetch('/users/me', { headers: new Headers({ authorization: token }) })
        .then(function (res) {
            return res.json()
        })
        .then(function (res) {
            if (res.role && res.role === 'admin') {
                notifications.innerHTML = "Welcome " + res.username;
                loginCont.style.display = "none";
                roleCont.style.display = "flex";
            } else {
                notifications.innerHTML = "You are not an admin";
                loginCont.style.display = "flex";
                roleCont.style.display = "none";
            }
        })
}

function userRole() {
    fetch('/admin/username/roles?' + formToQuery(usernameForm), {
        headers: new Headers({ authorization: token })
    });
    usernameForm.reset();
    notifications.innerHTML = "User role set";
}

function emailRole() {
    fetch('/admin/email/roles?' + formToQuery(usernameForm), {
        headers: new Headers({ authorization: token })
    });
    emailForm.reset();
    notifications.innerHTML = "Email role set";
}

function formToQuery(form) {
    var formObj = Object.fromEntries(new FormData(form));
    return serialize(formObj)
}

function serialize(obj) {
    var str = [];
    for (var p in obj)
        if (obj.hasOwnProperty(p)) {
            str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
        }
    return str.join("&");
}
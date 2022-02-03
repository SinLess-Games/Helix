const express = require('express');
const app = express();

app.get("/", (req, res) => {
    res.send('Hello World')
});

app.get("/login", (req, res) => {
    res.send('Login')
});

app.get("/register", (req, res) => {
    res.send('registration')
});



app.get("/policies", (req, res) => {
    res.send('policies')
});

app.get("/policies/privacy-policy", (req, res) => {
    res.send('Privacy Policy')
});

app.get("/policies/security-policy", (req, res) => {
    res.send('Security Policy')
});

app.get("/policies/terms-of-use", (req, res) => {
    res.send('Terms of use')
});

app.get("/policies/cookie-policy", (req, res) => {
    res.send('Cookie Policy')
});

app.get("/policies/user-information-policy", (req, res) => {
    res.send('User information Policy')
});



app.get("/wiki", (req, res) => {
    res.send('Wiki')
});



app.get("/store", (req, res) => {
    res.send('Store')
});

app.get("/store/cart", (req, res) => {
    res.send('Cart')
});



app.get("/dashboard", (req, res) => {
    res.send('DashBoard')
});

app.get("/dashboard/server-list", (req, res) => {
    res.send('Server List')
});

app.get("/dashboard/server-list/dashboard", (req, res) => {
    res.send('Server DashBoard')
});

app.get("/profile", (req, res) => {
    res.send('Profile')
});

app.get("/profile/account-info", (req, res) => {
    res.send('Account Information')
});

app.get("/profile/my-products", (req, res) => {
    res.send('My Products')
});

app.get("/profile/account-security", (req, res) => {
    res.send('Account Security')
});


app.listen(3000, () => console.log('Listening On port 3000. \n\n http://localhost:3000'))
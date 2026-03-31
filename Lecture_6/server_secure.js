const express = require('express');
const jwt = require('jsonwebtoken');
const cookieParser = require('cookie-parser');

const app = express();
const SECRET_KEY = "NODE_SOA_SECURE_KEY";

// CONFIG: Enable JSON body and Cookie parsing
app.use(express.json());
app.use(cookieParser());

// 1. Middleware to validate Token and Scopes
const authorize = (requiredScope) => {
    return (req, res, next) => {
        // Read token from HttpOnly COOKIE
        const token = req.cookies.access_token;

        if (!token) {
            return res.status(401).json({ message: "You are not logged in (Missing Cookie)!" });
        }

        try {
            const decoded = jwt.verify(token, SECRET_KEY);
            
            // CHECK SCOPES
            if (requiredScope && !decoded.scopes.includes(requiredScope)) {
                return res.status(403).json({ message: `Missing required permission: ${requiredScope}` });
            }

            req.user = decoded.user;
            next();
        } catch (err) {
            return res.status(401).json({ message: "Invalid or expired token!" });
        }
    };
};

// 2. Login API - Set HttpOnly Cookie
app.post('/login', (req, res) => {
    const { username } = req.body;
    let scopes = [];

    if (username === 'admin') {
        scopes = ['profile:read', 'profile:edit'];
    } else {
        scopes = ['profile:read'];
    }

    // Create JWT
    const token = jwt.sign(
        { user: username, scopes: scopes }, 
        SECRET_KEY, 
        { expiresIn: '30m' }
    );

    // SET HTTPONLY COOKIE
    res.cookie('access_token', token, {
        httpOnly: true,   // Most important: prevent XSS
        secure: false,    // Set to true when using HTTPS
        sameSite: 'Lax'   // Basic CSRF protection
    });

    res.json({ message: "Login successful and cookie has been set!" });
});

// 3. API requiring only View permission
app.get('/view-profile', authorize('profile:read'), (req, res) => {
    res.json({ data: `Profile data of ${req.user} (Node.js)` });
});

// 4. API requiring Edit permission
app.post('/edit-profile', authorize('profile:edit'), (req, res) => {
    res.json({ message: `User ${req.user} updated profile successfully!` });
});

// 5. Logout API - Clear Cookie
app.post('/logout', (req, res) => {
    res.clearCookie('access_token');
    res.json({ message: "Cookie cleared, you have logged out!" });
});

app.listen(3000, () => console.log('Node.js Secure Server running on port 3000'));
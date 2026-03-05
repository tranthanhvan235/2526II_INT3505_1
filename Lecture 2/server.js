const express = require("express");
const app = express();

app.use(express.json());

let users = [
  { id: 1, name: "Nguyen Van A", email: "a@gmail.com" },
  { id: 2, name: "Tran Thi B", email: "b@gmail.com" }
];

// 1. Lay danh sach nguoi dung
app.get("/api/users", (req, res) => {
  res.json(users);
});

// 2. Lay thong tin 1 nguoi dung
app.get("/api/users/:id", (req, res) => {
  const user = users.find(u => u.id == req.params.id);

  if (!user) {
    return res.status(404).json({ message: "User not found" });
  }

  res.json(user);
});

// 3. Tao user moi
app.post("/api/users", (req, res) => {
  const newUser = {
    id: users.length + 1,
    name: req.body.name,
    email: req.body.email
  };

  users.push(newUser);
  res.status(201).json(newUser);
});

// 4. Cap nhat email
app.put("/api/users/:id", (req, res) => {
  const user = users.find(u => u.id == req.params.id);

  if (!user) {
    return res.status(404).json({ message: "User not found" });
  }

  user.email = req.body.email;

  res.json(user);
});

// 5. Xoa user
app.delete("/api/users/:id", (req, res) => {
  const index = users.findIndex(u => u.id == req.params.id);

  if (index === -1) {
    return res.status(404).json({ message: "User not found" });
  }

  users.splice(index, 1);
  res.json({ message: "User deleted" });
});

// Demo loi 500
app.get("/api/error", (req, res) => {
  throw new Error("Internal Server Error Demo");
});

// Demo loi 429 (rate limit gia lap)
let requestCount = 0;

app.get("/api/limited", (req, res) => {
  requestCount++;

  if (requestCount > 5) {
    return res.status(429).json({ message: "Too many requests" });
  }

  res.json({ message: "Request OK", count: requestCount });
});

app.listen(3000, () => {
  console.log("Server running at http://localhost:3000");
});
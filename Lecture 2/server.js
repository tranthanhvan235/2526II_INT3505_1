const express = require("express");
const app = express();

app.use(express.json());

let users = [
  { id: 1, name: "Nguyen Van A", email: "a@gmail.com" },
  { id: 2, name: "Tran Thi B", email: "b@gmail.com" }
];


app.get("/api/users", (req, res) => {
  res.json(users);
});


app.get("/api/users/:id", (req, res) => {
  const user = users.find(u => u.id == req.params.id);

  if (!user) {
    return res.status(404).json({ message: "User not found" });
  }

  res.json(user);
});


app.post("/api/users", (req, res) => {
  const newUser = {
    id: users.length + 1,
    name: req.body.name,
    email: req.body.email
  };

  users.push(newUser);
  res.status(201).json(newUser);
});


app.put("/api/users/:id", (req, res) => {
  const user = users.find(u => u.id == req.params.id);

  if (!user) {
    return res.status(404).json({ message: "User not found" });
  }

  user.email = req.body.email;

  res.json(user);
});


app.delete("/api/users/:id", (req, res) => {
  const index = users.findIndex(u => u.id == req.params.id);

  if (index === -1) {
    return res.status(404).json({ message: "User not found" });
  }

  users.splice(index, 1);
  res.json({ message: "User deleted" });
});


app.get("/api/error", (req, res) => {
  throw new Error("Internal Server Error Demo");
});


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
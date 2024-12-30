import express from "express";

const app = express();
app.use(express.json());
const port = 3001;

app.get("/", (req, res) => {
  console.log(req.body, req.headers);
  res.send("hello");
  console.log("hello");
});

app.post("/", (req, res) => {
  console.log(req.body, req.headers);
  res.send("hello");
  console.log("hello");
});
app.listen(port, () => {
  console.log("server is listenting at", port);
});

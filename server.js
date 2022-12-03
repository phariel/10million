const http = require("http");
const fs = require("fs");
const port = process.env["PORT"] ?? 8080;

const requestListener = function (req, res) {
  const cont = fs.readFileSync("./ball.txt", "utf-8");
  const temp = `<input id="#ball" value='${cont}' />`;
  res.setHeader("Content-Type", "text/html");
  res.writeHead(200);
  res.end(temp);
};

const server = http.createServer(requestListener);
server.listen(port);
console.log(`Server Started at ${port}`);

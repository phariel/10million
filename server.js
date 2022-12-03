const http = require("http");
const fs = require("fs");

const requestListener = function (req, res) {
  const cont = fs.readFileSync("./ball.txt", "utf-8");
  const temp = `<input id="#ball" value='${cont}' />`;
  res.setHeader("Content-Type", "text/html");
  res.writeHead(200);
  res.end(temp);
};

const server = http.createServer(requestListener);
server.listen(8080);
console.log("Server Start");

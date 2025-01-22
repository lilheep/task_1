const http = require("http");
const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express()

app.use(express.static(path.join(__dirname, "../frontend/public")));
    
app.listen(3000, function(){
    console.log("Server started at 3000!")
});
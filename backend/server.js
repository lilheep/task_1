const express = require("express");
const path = require("path");
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, "../frontend/public")));

const {Users, Roles, Staffs, Students} = require("./models.py");

app.get("/users", async(req, res) => {
    try {
        const users = await Users.findAll();
        res.json(users);
    } catch (error) {
        console.error(`Error fetching users: ${error}`);
        res.status(500).json({error: "Failed to fetch users!"});
    };
});


app.get("/roles", (req, res) => {
    try {
        const roles = Roles.findAll();
        res.json(roles);
    } catch (error) {
        console.error(`Error fetching roles: ${error}`);
        res.status(500).json({error: "Failed to fetch roles!"});
    };
});

app.get("/staffs", (req, res) => {
    try {
        const staffs = Staffs.findAll();
        req.json(staffs);
    } catch (error) {
        console.error(`Error fetching staffs: ${error}`);
        res.status(500).json({error: "Failed to fetch staffs!"});
    };
});

app.get("/students", (req, res) => {
    try {
        const students = Students.findAll();
        req.json(students);
    } catch (error) {
        console.error(`Error fetching students: ${error}`);
        res.status(500).json({error: "Failed to fetch students!"});
    };
});

app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "./fronted/public/index.html"));
});
    
app.listen(PORT, function(){
    console.log(`Server started at ${PORT}!`)
});
const express = require("express");
const mysql = require("mysql");
const path = require("path");
const PORT = process.env.PORT || 3000;

const app = express();
app.use(express.static(path.join(__dirname, "templates")));

const constants = {
  matchStatus: {
    pending: 0,
    accepted: 1,
    rejected: -1,
  },
};
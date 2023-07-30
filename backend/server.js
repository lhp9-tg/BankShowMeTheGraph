import express from "express";
import fileUpload from "express-fileupload";
import { PythonShell } from "python-shell";
// import cors from "cors";
import fs from "fs";

const app = express();

app.use(fileUpload());
// app.use(cors());

const cors = function (req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  if (req.method === "OPTIONS") {
    res.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE");
    res.setHeader("Access-Control-Allow-Headers", "Accept , Content-Type");
  }
};

app.post("/upload", (req, res) => {
  console.log(req.files);
  let csvFile = req.files["file"];

  // Vérifie si le fichier est bien un fichier CSV
  if (!csvFile.name.endsWith(".csv")) {
    return res.status(400).send("File is not a CSV");
  }

  // Création des dossiers si ils n'existent pas
  const dir = "../data";

  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir);
  }
  if (!fs.existsSync(dir + "/temp")) {
    fs.mkdirSync(dir + "/temp");
  }
  if (!fs.existsSync(dir + "/JSON")) {
    fs.mkdirSync(dir + "/JSON");
  }

  const filename = Date.now();

  csvFile.mv(`${dir}/temp/${filename}.csv`, function (err) {
    if (err) {
      console.error(err);
      return res.status(500).send(err);
    }

    PythonShell.run("../python/showmethegraph.py", null, function (err) {
      if (err) {
        console.error(err);
        throw err;
      }
      res.send("File uploaded and script run!");
    });
  });
});

app.get("/", (req, res) => {
  res.send("Hello, world!");
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send("Something broke!");
});

app.listen(5000, () => {
  console.log("Server is running on port 5000");
});

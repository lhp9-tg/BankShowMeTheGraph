import express from "express";
import fileUpload from "express-fileupload";
import { PythonShell } from "python-shell";
import cors from "cors";

const app = express();

app.use(fileUpload());
app.use(cors());

app.post("/upload", (req, res) => {
  console.log(req.files);
  let csvFile = req.files["file"];

  csvFile.mv("../data/save.csv", function (err) {
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

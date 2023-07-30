import React, { useState } from 'react';
import axios from 'axios';
import Plot from 'react-plotly.js';

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);

  const onFileChange = (e) => {
    setFile(e.target.files[0]);
  }

  const onFileUpload = () => {
    const formData = new FormData(); 
    formData.append('file', file); 
  
    axios.post('http://localhost:5000/upload', formData)
      .then((response) => {
        console.log(response.data);
      })
      .catch((error) => {
        console.error("Error uploading file: ", error);
      });
  }

  return (
    <div>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload}>Upload</button>
      {data && <Plot data={data} />}
    </div>
  );
}

export default App;

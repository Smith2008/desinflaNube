import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/costs/')
      .then(res => setData(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Costos AWS</h1>
      <ul>
        {data.map(item => (
          <li key={item.date}>{item.date}: ${item.cost}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;

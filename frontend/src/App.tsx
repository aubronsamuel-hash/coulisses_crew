import { useEffect } from 'react';

function App() {
  useEffect(() => {
    fetch('http://localhost:8001/healthz')
      .then((res) => res.json())
      .then((data) => console.log(data))
      .catch((err) => console.error(err));
  }, []);

  return <div>Frontend OK</div>;
}

export default App;

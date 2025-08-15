import { useEffect } from 'react'

function App() {
  useEffect(() => {
    const url = import.meta.env.VITE_API_URL || ''
    if (url) {
      fetch(`${url}/healthz`)
        .then((res) => res.json())
        .then((data) => console.log(data))
        .catch((err) => console.error(err))
    }
  }, [])

  return <h1>Frontend OK</h1>
}

export default App

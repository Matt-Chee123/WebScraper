import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';


function App() {
    const [url,setUrl] = useState('');
    const [links, setLinks] = useState([]);
    const [error, setError] = useState(null);

    const onClickHandler = async (e) => {
        e.preventDefault(); // Prevents the default form submission
        try {
            const response = await fetch('http://127.0.0.1:5000/scrape/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({url}),
            });

            const data = await response.json();

            if (response.ok) {
                setLinks(data.links);
                setError(null);
            } else {
                setError(data.error || 'Something went wrong!');
                setLinks([]);
            }
        } catch (err) {
            setError('Failed to fetch data');
            setLinks([]);
        }
    }

  const handleInputChange = (e) => {
    setUrl(e.target.value); // Updates the URL state
  };
  console.log(links)
  return (
    <div className="App">
    <nav className="navbar navbar-expand-lg bg-black">
      <div class="container-fluid">
        <a className="navbar-brand text-light">WebScraper</a>
      <form className="d-flex" role="search" onSubmit={onClickHandler}>
        <input className="form-control me-2" type="url" value={url} onChange={handleInputChange} placeholder="Enter a URL"></input>
        <button className="btn btn-outline-success text-light" type="submit">Submit</button>
      </form>
      </div>
    </nav>
    </div>
  );
}

export default App;

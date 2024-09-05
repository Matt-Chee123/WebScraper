import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';


function App() {
    const [description,setDescription] = useState('');
    const [links, setLinks] = useState([]);
    const [error, setError] = useState(null);

    const onClickHandler = async (e) => {
        e.preventDefault(); // Prevents the default form submission
        try {
            const response = await fetch('http://127.0.0.1:5000/scrape/google', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({description}),
            });

            const data = await response.json();

            if (response.ok) {
                setLinks(data.jobs);
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
    setDescription(e.target.value);
    console.log(description)
  };

  console.log(links);
  return (
    <div className="App">
    <nav className="navbar navbar-expand-lg bg-black">
      <div class="container-fluid">
        <a className="navbar-brand text-light">WebScraper</a>
      <form className="d-flex" role="search" onSubmit={onClickHandler}>
        <input className="form-control me-2" type="string" value={description} onChange={handleInputChange} placeholder="Enter a Job"></input>
        <button className="btn btn-outline-success text-light" type="submit">Submit</button>
      </form>
      </div>
    </nav>
    <h1> Jobs</h1>
    </div>
  );
}

export default App;

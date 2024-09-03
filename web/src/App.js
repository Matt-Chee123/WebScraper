import logo from './logo.svg';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';


function App() {
    const [url,setUrl] = useState('');

    const onClickHandler = (e) => {
        e.preventDefault(); // Prevents the default form submission
        console.log(url); // Logs the current URL state
    }

  const handleInputChange = (e) => {
    setUrl(e.target.value); // Updates the URL state
  };

  return (
    <div className="App">
    <nav className="navbar navbar-expand-lg bg-black">
      <div class="container-fluid">
        <a className="navbar-brand text-light">WebScraper</a>
      <form className="d-flex" role="search" onSubmit={onClickHandler}>
        <input className="form-control me-2" type="string" onChange={handleInputChange} placeholder="Enter a URL"></input>
        <button className="btn btn-outline-success text-light" type="submit">Submit</button>
      </form>
      </div>
    </nav>
    </div>
  );
}

export default App;

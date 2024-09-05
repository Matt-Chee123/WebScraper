import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';
import GoogleContainer from './googleContainer/GoogleContainer';

function App() {
    const [description,setDescription] = useState('');
    const [submitDescription, setSubmitDescription] = useState(''); // To store the submitted description

    const handleInputChange = (e) => {
        setDescription(e.target.value);
    };

    const onClickHandler = (e) => {
        e.preventDefault(); // Prevent form from submitting and reloading
        setSubmitDescription(description); // Update the description to be used for the API call
    };

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
    <GoogleContainer description={submitDescription}/>
    </div>
  );
}

export default App;

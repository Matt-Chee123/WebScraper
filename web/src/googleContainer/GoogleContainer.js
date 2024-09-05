import './googContainer.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState } from 'react';

function GoogleContainer({ googJobs }) {
    console.log(googJobs);
    return(
        <div className="googContainer">
            <h3> Google Jobs</h3>
            <ul className="urlList">
                { googJobs.map((url,index) => (
                    <li key={index}><a href={url.link} target="_blank" rel="noopener noreferrer">{url.name}</a></li>
                ))}
            </ul>
        </div>
    )
}

export default GoogleContainer;
import './googContainer.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState, useEffect } from 'react';

function GoogleContainer({ description }) {
    const [jobs, setJobs] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (description) { // Only fetch if a description is provided
            const fetchJobs = async () => {
                try {
                    const response = await fetch('http://127.0.0.1:5000/scrape/google', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ description }), // Pass the description to the API
                    });

                    const data = await response.json();

                    if (response.ok) {
                        setJobs(data.jobs);
                        setError(null);
                    } else {
                        setError(data.error || 'Something went wrong!');
                        setJobs([]);
                    }
                } catch (err) {
                    setError('Failed to fetch data');
                    setJobs([]);
                }
            };

            fetchJobs(); // Trigger the API call when description changes
        }
    }, [description]);

    return(
        <div className="googContainer">
            <h3> Google Jobs</h3>
            <ul className="urlList">
                { jobs.map((url,index) => (
                    <li key={index}><a href={url.link} target="_blank" rel="noopener noreferrer">{url.name}</a></li>
                ))}
            </ul>
        </div>
    )
}

export default GoogleContainer;
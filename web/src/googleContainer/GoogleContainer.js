import '../jobContainer.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import React, { useState, useEffect } from 'react';

export default function GoogleContainer({ description }) {
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


    const handleRadioClick = async (url,isAccepted) => {
        if (isAccepted) {
            try {
                const response = await fetch('http://127.0.0.1:5000/job/accepted', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ link: url }), // Send the URL to the server
                });

                if (response.ok) {
                    console.log("Link saved successfully to accept file");
                } else {
                    console.log("Failed to save link");
                }
            } catch (error) {
                console.error("Error:", error);
            }
        } else {
            try {
                const response = await fetch('http://127.0.0.1:5000/job/declined', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ link: url }), // Send the URL to the server
                });

                if (response.ok) {
                    console.log("Link saved successfully to decline file");
                } else {
                    console.log("Failed to save link");
                }
            } catch (error) {
                console.error("Error:", error);
            }
        };
    }
    return(
        <div className="jobContainer">
            <h3>Google Jobs</h3>
            <ul className="urlList">
                { jobs.map((url,index) => (
                    <li key={index}>
                    <a href={url.link} target="_blank" rel="noopener noreferrer">{url.name}</a>
                    <div className="radioButtons">
                        <input type="radio" id={`job-${index}-accept`}
                        name={`job-{index}`}
                        vale="accept"
                        onClick={() => handleRadioClick(url.link,true)}
                    />
                    <label htmlFor={`job-${index}-option1`}>Accept</label>
                        <input type="radio" id={`job-${index}-decline`}
                        name={`job-{index}`}
                        vale="decline"
                        onClick={() => handleRadioClick(url.link,false)}
                    />
                    <label htmlFor={`job-${index}-option1`}>Decline</label>
                    </div>
                    </li>
                ))}
            </ul>
        </div>
    )
}
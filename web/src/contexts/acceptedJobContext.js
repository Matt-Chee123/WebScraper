import React, { createContext, useContext, useState, useEffect } from 'react';

const AcceptedContext = createContext();

export function AcceptedProvider({ children }) {
    const [acceptedData, setAcceptedData] = useState(null);

    useEffect(() => {
        fetch(`http://127.0.0.1:5000/job/getAccepted`)
            .then(response => response.json())
            .then(data => setAcceptedData(data))
            .catch(error => console.error('Error fetching accepted links:', error));
    })

    return (
        <AcceptedContext.Provider value={acceptedData}>
            {children}
        </AcceptedContext.Provider>
    )
}

export function useAccepted() {
    return useContext(AcceptedContext);
}
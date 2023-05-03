import { useEffect, useState, useRef } from 'react';

const Clients = ({ clients }) => {
    useEffect(() => {
        console.log(clients);
    }, [clients]);

    if (!clients) {
        return <>0</>;
    }

    return <>{clients.length}</>;
};

export default Clients;

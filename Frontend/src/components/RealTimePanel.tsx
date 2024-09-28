'use client'

import { Divider } from "antd";
import AccelerationMonitor from "./AccelerationMonitor";
import AngleMonitor from "./AngleMonitor";
import { useEffect, useState } from 'react';
import io, { Socket } from 'socket.io-client';
import { DefaultEventsMap } from "@socket.io/component-emitter";

interface ISocketValues {
    data: {
        accelerometer: number,
        gyroscope: number,
    }
}

export default function RealTimePanel() {

    // Socket in useEffect
    let socket: Socket<DefaultEventsMap, DefaultEventsMap>;
    const [socketValues, setSocketValues] = useState<ISocketValues | null>(null);

    // try this when socket is fully function.
    // useEffect(() => {
    //     socket = io('http://localhost:8080');

    //     socket.on('connect', () => {
    //         console.log('Connected to server');
    //     });

    //     socket.on('data', (data) => {
    //         setSocketValues(data);
    //     });

    //     socket.on('disconnect', () => {
    //         console.log('Disconnected from server');
    //     });

    //     return () => {
    //         socket.disconnect();
    //     };
    // }, []);

    // Mock Data from Socket
    useEffect(() => {
        setSocketValues({
            data: {
                accelerometer: 100,
                gyroscope: 20
            }
        })
    }, [])

    return (
        <div className="mx-40 my-10 py-6 px-8 rounded-xl border-2 border-green-800 shadow-xl bg-gray-200">
            <div className="font-bold text-2xl text-green-800">Real - Time Performance</div>
            <Divider className="m-0 mt-2 border-green-800 border-[1px]"/>
            <div className="flex flex-row justify-around mt-4">
                <AccelerationMonitor acceleration={socketValues ? socketValues.data.accelerometer : 0}/>
                <AngleMonitor/>
            </div>
        </div>
    )
}
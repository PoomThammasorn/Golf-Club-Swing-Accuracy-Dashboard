'use client'

import { Divider } from "antd";
import LineChart from "./LineChart";

type DistanceErrorProps = {
    distanceErrors: any
}

export default function DistanceErrorChart(props: DistanceErrorProps) {
    return (
        <div className="block w-[460px] m-4 py-4 px-6 rounded-md shadow-xl shadow-lg bg-gray-100">
            <div className="font-bold text-xl text-green-800">Distance Error Statistics</div>
            <Divider className="m-0 mt-2 border-green-800"/>
            <LineChart value={props.distanceErrors} />
        </div>
    )
}
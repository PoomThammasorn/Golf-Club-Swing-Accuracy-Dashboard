'use client'

import PowerBar from './PowerBar' 
import { Divider, Statistic, ConfigProvider } from "antd";

type CiubHeadSpeedProps = {
    velocity: number
}

export default function ClubHeadSpeedMonitor(props: CiubHeadSpeedProps) {
    return (
        <div className="block w-[450px] m-4 py-4 px-6 rounded-md shadow-xl shadow-lg bg-gray-100">
            <div className="font-bold text-xl text-green-800">Club Head Speed</div>
            <Divider className="m-0 mt-2 border-green-800"/>
            <div className='flex flex-row justify-between pt-8'>
                <PowerBar value={props.velocity}/>
                <ConfigProvider
                    theme={{
                        token: {
                            fontFamily: 'Roboto Condensed, sans-serif'
                        },
                        components: {
                            Statistic: {
                                contentFontSize: 28,
                                titleFontSize: 16
                            },
                        },
                    }}
                >
                    <div className='flex flex-row justify-start'>
                        <Statistic title="Velocity" value={(props.velocity / 0.44704).toFixed(2)} suffix="mph" className='p-4'/>
                    </div>
                </ConfigProvider>
            </div>
        </div>
    )
}
'use client'

import PowerBar from './PowerBar' 
import { Divider, Statistic, ConfigProvider } from "antd";

type AccelerationProps = {
    acceleration: number
}

export default function AccelerationMonitor(props: AccelerationProps) {
    return (
        <div className="block w-[400px] m-4 py-4 px-6 rounded-md shadow-xl shadow-lg bg-gray-100">
            <div className="font-2xl font-bold text-lg text-green-800">Acceleration</div>
            <Divider className="m-0 mt-2 border-green-800"/>
            <div className='flex flex-row justify-start pt-8'>
                <PowerBar value={props.acceleration}/>
                <div className='ml-12'>
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
                    <Statistic title="Velocity" value={props.acceleration} suffix="m/s" className='p-2'/>
                    <Statistic title="Performance" value={'Good'} className='p-2'/>
                </ConfigProvider>
                </div>
            </div>
        </div>
    )
}
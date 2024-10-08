'use client'

import { Button, Divider, ConfigProvider, Modal } from "antd";
import { ReloadOutlined, DeleteOutlined } from '@ant-design/icons';
import { useEffect, useState } from "react";
import axios from 'axios';
import { backendUrl } from "@/constant";
import DistanceErrorChart from "./DistanceErrorChart";
import ScoreCard from "./ScoreCard";

export default function HistoryPanel() {

    const [loading, setLoading] = useState<boolean>(true);
    const [refresh, setRefresh] = useState<boolean>(true);
    const [distanceErrorArray, setDistanceErrorArray] = useState<Array<number>>([]);

    const getScore = (numberArray: Array<number>) => {
        return numberArray.filter(num => num === 0).length
    }

    const handleReloadPage = () => {
        setRefresh(!refresh)
    }

    const handleResetDatabase = async () => {
        try {
            const response = await axios.delete(`${backendUrl}/api/v1/sensors`);
            setRefresh(!refresh)
        } catch (error) {
            console.log(error)
        }
    }

    useEffect(() => {
        const getAllSensorData = async () => {
            try {
                setLoading(true)
                const response = await axios.get(`${backendUrl}/api/v1/sensors`);
                const distanceErrorArrayTmp = response.data.data.map((obj: any) => obj.distanceError)
                setDistanceErrorArray(distanceErrorArrayTmp)
            } catch(err) {
                console.log(err)
            } finally {
                setLoading(false)
            }
        }
        getAllSensorData()
    }, [refresh])
    
    return (
        <div className="w-[1000px] mb-8 py-6 px-8 rounded-xl border-2 border-green-800 shadow-xl bg-gray-200">
            <div className="font-bold text-2xl text-green-800">History</div>
            <Divider className="m-0 mt-2 border-green-800 border-[1px]"/>

            <div className="flex flex-col items-center">
                <div className="flex flex-row justify-center my-10">
                    {/* Line Chart shows Error */}
                    <DistanceErrorChart distanceErrors={distanceErrorArray} />

                    <div className="flex flex-col justify-center items-center">
                        {/* Score Card */}
                        <ScoreCard 
                            title={'Score'} 
                            value={getScore(distanceErrorArray)} 
                            maxValue={distanceErrorArray.length}
                            refresh={refresh} />

                        {/* Button Panel */}
                        <ConfigProvider
                            theme={{
                                components: {
                                    Button: {
                                        defaultHoverBorderColor: '#006d2c',
                                        defaultActiveBorderColor: '#006d2c',
                                        colorText: '#006d2c',
                                        defaultHoverColor: '#006d2c',
                                        defaultActiveColor: '#006d2c',
                                    },
                                },

                                token: {
                                    colorPrimaryBg: '#a70000',
                                    fontFamily: 'Roboto Condensed, sans-serif',
                                    fontSize: 16,
                                    colorText: '#006d2c' 
                                },
                            }}
                        >
                            <Button className="mt-4 shadow-md" type="default" onClick={handleReloadPage}><ReloadOutlined />Refresh History</Button>
                        </ConfigProvider>

                        <ConfigProvider
                            theme={{
                                components: {
                                    Button: {
                                        defaultBg: "#a70000",
                                        defaultHoverBg: "#ff0000",
                                        defaultActiveBg: "#ff0000",
                                        defaultHoverBorderColor: '#ff0000',
                                        defaultActiveBorderColor: '#ff0000',
                                        colorText: 'white',
                                        defaultHoverColor: 'white',
                                        defaultActiveColor: 'white'
                                    },
                                },

                                token: {
                                    colorPrimaryBg: '#a70000',
                                    fontFamily: 'Roboto Condensed, sans-serif',
                                    fontSize: 16,
                                    colorText: '#006d2c' 
                                },
                            }}
                        >
                            <Button className="mt-4 shadow-md" type="default" onClick={handleResetDatabase}><DeleteOutlined />Delete History</Button>
                        </ConfigProvider>

                    </div>
                </div>
            </div>
        </div>
    )
}
import { InputNumber, Button, ConfigProvider } from "antd";
import { SaveFilled } from '@ant-design/icons'
import axios from 'axios';
import { useState } from "react";
import { backendUrl } from "@/constant";

type SubmissionProps = {
    minDistance: number,
    maxDistance: number
}

export default function PerformanceSubmitForm(props: SubmissionProps) {

    const [expectedDistance, setExpectedDistance] = useState<number>(0)

    const handleInputChange = (value: any) => {
        setExpectedDistance(value);
    };

    const handleSubmit = async () => {
        try {
            const timestamp = new Date().toUTCString();
            const minDistanceError = Math.abs(props.minDistance - expectedDistance)
            const maxDistanceError = Math.abs(props.maxDistance - expectedDistance)
            const distanceError = maxDistanceError < minDistanceError ? maxDistanceError : minDistanceError
            const payload = {
                timestamp: timestamp,
                distanceError: distanceError
            }
            const response = await axios.post(`${backendUrl}/api/v1/sensors`, payload);
            console.log(response)
        } catch (err) {
            console.log(err)
        }
    }
    
    return (
        <div className="flex flex-row justify-center m-4"> 
            <ConfigProvider
                theme={{
                    components: {
                        InputNumber: {
                            activeBorderColor: "#41ab5d",
                            hoverBorderColor: "#41ab5d",
                        },
                        Button: {
                            defaultBg: "#006d2c",
                            defaultHoverBg: "#41ab5d",
                            defaultActiveBg: "#41ab5d",
                            defaultHoverBorderColor: '#41ab5d',
                            defaultActiveBorderColor: '#41ab5d',
                            colorText: 'white',
                            defaultHoverColor: 'white',
                            defaultActiveColor: 'white'
                        },
                    },

                    token: {
                        fontFamily: 'Roboto Condensed, sans-serif',
                        fontSize: 16,
                        colorText: '#006d2c' 
                    },
                }}
            >
                <InputNumber
                    className="w-[270px] mr-4 rounded-md shadow-md"
                    controls={false}
                    placeholder=""
                    prefix={<h3 className="font-bold text-md pr-6">Expected Distance:</h3>} 
                    suffix={<h3 className="font-bold text-md">ft.</h3>}
                    onChange={handleInputChange}
                />
                <Button className="ml-6 shadow-md" type="default" onClick={handleSubmit}><SaveFilled /> Save Performance</Button>
            </ConfigProvider>   
        </div>
    )
}
import { Divider } from "antd";
import { useEffect, useState } from "react";

type ScoreCardProps = {
    title: string,
    value: number,
    maxValue: number,
    refresh: boolean,
}

export default function ScoreCard(props: ScoreCardProps) {

    const [bgColor, setBgColor] = useState<string>('#75db60');

    const getColor = () => {
        if((props.value / props.maxValue) < 0.5) {
            return 'bg-[#be360d50]'
        } else if ((props.value / props.maxValue) < 0.75) {
            return 'bg-[#fbb32250]'
        } else {
            return 'bg-[#75db6050]'
        }
    }

    useEffect(() => {
        setBgColor(getColor())
        console.log(bgColor)
    }, [props])

    return (
        <div className={`block w-[250px] m-4 py-4 px-6 rounded-md shadow-xl shadow-lg ${bgColor}`}>
            <div className="font-bold text-md text-green-800">{props.title}</div>
            <Divider className="m-0 mt-2 border-green-800" />
            <div className="text-center pt-4 text-2xl">{props.value} / {props.maxValue}</div>
        </div>
    )
}
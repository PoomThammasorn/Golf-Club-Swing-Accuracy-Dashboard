import { Divider} from "antd";
import AccelerationMonitor from "./AccelerationMonitor";

export default function HistoryPanel() {

    // Socket in useEffect

    return (
        <div className="mx-40 my-10 py-6 px-8 rounded-xl border-2 border-green-800 shadow-xl bg-gray-200">
            <div className="font-bold text-2xl text-green-800">History</div>
            <Divider className="m-0 mt-2 border-green-800 border-[1px]"/>
            <div className="flex flex-row justify-around my-10">
                Maintenance
            </div>
        </div>
    )
}
import { Avatar, Divider } from 'antd';

type StatisticMonitorProps = {
	title: string;
	value: number | string;
	unit: string;
	pic?: string;
};

export default function StatisticMonitor(props: StatisticMonitorProps) {
	return (
		<div className="text-center block w-[250px] m-4 py-4 px-6 rounded-md shadow-xl shadow-lg bg-gray-100">
			<div className="font-bold text-md text-green-800">
				{props.title}
			</div>
			<Divider className="m-0 mt-2 border-green-800" />
			{props.pic && (
				<Avatar
					className="mt-2"
					size={{
						xs: 40,
						sm: 64,
						md: 72,
						lg: 80,
						xl: 96,
						xxl: 112,
					}}
					src={props.pic}
					alt="Not found"
				/>
			)}
			<div className="text-center pt-4 text-2xl">
				{props.value} {props.unit}
			</div>
		</div>
	);
}

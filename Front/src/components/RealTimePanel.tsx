'use client';

import { Divider, Input } from 'antd';
import AccelerationMonitor from './AccelerationMonitor';
import { useEffect, useState } from 'react';
import io from 'socket.io-client';
import StatisticMonitor from './StatisticMonitor';
import PerformanceSubmitForm from './PerformanceSubmitForm';
import { getFullname, getPic } from '@/utils';

interface ISocketValues {
	timestamp: Date;
	velocity?: number;
	result?: string;
}

export default function RealTimePanel() {
	// const [socketValues, setSocketValues] = useState<ISocketValues | null>(null);
	const [velocity, setVelocity] = useState<number>(0);
	const [ballSpeed, setBallSpeed] = useState<number>(0);
	const [distance, setDistance] = useState<number>(0);
	const [unknownFactor, setUnknownFactor] = useState<number>(5.8);
	const [golfer, setGolfer] = useState<string>('');
	const smashFactor = 1.5;

	const calculateDistance = (velocity: number) => {
		const distanceFromVelocity =
			((velocity * 1.5) ** 2 / (2 * 0.13 * 9.81)) * 3.28084;
		setDistance(distanceFromVelocity);
		return distanceFromVelocity;
	};

	useEffect(() => {
		// Create Socket.io client instance
		const socket = io('http://localhost:6996');

		socket.on('connect', () => {
			console.log('Connected to Socket.io server');
		});

		// Listen for new data from the server
		socket.on('newData', (data: string) => {
			console.log(`Raw data received: ${data}`);

			try {
				const parsedData: ISocketValues = JSON.parse(data); // Parse the incoming data
				console.log(parsedData);
				if (!parsedData.velocity) {
					setGolfer(parsedData.result || '');
				} else {
					setUnknownFactor(6.1 + 0.05 * (parsedData.velocity || 0));
					setVelocity((parsedData.velocity || 0) / unknownFactor); // Update the velocity
					setBallSpeed(
						((parsedData.velocity || 0) * smashFactor) /
							(unknownFactor * 0.44704)
					);
					setDistance(
						calculateDistance(
							(parsedData.velocity || 0) / unknownFactor
						)
					);
				}
			} catch (error) {
				console.error('Failed to parse data:', error);
			}
		});

		socket.on('disconnect', () => {
			console.log('Disconnected from Socket.io server');
		});

		// Clean up on unmount
		return () => {
			socket.disconnect();
		};
	}, []);

	return (
		<div className="w-[1200px] py-6 px-8 rounded-xl border-2 border-green-800 shadow-xl bg-gray-200">
			<div className="font-bold text-2xl text-green-800">
				Real - Time Performance
			</div>
			<Divider className="m-0 mt-2 border-green-800 border-[1px]" />

			<div className="flex flex-col items-center">
				<div className="flex flex-row justify-center mt-6">
					{/* Power Bar Monitoring */}
					<AccelerationMonitor velocity={velocity || 0} />

					{/* Other Values */}
					<div>
						<StatisticMonitor
							title={'Ball Speed'}
							value={ballSpeed.toFixed(2)}
							unit="mph"
						/>
						<StatisticMonitor
							title={'Sensor Distance'}
							value={
								(distance * 0.8).toFixed(2) +
								' ~ ' +
								(distance * 1.2).toFixed(2)
							}
							unit="ft"
						/>
					</div>

					<div>
						<StatisticMonitor
							title={"Golfer's Swing Style"}
							value={getFullname(golfer) || '---'}
							unit=""
							pic={getPic(golfer)}
						/>
					</div>
				</div>

				<PerformanceSubmitForm
					minDistance={distance * 0.8}
					maxDistance={distance * 1.2}
				/>
			</div>
		</div>
	);
}

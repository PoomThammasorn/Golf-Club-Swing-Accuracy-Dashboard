'use client';

import { useEffect, useRef, useState } from 'react';
import { Spin } from 'antd';
import Chart from 'chart.js/auto';

export default function PowerBar(props) {

    const canvasRef = useRef(null);
    const [chartInstance, setChartInstance] = useState(null);

    useEffect(() => {
        try {
            if (chartInstance) {
                chartInstance.destroy();
            }
            const ctx = canvasRef.current.getContext('2d');
            const data = {
                labels: [""],
                datasets: [
                    {
                        data: [120],
                        backgroundColor: ["red"],
                        borderWidth: 0,
                        borderRadius: 3,
                    },
                ],
            };

            const config = {
                type: 'bar',
                data: data,
                options: {
                    responsive: false,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: props.xAxisLabel,
                                font: {
                                    family: 'Roboto Condensed, sans-serif',
                                    size: 18,
                                    weight: 'bold',
                                },
                                color: '#666666',
                            },
                            ticks: {
                                display: false,
                                autoSkip: false,
                                font: {
                                    family: 'Roboto Condensed, sans-serif',
                                    size: 12,
                                    weight: 'bold',
                                },
                                color: '#666666',
                            },
                        },
                        y: {
                            title: {
                                display: true,
                                text: props.yAxisLabel,
                                font: {
                                    family: 'Roboto Condensed, sans-serif',
                                    size: 18,
                                    weight: 'bold',
                                },
                                color: '#666666',
                            },
                            beginAtZero: true,
                            min: 0,
                            max: 200,
                            ticks: {
                                stepSize: 50,
                                font: {
                                    family: 'Roboto Condensed, sans-serif',
                                    size: 14,
                                    weight: 'normal',
                                },
                                color: '#666666',
                            },
                        },
                    },
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            enabled: true,
                        },
                        datalabels: 
                            props.showDataLabels ? {
                                color: '#666666', 
                                font: {
                                    size: 10, 
                                    weight: 'bold'
                                },
                                anchor: 'end', 
                                align: 'end', 
                                offset: -3,
                            } : {
                                display: false,
                            },
                    },
                },
            };

            const newChartInstance = new Chart(ctx, config);
            setChartInstance(newChartInstance);

            return () => {
                newChartInstance.destroy();
            };
        } catch (ex) {
            console.error(ex);
        }
    }, []);

    return (
        <div>
            <canvas width="140" height="230" ref={canvasRef} />
        </div>
    );
}
import { useEffect, useRef, useState } from 'react';
import Chart, { ChartConfiguration } from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels'; // Import the plugin

interface LineChartProps {
    value: Array<number>;
    xAxisLabel?: string;
    yAxisLabel?: string;
    showDataLabels?: boolean;
}

// Register the plugin with Chart.js
Chart.register(ChartDataLabels);

export default function LineChart(props: LineChartProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [chartInstance, setChartInstance] = useState<Chart | null>(null);

    useEffect(() => {
        try {
            if (chartInstance) {
                chartInstance.destroy();
            }

            const ctx = canvasRef.current?.getContext('2d');
            if (!ctx) return;

            const data = {
                labels: props.value.map((_, index) => `${index + 1}`),
                datasets: [{
                    label: 'Props Data',
                    data: props.value, // Your data array
                    fill: true,
                    backgroundColor: '#41ab5d70',
                    borderColor: '#006d2c',
                    tension: 0.1
                }]
            };

            const config: ChartConfiguration<'line'> = {
                type: 'line',
                data: data,
                // options: {
                //     responsive: false,
                //     maintainAspectRatio: false,
                //     plugins: {
                //         legend: {
                //             display: false,
                //         },
                //         tooltip: {
                //             enabled: true,
                //         },
                //         datalabels: props.showDataLabels
                //             ? {
                //                   color: '#666666',
                //                   font: {
                //                       size: 10,
                //                       weight: 'bold',
                //                   },
                //                   anchor: 'end',
                //                   align: 'end',
                //                   offset: -3,
                //               }
                //             : {
                //                   display: false,
                //               },
                //     },
                options: {
                    responsive: false,
                    scales: {
                        x: {
                            title: {
                                display: true, // Set to true to display the title
                                text: 'Tries', // Text for the X-axis label
                                font: {
                                    weight: 'bold',
                                    family: 'Roboto Condensed, sans-serif',
                                    size: 16, // Font size for the label
                                },
                                padding: { // Padding for positioning
                                    top: 10, // Top padding
                                    bottom: 10 // Bottom padding
                                }
                            },
                            ticks: {
                                display: true,
                                autoSkip: false,
                                font: {
                                    family: 'Roboto Condensed, sans-serif',
                                    size: 12,
                                    weight: 'normal',
                                },
                                color: '#666666',
                            },
                        },
                        y: {
                            beginAtZero: true, // Starts Y-axis at zero
                            title: {
                                display: true, // Set to true to display the title
                                text: 'Distance Error (ft.)', // Text for the X-axis label
                                font: {
                                    weight: 'bold',
                                    family: 'Roboto Condensed, sans-serif',
                                    size: 16, // Font size for the label
                                },
                                padding: { // Padding for positioning
                                    top: 10, // Top padding
                                    bottom: 10 // Bottom padding
                                }
                            },
                            ticks: {
                                font: {
                                    family: 'Roboto Condensed, sans-serif',
                                    size: 14,
                                    weight: 'normal',
                                },
                                color: '#666666',
                            },
                        }
                    },
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            enabled: false,
                        },
                        datalabels: {
                            display: false // Ensure this plugin is disabled for data labels if you're using it
                        }
                    }
                }
            };

            const newChartInstance = new Chart(ctx, config);
            setChartInstance(newChartInstance);

            return () => {
                newChartInstance.destroy();
            };

        } catch (ex) {
            console.error(ex);
        }
    }, [props]);

    return (
        <div className='pt-6 pr-4'>
            <canvas width="400" height="200" ref={canvasRef} />
        </div>
    );
}

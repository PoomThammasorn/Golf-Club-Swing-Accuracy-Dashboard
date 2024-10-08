import { useEffect, useRef, useState } from 'react';
import Chart, { ChartConfiguration } from 'chart.js/auto';
import ChartDataLabels from 'chartjs-plugin-datalabels'; // Import the plugin

interface PowerBarProps {
    value: number;
    xAxisLabel?: string;
    yAxisLabel?: string;
    showDataLabels?: boolean;
}

// Register the plugin with Chart.js
Chart.register(ChartDataLabels);

const getColor = (value: number) => {
    if (value < 30) {
        return '#b9e840'; // Low values
    } else if (value >= 30 && value <= 70) {
        return '#fbb322'; // Medium values
    } else {
        return '#be360d'; // High values
    }
}

export default function PowerBar(props: PowerBarProps) {
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
                labels: [""],
                datasets: [
                    {
                        data: [props.value * 1.5],
                        backgroundColor: [getColor(props.value)],
                        borderWidth: 0,
                        borderRadius: 3,
                    },
                ],
            };

            const config: ChartConfiguration<'bar'> = {
                type: 'bar',
                data: data,
                options: {
                    indexAxis: 'y',
                    responsive: false,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
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
                                display: true,
                                autoSkip: false,
                                font: {
                                    family: 'Roboto Condensed, sans-serif',
                                    size: 12,
                                    weight: 'bold',
                                },
                                color: '#666666',
                            },
                        },
                        x: {
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
                            max: 100,
                            ticks: {
                                stepSize: 25,
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
                            enabled: false,
                        },
                        datalabels: props.showDataLabels
                            ? {
                                  color: '#666666',
                                  font: {
                                      size: 10,
                                      weight: 'bold',
                                  },
                                  anchor: 'end',
                                  align: 'end',
                                  offset: -3,
                              }
                            : {
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
    }, [props]);

    return (
        <div>
            <canvas width="230" height="140" ref={canvasRef} />
        </div>
    );
}

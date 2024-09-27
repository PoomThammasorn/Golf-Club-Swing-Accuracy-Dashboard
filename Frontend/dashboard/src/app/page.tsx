import HistoryPanel from "@/components/HistoryPanel";
import RealTimePanel from "@/components/RealTimePanel";

export default function Home() {
    return (
        <main>
            {/* Top bar */}
            <div className="py-6 z-10 bg-green-900 shadow-xl">
                <h1 className="text-zinc-100 text-3xl text-center font-bold">Sia Arm</h1>
            </div>

            {/* RealTimePanel */}
            <RealTimePanel />

            <HistoryPanel />
        </main>
    )
}
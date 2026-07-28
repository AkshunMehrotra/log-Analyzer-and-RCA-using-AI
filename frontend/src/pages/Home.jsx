import Navbar from "../components/Navbar";

function Home() {
    return (
        <>
            <Navbar />

            <div
                style={{
                    maxWidth: "1200px",
                    margin: "40px auto",
                    padding: "20px",
                }}
            >
                <h1>AI Log Analyzer & RCA</h1>

                <p>
                    Upload your Log, CSV or TXT file to generate
                    AI-powered Root Cause Analysis.
                </p>
            </div>
        </>
    );
}

export default Home;
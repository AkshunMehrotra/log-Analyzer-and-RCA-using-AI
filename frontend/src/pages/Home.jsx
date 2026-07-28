import Navbar from "../components/Navbar";
import UploadCard from "../components/UploadCard";

function Home() {
  return (
    <>
      <Navbar />

      <div className="container">
        <UploadCard />
      </div>
    </>
  );
}

export default Home;
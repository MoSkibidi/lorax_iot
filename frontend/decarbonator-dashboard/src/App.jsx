import { useState } from "react";
import Sidebar from "./components/sidebar";
import Dashboard from "./pages/dashboard";
import PlantStats from "./pages/PlantStats";
// import Prediction from "./pages/Prediction";
// import About from "./pages/About";

function App() {
  const [page, setPage] = useState("dashboard");

  // ฟังก์ชันช่วยเช็คว่าเมนูไหน active
  const getMenuItemClass = (targetPage) =>
    page === targetPage ? "menu-item active" : "menu-item";

  // เนื้อหาที่จะแสดงตรง main content ด้านขวา
  let contentTitle = "";
  let contentSubtitle = "";

  if (page === "dashboard") {
    contentTitle = "Dashboard Page";
    contentSubtitle = "คุณกำลังอยู่ที่หน้า Dashboard";
  } else if (page === "plant-stats") {
    contentTitle = "Plant Stats Page";
    contentSubtitle = "คุณกำลังอยู่ที่หน้า Plant Stats";
  } else if (page === "prediction") {
    contentTitle = "Map Page";
    contentSubtitle = "คุณกำลังอยู่ที่หน้า Map";
  } else if (page === "about") {
    contentTitle = "About Us Page";
    contentSubtitle = "คุณกำลังอยู่ที่หน้า About Us";
  }

  return (
    <div className="app">
      {/* ด้านซ้าย: Sidebar สีเขียว */}
      <aside className="sidebar">
        <div className="logo">
          <span className="logo-small">THE</span>
          <span className="logo-main">DECARBONATOR</span>
          <span className="logo-sub">3000</span>
        </div>

        <nav className="menu">
          <button
            className={getMenuItemClass("dashboard")}
            onClick={() => setPage("dashboard")}
          >
            DASHBOARD
          </button>

          <button
            className={getMenuItemClass("plant-stats")}
            onClick={() => setPage("plant-stats")}
          >
            PLANT STATS
          </button>

          <button
            className={getMenuItemClass("map")}
            onClick={() => setPage("map")}
          >
            Map
          </button>

          <button
            className={getMenuItemClass("about")}
            onClick={() => setPage("about")}
          >
            ABOUT US
          </button>
        </nav>

        <div className="plant-icon">
          <span className="plant-emoji">🌱</span>
        </div>
      </aside>

      {/* ด้านขวา: เนื้อหาหลัก */}
      <main className="content">
        <h1 className="content-title">{contentTitle}</h1>
        <p className="content-subtitle">{contentSubtitle}</p>
  const [plants, setPlants] = useState([
    {
      id: 1,
      name: "Plant 1",
      description: "Body text for whatever you'd like to say. Add main takeaway points, quotes, anecdotes, or even a very very short story."
    },
    {
      id: 2,
      name: "Plant 2",
      description: "Body text for whatever you'd like to say. Add main takeaway points, quotes, anecdotes, or even a very very short story."
    }
  ]);

  const handleAddPlant = () => {
    const newPlant = {
      id: plants.length + 1,
      name: `Plant ${plants.length + 1}`,
      description: "Body text for whatever you'd like to say. Add main takeaway points, quotes, anecdotes, or even a very very short story."
    };
    setPlants([...plants, newPlant]);
  };

  const renderContent = () => {
    switch (page) {
      case "dashboard":
        return <Dashboard />;
      case "plant-stats":
        return <PlantStats plants={plants} onAddPlant={handleAddPlant} />;
      case "prediction":
        return <Prediction />;
      case "about":
        return <About />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen">
      <Sidebar currentPage={page} setPage={setPage} />
      <main className="flex-1 p-10 bg-gray-100 overflow-y-auto">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;
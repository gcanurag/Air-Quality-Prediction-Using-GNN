import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from './Components/Sidebar';
import PredictPollutants from './Components/PredictPollutants';
import Homepage from './Components/HomePage';

function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/sidebar" element={<Sidebar />} />
      <Route path="/" element={<Homepage />} />
        <Route path="/predict" element={<PredictPollutants />} />
    </Routes>
  </BrowserRouter>
  )
}

export default App;

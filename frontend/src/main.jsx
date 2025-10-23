import React from 'react'
import ReactDOM from 'react-dom/client'
import MCAI3D from './components/MCAI3D'
import MCAIAutonomous3D from './components/MCAIAutonomous3D'
import ImageTo3D from './components/ImageTo3D'

const path = window.location.pathname;
const Component = path === '/generate-3d' ? ImageTo3D : MCAIAutonomous3D;

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Component />
  </React.StrictMode>,
)

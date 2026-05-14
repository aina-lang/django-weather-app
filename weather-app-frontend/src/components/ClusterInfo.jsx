import { useEffect, useState } from "react";
import axios from "axios";

export default function ClusterInfo() {
  const [info, setInfo] = useState(null);

  useEffect(() => {
    const fetchInfo = async () => {
      try {
        const res = await axios.get(
          `${import.meta.env.VITE_API_URL}/api/cluster-info/`
        );
        setInfo(res.data);
      } catch (e) {
        console.error(e);
      }
    };
    fetchInfo();
    // Refresh toutes les 5 secondes
    const interval = setInterval(fetchInfo, 5000);
    return () => clearInterval(interval);
  }, []);

  if (!info) return null;

  return (
    <div style={{
      position: "fixed",
      bottom: "16px",
      right: "16px",
      background: "rgba(0,0,0,0.8)",
      color: "white",
      padding: "12px 18px",
      borderRadius: "12px",
      fontSize: "13px",
      zIndex: 9999,
      fontFamily: "monospace",
      border: "1px solid rgba(255,255,255,0.2)"
    }}>
      <div>📦 Pod : <strong>{info.pod_name}</strong></div>
      <div>🖥️ Node : <strong style={{
        color: info.node_name === "machine1" ? "#4ade80" :
               info.node_name === "machine2" ? "#60a5fa" : "#f59e0b"
      }}>{info.node_name}</strong></div>
    </div>
  );
}

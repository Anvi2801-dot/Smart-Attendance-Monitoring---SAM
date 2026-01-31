import React, { useState } from 'react';
import './style.css';

export default function App() {
  // 1. Change to [students, setStudents] so we can update the list
  const [students, setStudents] = useState([
    { id: 1, name: 'Person_1', image: '/photo/student_1.png', status: ''},
    { id: 2, name: 'Person_2', image: '/photo/student_2.png', status: '' },
    { id: 3, name: 'Person_3', image: '/photo/student_3.png', status: '' },
    { id: 4, name: 'Person_4', image: 'https://robohash.org/student_4?set=set5', status: '' },
  ]);

  // 2. The function that talks to your Django Backend
  const runAttendance = async () => {
    console.log("AI is processing video...");
    
    try {
      // We send the request to your Django view
      const response = await fetch('http://127.0.0.1:8000/process-video/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file_path: "media/video.mp4" }) // Path to the uploaded video
      });

      const data = await response.json();

      if (data.status === "done") {
        // This replaces the empty statuses with 'Present' or 'Absent'
        setStudents(data.results); 
      }
    } catch (error) {
      console.error("Error connecting to backend:", error);
      alert("Backend not reachable. Ensure Django is running on port 8000.");
    }
  };

  return (
    <div className="App">
      <h1 style={{ textAlign: 'center', marginTop: '20px' }}>Student List</h1>

      <div style={{ display: 'flex', justifyContent: 'center', margin: '20px 0' }}>
        <button 
          onClick={runAttendance} 
          style={{
            padding: '12px 30px', backgroundColor: '#2ecc71', color: 'white',
            border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold'
          }}
        >
          Start Recognition
        </button>
      </div>

      {/* --- MAKE SURE THIS TABLE SECTION IS PRESENT --- */}
      <table className="student-table" style={{ margin: '0 auto', width: '80%' }}>
        <thead>
          <tr style={{ backgroundColor: '#16a085', color: 'white' }}>
            <th>Sr No.</th>
            <th>Name</th>
            <th>Picture</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student, index) => (
            <tr key={student.id} style={{ textAlign: 'center', borderBottom: '1px solid #ddd' }}>
              <td>{index + 1}</td>
              <td>{student.name}</td>
              <td>
                <img src={student.image} alt={student.name} style={{ width: '50px', borderRadius: '50%' }} />
              </td>
              <td style={{ 
                fontWeight: 'bold', 
                color: student.status === 'Present' ? '#2ecc71' : '#e74c3c' 
              }}>
                {student.status || "Pending..."}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
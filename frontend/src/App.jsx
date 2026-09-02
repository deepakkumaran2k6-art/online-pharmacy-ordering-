import { useEffect, useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [medicines, setMedicines] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    axios
      .get('http://127.0.0.1:8000/medicines/')
      .then((response) => {
        setMedicines(response.data)
        setLoading(false)
      })
      .catch((error) => {
        console.error(error)
        setError('Failed to load medicines')
        setLoading(false)
      })
  }, [])

  return (
    <div>
      <h1>Online Pharmacy</h1>

      <h2>Available Medicines</h2>

      {loading && <p>Loading medicines...</p>}

      {error && <p>{error}</p>}

      {!loading && !error && medicines.length === 0 && (
        <p>No medicines available.</p>
      )}

      <div>
        {medicines.map((medicine) => (
          <div key={medicine.medicine_id}>
            <h3>{medicine.medicine_name}</h3>
            <p>{medicine.description}</p>
            <p>Price: ₹{medicine.price}</p>
            <p>Stock: {medicine.stock_quantity}</p>
            <p>
              Prescription Required:{' '}
              {medicine.prescription_required ? 'Yes' : 'No'}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
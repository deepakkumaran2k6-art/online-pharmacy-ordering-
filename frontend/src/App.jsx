import { useEffect, useState } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = 'http://127.0.0.1:8000'

function App() {
  const [medicines, setMedicines] = useState([])
  const [categories, setCategories] = useState([])
  const [orders, setOrders] = useState([])

  const [search, setSearch] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

  const [cart, setCart] = useState([])
  const [showCart, setShowCart] = useState(false)
  const [showOrders, setShowOrders] = useState(false)

  const [deliveryAddress, setDeliveryAddress] = useState('')

  const [prescriptionFiles, setPrescriptionFiles] = useState({})

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem('access_token')
  )

  const [loading, setLoading] = useState(true)
  const [loginLoading, setLoginLoading] = useState(false)
  const [orderLoading, setOrderLoading] = useState(false)

  const [uploadingPrescription, setUploadingPrescription] = useState(null)

  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  useEffect(() => {
    loadMedicines()
    loadCategories()

    if (localStorage.getItem('access_token')) {
      loadOrders()
    }
  }, [])

  const loadMedicines = () => {
    axios
      .get(`${API_URL}/medicines/`)
      .then((response) => {
        setMedicines(response.data)
        setLoading(false)
      })
      .catch((error) => {
        console.error(error)
        setError('Failed to load medicines')
        setLoading(false)
      })
  }

  const loadCategories = () => {
    axios
      .get(`${API_URL}/categories/`)
      .then((response) => {
        setCategories(response.data)
      })
      .catch((error) => {
        console.error(error)
      })
  }

  const loadOrders = () => {
    const token = localStorage.getItem('access_token')

    if (!token) {
      return
    }

    axios
      .get(`${API_URL}/orders/`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then((response) => {
        setOrders(response.data)
      })
      .catch((error) => {
        console.error(error)

        if (error.response?.status === 401) {
          localStorage.removeItem('access_token')
          setIsLoggedIn(false)
        }
      })
  }

  const handleLogin = async (event) => {
    event.preventDefault()

    setError('')
    setMessage('')
    setLoginLoading(true)

    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        email: email,
        password: password
      })

      localStorage.setItem(
        'access_token',
        response.data.access_token
      )

      setIsLoggedIn(true)
      setMessage('Logged in successfully')
      setEmail('')
      setPassword('')

      loadOrders()
    } catch (error) {
      console.error(error)

      setError(
        error.response?.data?.detail ||
          'Login failed. Check your email and password.'
      )
    } finally {
      setLoginLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')

    setIsLoggedIn(false)
    setOrders([])
    setCart([])
    setPrescriptionFiles({})
    setShowCart(false)
    setShowOrders(false)

    setMessage('Logged out successfully')
    setError('')
  }

  const addToCart = (medicine) => {
    setMessage('')
    setError('')

    const existingItem = cart.find(
      (item) => item.medicine_id === medicine.medicine_id
    )

    if (existingItem) {
      if (existingItem.quantity >= medicine.stock_quantity) {
        setError('Cannot add more than available stock')
        return
      }

      setCart(
        cart.map((item) =>
          item.medicine_id === medicine.medicine_id
            ? {
                ...item,
                quantity: item.quantity + 1
              }
            : item
        )
      )
    } else {
      setCart([
        ...cart,
        {
          medicine_id: medicine.medicine_id,
          medicine_name: medicine.medicine_name,
          price: Number(medicine.price),
          stock_quantity: medicine.stock_quantity,
          quantity: 1
        }
      ])
    }

    setMessage(`${medicine.medicine_name} added to cart`)
  }

  const increaseQuantity = (medicineId) => {
    setCart(
      cart.map((item) => {
        if (item.medicine_id === medicineId) {
          if (item.quantity >= item.stock_quantity) {
            return item
          }

          return {
            ...item,
            quantity: item.quantity + 1
          }
        }

        return item
      })
    )
  }

  const decreaseQuantity = (medicineId) => {
    setCart(
      cart
        .map((item) => {
          if (item.medicine_id === medicineId) {
            return {
              ...item,
              quantity: item.quantity - 1
            }
          }

          return item
        })
        .filter((item) => item.quantity > 0)
    )
  }

  const removeFromCart = (medicineId) => {
    setCart(
      cart.filter(
        (item) => item.medicine_id !== medicineId
      )
    )
  }

  const getCartTotal = () => {
    return cart.reduce(
      (total, item) =>
        total + item.price * item.quantity,
      0
    )
  }

  const getCartCount = () => {
    return cart.reduce(
      (total, item) => total + item.quantity,
      0
    )
  }

  const handlePlaceOrder = async () => {
    setError('')
    setMessage('')

    if (!isLoggedIn) {
      setError('Please login before placing an order')
      return
    }

    if (cart.length === 0) {
      setError('Your cart is empty')
      return
    }

    if (!deliveryAddress.trim()) {
      setError('Please enter your delivery address')
      return
    }

    const token = localStorage.getItem('access_token')

    if (!token) {
      setError('Please login again')
      setIsLoggedIn(false)
      return
    }

    setOrderLoading(true)

    const orderData = {
      delivery_address: deliveryAddress.trim(),
      items: cart.map((item) => ({
        medicine_id: item.medicine_id,
        quantity: item.quantity
      }))
    }

    try {
      const response = await axios.post(
        `${API_URL}/orders/`,
        orderData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )

      setMessage(
        `Order #${response.data.order_id} placed successfully`
      )

      setCart([])
      setDeliveryAddress('')
      setShowCart(false)

      loadMedicines()
      loadOrders()
    } catch (error) {
      console.error(error)

      if (error.response?.status === 401) {
        localStorage.removeItem('access_token')
        setIsLoggedIn(false)
        setError('Session expired. Please login again.')
      } else {
        setError(
          error.response?.data?.detail ||
            'Failed to place order'
        )
      }
    } finally {
      setOrderLoading(false)
    }
  }

  const handlePrescriptionFileChange = (orderId, file) => {
    if (!file) {
      return
    }

    const allowedTypes = [
      'application/pdf',
      'image/jpeg',
      'image/png'
    ]

    if (!allowedTypes.includes(file.type)) {
      setError('Only PDF, JPG and PNG files are allowed')
      return
    }

    setPrescriptionFiles((previousFiles) => ({
      ...previousFiles,
      [orderId]: file
    }))

    setError('')
    setMessage(`${file.name} selected`)
  }

  const handlePrescriptionUpload = async (orderId) => {
    setError('')
    setMessage('')

    const token = localStorage.getItem('access_token')

    if (!token) {
      setError('Please login again')
      setIsLoggedIn(false)
      return
    }

    const file = prescriptionFiles[orderId]

    if (!file) {
      setError('Please select a prescription file')
      return
    }

    const formData = new FormData()

    formData.append('order_id', orderId)
    formData.append('file', file)

    setUploadingPrescription(orderId)

    try {
      const response = await axios.post(
        `${API_URL}/prescriptions/upload`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )

      setMessage(
        `Prescription uploaded successfully for Order #${orderId}`
      )

      setPrescriptionFiles((previousFiles) => {
        const updatedFiles = { ...previousFiles }
        delete updatedFiles[orderId]
        return updatedFiles
      })

      console.log(response.data)
    } catch (error) {
      console.error(error)

      if (error.response?.status === 401) {
        localStorage.removeItem('access_token')
        setIsLoggedIn(false)
        setError('Session expired. Please login again.')
      } else {
        setError(
          error.response?.data?.detail ||
            'Failed to upload prescription'
        )
      }
    } finally {
      setUploadingPrescription(null)
    }
  }

  const filteredMedicines = medicines.filter((medicine) => {
    const matchesSearch = medicine.medicine_name
      .toLowerCase()
      .includes(search.toLowerCase())

    const matchesCategory =
      selectedCategory === 'all' ||
      medicine.category_id === Number(selectedCategory)

    return matchesSearch && matchesCategory
  })

  return (
    <div className="pharmacy-container">
      <h1 className="pharmacy-title">
        Online Pharmacy
      </h1>

      <p className="pharmacy-subtitle">
        Find the medicines you need
      </p>

      <div className="top-actions">
        {!isLoggedIn ? (
          <form
            className="login-form"
            onSubmit={handleLogin}
          >
            <h2>Login</h2>

            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(event) =>
                setEmail(event.target.value)
              }
              required
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />

            <button
              type="submit"
              disabled={loginLoading}
            >
              {loginLoading
                ? 'Logging in...'
                : 'Login'}
            </button>
          </form>
        ) : (
          <div className="logged-in-section">
            <p>Logged in successfully</p>

            <button
              onClick={() => {
                setShowOrders(!showOrders)
                setShowCart(false)

                if (!showOrders) {
                  loadOrders()
                }
              }}
            >
              My Orders
            </button>

            <button onClick={handleLogout}>
              Logout
            </button>
          </div>
        )}

        <button
          className="cart-button"
          onClick={() => {
            setShowCart(!showCart)
            setShowOrders(false)
          }}
        >
          Cart ({getCartCount()})
        </button>
      </div>

      {message && (
        <p className="success-message">
          {message}
        </p>
      )}

      {error && (
        <p className="error">
          {error}
        </p>
      )}

      {showCart && (
        <div className="cart-section">
          <h2>Shopping Cart</h2>

          {cart.length === 0 ? (
            <p>Your cart is empty.</p>
          ) : (
            <>
              {cart.map((item) => (
                <div
                  className="cart-item"
                  key={item.medicine_id}
                >
                  <div>
                    <h3>{item.medicine_name}</h3>

                    <p>
                      ₹{item.price} × {item.quantity}
                    </p>

                    <p>
                      Subtotal: ₹
                      {(
                        item.price * item.quantity
                      ).toFixed(2)}
                    </p>
                  </div>

                  <div className="quantity-controls">
                    <button
                      onClick={() =>
                        decreaseQuantity(
                          item.medicine_id
                        )
                      }
                    >
                      -
                    </button>

                    <span>{item.quantity}</span>

                    <button
                      onClick={() =>
                        increaseQuantity(
                          item.medicine_id
                        )
                      }
                    >
                      +
                    </button>

                    <button
                      onClick={() =>
                        removeFromCart(
                          item.medicine_id
                        )
                      }
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))}

              <h2>
                Total: ₹
                {getCartTotal().toFixed(2)}
              </h2>

              <div className="order-form">
                <h3>Delivery Address</h3>

                <textarea
                  placeholder="Enter delivery address"
                  value={deliveryAddress}
                  onChange={(event) =>
                    setDeliveryAddress(
                      event.target.value
                    )
                  }
                  rows="4"
                />

                <button
                  className="place-order-button"
                  onClick={handlePlaceOrder}
                  disabled={orderLoading}
                >
                  {orderLoading
                    ? 'Placing Order...'
                    : 'Place Order'}
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {showOrders && isLoggedIn && (
        <div className="orders-section">
          <h2>My Orders</h2>

          {orders.length === 0 ? (
            <p>No orders found.</p>
          ) : (
            orders.map((order) => (
              <div
                className="order-card"
                key={order.order_id}
              >
                <h3>
                  Order #{order.order_id}
                </h3>

                <p>
                  <strong>Total:</strong> ₹
                  {Number(order.total_amount).toFixed(2)}
                </p>

                <p>
                  <strong>Status:</strong>{' '}
                  {order.order_status}
                </p>

                <p>
                  <strong>Delivery Address:</strong>{' '}
                  {order.delivery_address}
                </p>

                <p>
                  <strong>Order Date:</strong>{' '}
                  {order.order_date
                    ? new Date(
                        order.order_date
                      ).toLocaleString('en-IN')
                    : 'Not available'}
                </p>

                <div className="prescription-upload-section">
                  <h4>Upload Prescription</h4>

                  <input
                    type="file"
                    accept=".pdf,.jpg,.jpeg,.png"
                    onChange={(event) =>
                      handlePrescriptionFileChange(
                        order.order_id,
                        event.target.files[0]
                      )
                    }
                  />

                  {prescriptionFiles[order.order_id] && (
                    <p>
                      Selected:{' '}
                      {prescriptionFiles[
                        order.order_id
                      ].name}
                    </p>
                  )}

                  <button
                  type="button"
                    onClick={() =>
                      handlePrescriptionUpload(
                        order.order_id
                      )
                    }
                    disabled={
                      uploadingPrescription ===
                      order.order_id
                    }
                  >
                    {uploadingPrescription ===
                    order.order_id
                      ? 'Uploading...'
                      : 'Upload Prescription'}
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}

      <div className="controls">
        <input
          className="search-input"
          type="text"
          placeholder="Search medicine..."
          value={search}
          onChange={(event) =>
            setSearch(event.target.value)
          }
        />

        <select
          className="category-select"
          value={selectedCategory}
          onChange={(event) =>
            setSelectedCategory(
              event.target.value
            )
          }
        >
          <option value="all">
            All Categories
          </option>

          {categories.map((category) => (
            <option
              key={category.category_id}
              value={category.category_id}
            >
              {category.category_name}
            </option>
          ))}
        </select>
      </div>

      {loading && (
        <p className="loading">
          Loading medicines...
        </p>
      )}

      {!loading && !error && (
        <p className="medicine-count">
          Showing {filteredMedicines.length} of{' '}
          {medicines.length} medicines
        </p>
      )}

      {!loading &&
        filteredMedicines.length === 0 && (
          <p className="no-results">
            No medicines found.
          </p>
        )}

      <div className="medicine-grid">
        {filteredMedicines.map((medicine) => (
          <div
            className="medicine-card"
            key={medicine.medicine_id}
          >
            <h3>{medicine.medicine_name}</h3>

            <p className="medicine-description">
              {medicine.description}
            </p>

            <p className="medicine-price">
              ₹{Number(medicine.price).toFixed(2)}
            </p>

            <p className="medicine-stock">
              Stock: {medicine.stock_quantity}
            </p>

            <p className="prescription">
              Prescription Required:{' '}
              {medicine.prescription_required
                ? 'Yes'
                : 'No'}
            </p>

            <button
              onClick={() => addToCart(medicine)}
              disabled={
                medicine.stock_quantity <= 0
              }
            >
              {medicine.stock_quantity > 0
                ? 'Add to Cart'
                : 'Out of Stock'}
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
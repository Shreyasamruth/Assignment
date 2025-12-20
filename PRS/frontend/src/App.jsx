import { useState, useEffect } from 'react'
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import ProductCard from './components/ProductCard'
import SearchBar from './components/SearchBar'
import Navbar from './components/Navbar'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import AdminDashboard from './pages/AdminDashboard'
import CartPage from './pages/CartPage'
import ProfilePage from './pages/ProfilePage'
import './index.css'

function Home() {
  const [popularProducts, setPopularProducts] = useState([])
  const [searchResults, setSearchResults] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [selectedProduct, setSelectedProduct] = useState(null)
  const [loading, setLoading] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      navigate('/login')
    }
    fetchPopular()
  }, [])

  const fetchPopular = async () => {
    setLoading(true)
    try {
      const res = await fetch('http://localhost:5000/api/popular')
      const data = await res.json()
      setPopularProducts(data.products)
    } catch (e) {
      console.error("Failed to fetch popular products", e)
    }
    setLoading(false)
  }

  const handleSearch = async (query) => {
    if (!query) return
    setSearchQuery(query)
    setLoading(true)
    setSelectedProduct(null)
    try {
      const res = await fetch(`http://localhost:5000/api/search?q=${encodeURIComponent(query)}`)
      const data = await res.json()
      setSearchResults(data.products)
    } catch (e) {
      console.error("Search failed", e)
    }
    setLoading(false)
  }

  const handleProductClick = async (product) => {
    setSelectedProduct(product)
    try {
      const res = await fetch(`http://localhost:5000/api/recommend/collab/${product.product_uid}`)
      const data = await res.json()
      setRecommendations(data.products)
    } catch (e) {
      console.error("Failed to fetch recommendations", e)
    }
  }

  const addToCart = async (product) => {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch('http://localhost:5000/api/cart', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ product_id: product.product_uid })
      })
      if (res.ok) {
        alert('Added to cart!')
        window.dispatchEvent(new Event('cartUpdated'));
      }
    } catch (e) {
      console.error("Failed to add to cart", e)
    }
  }

  return (
    <div className="home-container">
      <SearchBar onSearch={handleSearch} />

      {selectedProduct && (
        <div style={{ marginBottom: '4rem' }}>
          <div className="glass-card product-detail">
            <button onClick={() => setSelectedProduct(null)} className="close-btn">&times;</button>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', alignItems: 'start' }}>
              <div style={{ borderRadius: '12px', overflow: 'hidden', height: '300px' }}>
                {selectedProduct.image_url ? (
                  <img src={selectedProduct.image_url} alt={selectedProduct.product_title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                ) : (
                  <div style={{ width: '100%', height: '100%', background: 'var(--card-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <span style={{ fontSize: '3rem' }}>{selectedProduct.product_uid.substring(0, 1)}</span>
                  </div>
                )}
              </div>
              <div>
                <h2 style={{ marginTop: 0 }}>{selectedProduct.product_title || selectedProduct.product_uid}</h2>
                <p style={{ lineHeight: 1.6, color: 'var(--text-muted)' }}>{selectedProduct.product_description}</p>
                <div className="product-actions" style={{ marginTop: '2rem' }}>
                  <span className="price">$99.99</span>
                  <button
                    className="primary-btn"
                    onClick={() => addToCart(selectedProduct)}
                  >
                    Add to Cart
                  </button>
                </div>
              </div>
            </div>
          </div>

          {recommendations.length > 0 && (
            <>
              <h2 className="section-title">You Might Also Like</h2>
              <div className="grid-container">
                {recommendations.map(p => (
                  <ProductCard key={p.product_uid} product={p} onClick={handleProductClick} />
                ))}
              </div>
            </>
          )}
        </div>
      )}

      {searchQuery && !selectedProduct && (
        <>
          <h2 className="section-title">Results for "{searchQuery}"</h2>
          {loading ? <div className="loading">Searching...</div> : (
            <div className="grid-container">
              {searchResults.length > 0 ? (
                searchResults.map(p => (
                  <ProductCard key={p.product_uid} product={p} onClick={handleProductClick} />
                ))
              ) : (
                <p>No results found.</p>
              )}
            </div>
          )}
        </>
      )}

      {!searchQuery && !selectedProduct && (
        <>
          <h2 className="section-title">Trending Now</h2>
          {loading && popularProducts.length === 0 ? <div className="loading">Loading trends...</div> : (
            <div className="grid-container">
              {popularProducts.map(p => (
                <ProductCard key={p.product_uid} product={p} onClick={handleProductClick} />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  )
}

function App() {
  const location = useLocation();
  const [cartCount, setCartCount] = useState(0);

  const fetchCartCount = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;
    try {
      const res = await fetch('http://localhost:5000/api/cart', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      setCartCount(data.cart.length);
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if (location.pathname !== '/login' && location.pathname !== '/register') {
      fetchCartCount();
      window.addEventListener('cartUpdated', fetchCartCount);
      return () => window.removeEventListener('cartUpdated', fetchCartCount);
    }
  }, [location]);

  const showNavbar = !['/login', '/register'].includes(location.pathname);

  return (
    <div className="app">
      {showNavbar && <Navbar cartCount={cartCount} />}
      <AnimatePresence mode="wait">
        <Routes location={location} key={location.pathname}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/" element={<Home />} />
        </Routes>
      </AnimatePresence>
    </div>
  )
}

export default App

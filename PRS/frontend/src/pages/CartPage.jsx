import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Trash2, ShoppingBag, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const CartPage = () => {
    const [cartItems, setCartItems] = useState([]);
    const [loading, setLoading] = useState(true);
    const [total, setTotal] = useState(0);

    useEffect(() => {
        fetchCart();
    }, []);

    const fetchCart = async () => {
        try {
            const token = localStorage.getItem('token');
            const res = await fetch('http://localhost:5000/api/cart', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();
            setCartItems(data.cart);
            calculateTotal(data.cart);
        } catch (e) {
            console.error("Failed to fetch cart", e);
        }
        setLoading(false);
    };

    const calculateTotal = (items) => {
        const sum = items.reduce((acc, item) => acc + 99.99 * (item.quantity || 1), 0);
        setTotal(sum);
    };

    const removeFromCart = async (productId) => {
        try {
            const token = localStorage.getItem('token');
            await fetch(`http://localhost:5000/api/cart/${productId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const newItems = cartItems.filter(item => item.product_uid !== productId);
            setCartItems(newItems);
            calculateTotal(newItems);
        } catch (e) {
            console.error("Failed to remove item", e);
        }
    };

    if (loading) return <div className="loading">Loading cart...</div>;

    return (
        <div className="page-container">
            <h1 className="page-title">Shopping Cart</h1>

            {cartItems.length === 0 ? (
                <div className="empty-cart glass-card">
                    <ShoppingBag size={64} className="text-muted" />
                    <h2>Your cart is empty</h2>
                    <p>Looks like you haven't added anything to your cart yet.</p>
                    <Link to="/" className="primary-btn">Start Shopping</Link>
                </div>
            ) : (
                <div className="cart-grid">
                    <div className="cart-items">
                        {cartItems.map((item) => (
                            <motion.div
                                key={item.product_uid}
                                className="cart-item glass-card"
                                layout
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, scale: 0.9 }}
                            >
                                <div className="item-image-placeholder" style={{ padding: 0, overflow: 'hidden' }}>
                                    {item.image_url ? (
                                        <img src={item.image_url} alt={item.product_title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                                    ) : (
                                        <span style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{item.product_uid.substring(0, 2)}</span>
                                    )}
                                </div>
                                <div className="item-details">
                                    <h3>{item.product_title || item.product_uid}</h3>
                                    <p className="item-desc">{item.product_description}</p>
                                    <div className="item-meta">
                                        <span className="price">$99.99</span>
                                        <span className="qty">Qty: {item.quantity || 1}</span>
                                    </div>
                                </div>
                                <button
                                    onClick={() => removeFromCart(item.product_uid)}
                                    className="icon-btn delete"
                                    title="Remove"
                                >
                                    <Trash2 size={20} />
                                </button>
                            </motion.div>
                        ))}
                    </div>

                    <div className="cart-summary glass-card">
                        <h2>Order Summary</h2>
                        <div className="summary-row">
                            <span>Subtotal</span>
                            <span>${total.toFixed(2)}</span>
                        </div>
                        <div className="summary-row">
                            <span>Shipping</span>
                            <span>Free</span>
                        </div>
                        <div className="divider"></div>
                        <div className="summary-row total">
                            <span>Total</span>
                            <span>${total.toFixed(2)}</span>
                        </div>
                        <button className="primary-btn full-width checkout-btn">
                            Proceed to Checkout <ArrowRight size={20} />
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default CartPage;

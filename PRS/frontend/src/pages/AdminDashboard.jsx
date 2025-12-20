import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

const AdminDashboard = () => {
    const navigate = useNavigate();
    const [products, setProducts] = useState([]);

    useEffect(() => {
        const role = localStorage.getItem('role');
        if (role !== 'admin') {
            navigate('/');
        }
        fetchProducts();
    }, [navigate]);

    const fetchProducts = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/products');
            const data = await res.json();
            setProducts(data.products);
        } catch (e) {
            console.error(e);
        }
    };

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    return (
        <div className="admin-dashboard">
            <header className="admin-header">
                <h1>Admin Dashboard</h1>
                <button onClick={handleLogout} className="secondary-btn">Logout</button>
            </header>

            <div className="stats-grid">
                <motion.div className="glass-card stat-card" whileHover={{ scale: 1.02 }}>
                    <h3>Total Products</h3>
                    <p className="stat-number">{products.length}</p>
                </motion.div>
                <motion.div className="glass-card stat-card" whileHover={{ scale: 1.02 }}>
                    <h3>Total Users</h3>
                    <p className="stat-number">--</p>
                </motion.div>
            </div>

            <h2 className="section-title">Product Inventory</h2>
            <div className="product-list glass-card">
                <table>
                    <thead>
                        <tr>
                            <th>Image</th>
                            <th>Title</th>
                            <th>Description</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {products.map(p => (
                            <tr key={p.product_uid}>
                                <td>
                                    {p.image_url ?
                                        <img src={p.image_url} alt="" style={{ width: 50, height: 50, objectFit: 'cover', borderRadius: 4 }} />
                                        :
                                        <div style={{ width: 50, height: 50, background: '#333', borderRadius: 4 }} />
                                    }
                                </td>
                                <td>{p.product_title || p.product_uid}</td>
                                <td>{p.product_description.substring(0, 50)}...</td>
                                <td>
                                    <button className="icon-btn">Edit</button>
                                    <button className="icon-btn delete">Delete</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AdminDashboard;

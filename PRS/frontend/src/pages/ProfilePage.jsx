import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { User, Mail, Shield, Package } from 'lucide-react';

const ProfilePage = () => {
    const [user, setUser] = useState(null);

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const token = localStorage.getItem('token');
            const res = await fetch('http://localhost:5000/api/profile', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();
            setUser(data.user);
        } catch (e) {
            console.error("Failed to fetch profile", e);
        }
    };

    if (!user) return <div className="loading">Loading profile...</div>;

    return (
        <div className="page-container">
            <motion.div
                className="profile-header glass-card"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
            >
                <div className="avatar-large">
                    {user.username.substring(0, 2).toUpperCase()}
                </div>
                <div className="profile-info">
                    <h1>{user.username}</h1>
                    <span className={`role-badge ${user.role}`}>{user.role}</span>
                </div>
            </motion.div>

            <div className="profile-grid">
                <motion.div
                    className="glass-card info-card"
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 }}
                >
                    <h2>Account Details</h2>
                    <div className="info-item">
                        <User className="icon" />
                        <div>
                            <label>Username</label>
                            <p>{user.username}</p>
                        </div>
                    </div>
                    <div className="info-item">
                        <Shield className="icon" />
                        <div>
                            <label>Account Type</label>
                            <p>{user.role === 'admin' ? 'Administrator' : 'Standard User'}</p>
                        </div>
                    </div>
                </motion.div>

                <motion.div
                    className="glass-card info-card"
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    <h2>Recent Activity</h2>
                    <div className="empty-state">
                        <Package size={48} className="text-muted" />
                        <p>No recent orders found</p>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default ProfilePage;

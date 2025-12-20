import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { ShoppingCart, User, LogOut, Search, Menu, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const Navbar = ({ cartCount }) => {
    const navigate = useNavigate();
    const location = useLocation();
    const [isScrolled, setIsScrolled] = useState(false);
    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
    const username = localStorage.getItem('username');

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const handleLogout = () => {
        localStorage.clear();
        navigate('/login');
    };

    const navLinks = [
        { name: 'Home', path: '/' },
        { name: 'Shop', path: '/' }, // For now same as home
        { name: 'New Arrivals', path: '/' },
    ];

    return (
        <nav className={`navbar ${isScrolled ? 'scrolled' : ''}`}>
            <div className="nav-container">
                <Link to="/" className="logo">
                    Luxe<span className="text-accent">Store</span>
                </Link>

                {/* Desktop Nav */}
                <div className="desktop-nav">
                    {navLinks.map((link) => (
                        <Link
                            key={link.name}
                            to={link.path}
                            className={`nav-link ${location.pathname === link.path ? 'active' : ''}`}
                        >
                            {link.name}
                        </Link>
                    ))}
                </div>

                <div className="nav-actions">
                    <Link to="/cart" className="icon-btn relative">
                        <ShoppingCart size={24} />
                        {cartCount > 0 && (
                            <span className="badge">{cartCount}</span>
                        )}
                    </Link>

                    <div className="dropdown">
                        <button className="icon-btn">
                            <User size={24} />
                        </button>
                        <div className="dropdown-content glass-card">
                            <div className="user-info">
                                <p className="text-sm text-muted">Signed in as</p>
                                <p className="font-bold">{username}</p>
                            </div>
                            <div className="divider"></div>
                            <Link to="/profile" className="dropdown-item">Profile</Link>
                            <Link to="/orders" className="dropdown-item">Orders</Link>
                            <div className="divider"></div>
                            <button onClick={handleLogout} className="dropdown-item text-error">
                                <LogOut size={16} /> Logout
                            </button>
                        </div>
                    </div>

                    <button
                        className="mobile-menu-btn"
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                    >
                        {isMobileMenuOpen ? <X /> : <Menu />}
                    </button>
                </div>
            </div>

            {/* Mobile Menu */}
            <AnimatePresence>
                {isMobileMenuOpen && (
                    <motion.div
                        className="mobile-menu glass-card"
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                    >
                        {navLinks.map((link) => (
                            <Link
                                key={link.name}
                                to={link.path}
                                className="mobile-link"
                                onClick={() => setIsMobileMenuOpen(false)}
                            >
                                {link.name}
                            </Link>
                        ))}
                    </motion.div>
                )}
            </AnimatePresence>
        </nav>
    );
};

export default Navbar;

import React from 'react';
import { motion } from 'framer-motion';

const ProductCard = ({ product, onClick }) => {
    // Fallback if no image provided
    const gradients = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%)',
        'linear-gradient(120deg, #84fab0 0%, #8fd3f4 100%)',
        'linear-gradient(120deg, #e0c3fc 0%, #8ec5fc 100%)',
        'linear-gradient(120deg, #f093fb 0%, #f5576c 100%)'
    ];
    const rnd = product.product_uid ? product.product_uid.charCodeAt(0) % gradients.length : 0;
    const bg = gradients[rnd];

    return (
        <motion.div
            className="glass-card"
            onClick={() => onClick(product)}
            style={{ cursor: 'pointer' }}
            whileHover={{ scale: 1.03 }}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
        >
            <div
                style={{
                    height: '200px',
                    borderRadius: '12px',
                    marginBottom: '1rem',
                    overflow: 'hidden',
                    position: 'relative'
                }}
            >
                {product.image_url ? (
                    <img
                        src={product.image_url}
                        alt={product.product_title || product.product_uid}
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                ) : (
                    <div style={{
                        width: '100%',
                        height: '100%',
                        background: bg,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: 'rgba(255,255,255,0.7)',
                        fontSize: '3rem',
                        fontWeight: 'bold'
                    }}>
                        {(product.product_title || product.product_uid || 'P').substring(0, 1).toUpperCase()}
                    </div>
                )}
            </div>

            <h3 style={{ fontSize: '1.2rem', margin: '0 0 0.5rem 0', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {product.product_title || product.product_uid}
            </h3>

            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: '1.4', height: '40px', overflow: 'hidden', display: '-webkit-box', WebkitLineClamp: '2', WebkitBoxOrient: 'vertical', margin: 0 }}>
                {product.product_description}
            </p>

            <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: 'var(--accent)', fontWeight: 'bold', fontSize: '1.2rem' }}>$99.99</span>
                <button className="secondary-btn" style={{ padding: '0.4rem 0.8rem', fontSize: '0.9rem' }}>View Details</button>
            </div>
        </motion.div>
    );
};

export default ProductCard;

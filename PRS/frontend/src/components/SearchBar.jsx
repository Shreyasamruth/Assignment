import React, { useState } from 'react';

const SearchBar = ({ onSearch }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch(query);
    };

    return (
        <form onSubmit={handleSubmit} style={{ margin: '2rem 0', display: 'flex', justifyContent: 'center', gap: '1rem' }}>
            <input
                type="text"
                placeholder="Search for products (e.g., 'red lipstick', 'drill')..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            />
            <button type="submit" style={{ background: 'var(--primary)', color: 'white', border: 'none' }}>
                Search
            </button>
        </form>
    );
};

export default SearchBar;

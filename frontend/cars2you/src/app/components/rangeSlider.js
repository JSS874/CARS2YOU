import React, { useState } from 'react';

export default function RangeSliderComponent() {
    // State to hold the low and high values of the slider
    const [range, setRange] = useState({ low: 20, high: 80 });

    // Handler to update state when the slider value changes
    const handleChange = (event) => {
        const { name, value } = event.target;
        setRange(prev => ({
            ...prev,
            [name]: Number(value)
        }));
    };

    return (
        <div>
            <input
                type="range"
                min="0"
                max="100"
                value={range.low}
                name="low"
                onChange={handleChange}
                style={{ marginRight: '10px' }}
            />
            <input
                type="range"
                min="0"
                max="100"
                value={range.high}
                name="high"
                onChange={handleChange}
            />
            <p>Low: {range.low}, High: {range.high}</p>
        </div>
    );
}

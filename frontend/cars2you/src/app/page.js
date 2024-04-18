'use client'

import React, { useState } from 'react';
import RangeSliderComponent from './components/rangeSlider';

export default function Home() {
  const [make, setMake] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [color, setColor] = useState('');
  const [miles, setMiles] = useState('');
  const [price, setPrice] = useState('');

  return (
    <div>
      <div>Welcome, please enter what you are looking for in a car</div>
      <div>
        <div>Make <input type="text" onChange={(event) => setMake(event.target.value)} /></div>
        <div>Model <input type="text" onChange={(event) => setModel(event.target.value)}/></div>
        <div>Year <input type="text" onChange={(event) => setYear(event.target.value)}/></div>
        <div>Color <input type="text" onChange={(event) => setColor(event.target.value)}/></div>
        <div>Miles <RangeSliderComponent /></div>
        <div>Price <RangeSliderComponent /></div>
        
        <button>Find My Car</button>
      </div>
      <div>Your car: {make} {model} {year} {color} </div>
    </div>
  );
}

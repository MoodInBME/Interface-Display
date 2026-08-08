import React from 'react';

interface Props {
  x: number;
  y: number;
  width: number;
  height: number;
  text: string;
}

export const ActionButton: React.FC<Props> = ({ x, y, width, height, text }) => {
  return (
    <button
      style={{
        position: 'absolute',
        left: x,
        top: y,
        width,
        height,
        borderRadius: 27.50,
        background: 'linear-gradient(to bottom right, var(--bg-grad-start), var(--warning))',
        color: 'var(--warning-deep)',
        border: 'none',
        display: 'flex',
        alignItems: 'center',
        paddingLeft: 24, // Guessing padding for text
        fontSize: 26, // "subjudul 26px" based on typography? The prompt says "Pengaturan" and "Kembali". Let's use 26px, bold.
        fontWeight: 'bold',
        cursor: 'pointer',
        boxSizing: 'border-box'
      }}
    >
      {text}
    </button>
  );
};

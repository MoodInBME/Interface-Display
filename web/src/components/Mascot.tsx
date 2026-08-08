import React from 'react';

export const Mascot: React.FC = () => {
  return (
    <div
      style={{
        position: 'absolute',
        left: 269,
        top: 1024 - 283, // Assuming it sits at the bottom since "menempati sisi kanan area bawah" and total height is 1024
        width: 331,
        height: 283,
        border: '2px dashed var(--danger)',
        backgroundColor: 'transparent',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: 'var(--danger)'
      }}
    >
      {/* TODO: Placeholder maskot */}
      TODO: MASCOT
    </div>
  );
};

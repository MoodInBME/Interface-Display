import React from 'react';

export const CalendarIllustration: React.FC = () => {
  // Koordinat asli dari prompt diubah menjadi relatif terhadap kartu Tren (x: 55.44, y: 471.555)
  const cx = (x: number) => x - 55.44;
  const cy = (y: number) => y - 471.555;

  return (
    <div
      style={{
        position: 'absolute',
        left: cx(21.0128),
        top: cy(521.653),
        width: 230.981,
        height: 218.907,
        backgroundColor: 'var(--surface)',
        borderRadius: 26.25,
        // Ilustrasi kalender sederhana
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        color: 'var(--text-secondary)'
      }}
    >
      {/* Representasi abstrak kalender (karena SVG tidak bisa diekstrak murni) */}
      <span style={{ fontSize: 16 }}>Kalender</span>
    </div>
  );
};

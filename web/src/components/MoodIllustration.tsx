import React from 'react';

export const MoodIllustration: React.FC = () => {
  // Koordinat asli dari prompt diubah menjadi relatif terhadap kartu (x: 55.44, y: 256.264)
  const cx = (x: number) => x - 55.44;
  const cy = (y: number) => y - 256.264;

  return (
    <>
      <div style={{ position: 'absolute', width: 55.748 * 2, height: 55.748 * 2, borderRadius: '50%', background: 'var(--primary)', left: cx(475.855) - 55.748, top: cy(292.717) - 55.748 }} />
      <div style={{ position: 'absolute', width: 61.976 * 2, height: 61.976 * 2, borderRadius: '50%', background: 'var(--warning)', left: cx(386.692) - 61.976, top: cy(396.338) - 61.976 }} />
      <div style={{ position: 'absolute', width: 42.576 * 2, height: 42.576 * 2, borderRadius: '50%', background: 'var(--success)', left: cx(505.965) - 42.576, top: cy(395.746) - 42.576 }} />
      <div style={{ position: 'absolute', width: 32.431 * 2, height: 32.431 * 2, borderRadius: '50%', background: 'var(--physio)', left: cx(372.711) - 32.431, top: cy(293.255) - 32.431 }} />
    </>
  );
};
